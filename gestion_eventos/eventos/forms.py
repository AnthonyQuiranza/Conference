
from django import forms
from .models import Evento, Trabajo, Revision, Configuracion, Sesion
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado
from django_select2.forms import Select2MultipleWidget
import json

TIPOS_TRABAJO_CHOICES = [
    ('paper', 'Paper'),
    ('articulo', 'Artículo'),
    ('poster', 'Póster'),
    # Agrega más opciones según sea necesario
]

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'logo', 'fecha_inicio', 'fecha_fin', 'descripcion', 'tipos_trabajo', 'es_virtual', 'ubicacion', 'url_virtual', 'capacidad','sitio_web','organizador']
        widgets = {
            'tipos_trabajo': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        es_virtual = cleaned_data.get("es_virtual")
        ubicacion = cleaned_data.get("ubicacion")
        url_virtual = cleaned_data.get("url_virtual")

        if es_virtual and not url_virtual:
            self.add_error('url_virtual', 'Debe proporcionar una URL para el evento virtual.')
        elif not es_virtual and not ubicacion:
            self.add_error('ubicacion', 'Debe proporcionar una ubicación para el evento presencial.')

        return cleaned_data




class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ['titulo', 'resumen', 'archivo', 'tipo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        evento = kwargs.pop('evento', None)
        super().__init__(*args, **kwargs)
        if evento:
            self.fields['tipo'].queryset = evento.tipos_trabajo.all()



class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = ['puntuacion', 'comentarios']
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['nombre_sitio', 'logo', 'email_host', 'email_port', 'email_usuario', 'email_contraseña']
        widgets = {
            'nombre_sitio': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'email_host': forms.TextInput(attrs={'class': 'form-control'}),
            'email_port': forms.NumberInput(attrs={'class': 'form-control'}),
            'email_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'email_contraseña': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class UsuarioPersonalizadoForm(UserCreationForm):
    twitter = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter'}))
    linkedin = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'LinkedIn'}))

    class Meta:
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'rol', 'foto_perfil', 'descripcion', 'titulos_academicos', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'titulos_academicos': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_redes_sociales(self):
        twitter = self.cleaned_data.get('twitter')
        linkedin = self.cleaned_data.get('linkedin')
        redes_sociales = {}

        if twitter:
            redes_sociales['twitter'] = twitter
        if linkedin:
            redes_sociales['linkedin'] = linkedin

        return json.dumps(redes_sociales)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.redes_sociales = self.clean_redes_sociales()
        if commit:
            user.save()
        return user






class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion
        fields = ['titulo', 'hora_inicio', 'hora_fin', 'trabajo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'hora_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'trabajo': forms.Select(attrs={'class': 'form-control'}),
        }




class AsignarRevisorForm(forms.Form):
    revisores = forms.ModelMultipleChoiceField(
        queryset=UsuarioPersonalizado.objects.filter(rol='revisor'),
        widget=Select2MultipleWidget(attrs={'class': 'form-control'})
    )



class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = ['puntuacion', 'comentarios']
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control'}),
        }