from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Evento, Trabajo, Revision, Sesion, UsuarioPersonalizado, Configuracion
from .forms import AsignarRevisorForm, TrabajoForm, EventoForm, RevisionForm, ConfiguracionForm, UsuarioPersonalizadoForm, SesionForm
from django.core.mail import send_mail
from django.conf import settings

def is_autor(user):
    return user.rol == 'autor'

def is_revisor(user):
    return user.rol == 'revisor'

def is_organizador(user):
    return user.rol == 'organizador'

@login_required
def dashboard(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/dashboard.html', {'eventos': eventos})

@login_required
@user_passes_test(is_organizador)
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento creado correctamente.')
            return redirect('dashboard')
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})

@login_required
@user_passes_test(is_organizador)
def personalizar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento personalizado correctamente.')
            return redirect('dashboard')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/personalizar_evento.html', {'form': form, 'evento': evento})

@login_required
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    trabajos = evento.trabajo_set.all()
    
    trabajos_con_revisiones = []
    
    for trabajo in trabajos:
        revisiones = Revision.objects.filter(trabajo=trabajo)
        tiene_revision = revisiones.filter(revisor=request.user).exists()
        revision_id = revisiones.filter(revisor=request.user).first().id if tiene_revision else None
        trabajos_con_revisiones.append({
            'trabajo': trabajo,
            'tiene_revision': tiene_revision,
            'revision_id': revision_id
        })

    es_autor = request.user.rol == 'autor'
    es_revisor = request.user.rol == 'revisor'
    es_organizador = request.user.rol == 'organizador'
    
    return render(request, 'eventos/detalle_evento.html', {
        'evento': evento,
        'trabajos_con_revisiones': trabajos_con_revisiones,
        'es_autor': es_autor,
        'es_revisor': es_revisor,
        'es_organizador': es_organizador
    })


@login_required
@user_passes_test(is_autor)
def enviar_trabajo(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = TrabajoForm(request.POST, request.FILES, evento=evento)
        if form.is_valid():
            trabajo = form.save(commit=False)
            trabajo.autor = request.user
            trabajo.evento = evento
            trabajo.save()
            try:
                send_mail(
                    'Confirmación de envío de trabajo',
                    'Su trabajo ha sido enviado exitosamente.',
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f'Error al enviar el correo: {e}')
            messages.success(request, 'Trabajo enviado correctamente.')
            return redirect('detalle_evento', evento_id=evento.id)
    else:
        form = TrabajoForm(evento=evento)
    return render(request, 'eventos/enviar_trabajo.html', {'form': form, 'evento': evento})

@login_required
@user_passes_test(is_revisor)
def revisar_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    if request.method == 'POST':
        form = RevisionForm(request.POST)
        if form.is_valid():
            revision = form.save(commit=False)
            revision.revisor = request.user
            revision.trabajo = trabajo
            revision.save()
            try:
                send_mail(
                    'Confirmación de revisión de trabajo',
                    'Su revisión ha sido enviada exitosamente.',
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, 'Error al enviar el correo: {}'.format(e))
            messages.success(request, 'Revisión enviada correctamente.')
            return redirect('detalle_evento', evento_id=trabajo.evento.id)
    else:
        form = RevisionForm()
    return render(request, 'eventos/revisar_trabajo.html', {'form': form, 'trabajo': trabajo})

@login_required
def configurar(request):
    configuracion = Configuracion.objects.first()
    if request.method == 'POST':
        form = ConfiguracionForm(request.POST, request.FILES, instance=configuracion)
        if form.is_valid():
            form.save()
            try:
                settings.EMAIL_HOST = configuracion.email_host
                settings.EMAIL_PORT = configuracion.email_port
                settings.EMAIL_HOST_USER = configuracion.email_usuario
                settings.EMAIL_HOST_PASSWORD = configuracion.email_contraseña
                send_mail(
                    'Configuración Actualizada',
                    'Los parámetros de configuración del sitio han sido actualizados correctamente.',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, 'Configuración actualizada correctamente.')
            except Exception as e:
                messages.error(request, 'Error al enviar el correo: {}'.format(e))
                messages.success(request, 'Configuración guardada, pero el correo no está configurado correctamente.')
            return redirect('dashboard')
    else:
        form = ConfiguracionForm(instance=configuracion)
    return render(request, 'eventos/configurar.html', {'form': form})

def registrar(request):
    if request.method == 'POST':
        form = UsuarioPersonalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('login')
        else:
            messages.error(request, 'Error en el formulario, por favor verifica los campos.')
    else:
        form = UsuarioPersonalizadoForm()
    return render(request, 'eventos/registrar.html', {'form': form})

@login_required
@user_passes_test(is_organizador)
def crear_sesion(request):
    if request.method == 'POST':
        form = SesionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Sesión creada correctamente.')
                return redirect('dashboard')
            except ValidationError as e:
                messages.error(request, f'Error al crear la sesión: {e}')
    else:
        form = SesionForm()
    return render(request, 'eventos/crear_sesion.html', {'form': form})

@login_required
@user_passes_test(is_organizador)
def organizar_cronograma(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    sesiones = Sesion.objects.filter(evento=evento)
    trabajos_aceptados = Trabajo.objects.filter(evento=evento, aceptado=True)
    if request.method == 'POST':
        form = SesionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Sesión asignada correctamente.')
                return redirect('organizar_cronograma', evento_id=evento.id)
            except ValidationError as e:
                messages.error(request, f'Error al asignar la sesión: {e}')
    else:
        form = SesionForm(initial={'evento': evento})
    return render(request, 'eventos/organizar_cronograma.html', {'evento': evento, 'sesiones': sesiones, 'trabajos_aceptados': trabajos_aceptados, 'form': form})

@login_required
@user_passes_test(lambda u: u.rol == 'organizador')
def asignar_revisor(request, evento_id, trabajo_id):
    evento = get_object_or_404(Evento, id=evento_id)
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    if request.method == 'POST':
        form = AsignarRevisorForm(request.POST)
        if form.is_valid():
            revisor = form.cleaned_data['revisor']
            Revision.objects.create(
                trabajo=trabajo, 
                revisor=revisor, 
                puntuacion=0,  # Valor predeterminado para puntuacion
                comentarios=''  # Valor predeterminado para comentarios
            )
            messages.success(request, 'Revisor asignado correctamente.')
            return redirect('detalle_evento', evento_id=evento.id)
    else:
        form = AsignarRevisorForm()
    return render(request, 'eventos/asignar_revisor.html', {'form': form, 'evento': evento, 'trabajo': trabajo})



@login_required
@user_passes_test(lambda u: u.rol == 'revisor')
def gestionar_revision(request, revision_id):
    revision = get_object_or_404(Revision, id=revision_id)
    if revision.revisor != request.user:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RevisionForm(request.POST, instance=revision)
        if form.is_valid():
            form.save()
            messages.success(request, 'Revisión actualizada correctamente.')
            return redirect('dashboard')
    else:
        form = RevisionForm(instance=revision)
    return render(request, 'eventos/gestionar_revision.html', {
        'form': form, 
        'revision': revision, 
        'trabajo': revision.trabajo
    })

