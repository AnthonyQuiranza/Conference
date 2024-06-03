from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

class Configuracion(models.Model):
    nombre_sitio = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos/')
    email_host = models.CharField(max_length=100)
    email_port = models.IntegerField()
    email_usuario = models.CharField(max_length=100)
    email_contraseña = models.CharField(max_length=100)


class TipoTrabajo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos_eventos/', blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    tipos_trabajo = models.ManyToManyField(TipoTrabajo, blank=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)  # Campo para la ubicación
    es_virtual = models.BooleanField(default=False)  # Campo para indicar si es virtual
    url_virtual = models.URLField(blank=True, null=True)  # Campo para el enlace del evento virtual
    capacidad = models.PositiveIntegerField(blank=True, null=True)  # Campo para la capacidad
    organizador = models.CharField(max_length=200, blank=True, null=False)  # Campo para el organizador

    def __str__(self):
        return self.nombre

    def tipos_trabajo_list(self):
        return [tipo.nombre for tipo in self.tipos_trabajo.all()]

    def clean(self):
        # Validar que si es_virtual es True, url_virtual no sea None
        if self.es_virtual and not self.url_virtual:
            raise ValidationError('Debe proporcionar una URL para el evento virtual.')

        # Validar que si es_virtual es False, ubicacion no sea None
        if not self.es_virtual and not self.ubicacion:
            raise ValidationError('Debe proporcionar una ubicación para el evento presencial.')


class Trabajo(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    archivo = models.FileField(upload_to='trabajos/')
    tipo = models.ForeignKey(TipoTrabajo, on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    aceptado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo


class UsuarioPersonalizado(AbstractUser):
    ROLES = (
        ('autor', 'Autor'),
        ('revisor', 'Revisor'),
        ('organizador', 'Organizador'),
    )
    rol = models.CharField(max_length=15, choices=ROLES)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    titulos_academicos = models.CharField(max_length=200, blank=True, null=True)
    redes_sociales = models.TextField(blank=True, null=True)  # Cambiado a TextField para almacenar JSON como texto

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
        Group,
        related_name='usuario_personalizado_set',  # Cambia related_name para evitar conflicto
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='usuario_personalizado',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_personalizado_set',  # Cambia related_name para evitar conflicto
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='usuario_personalizado',
    )


class Revision(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
    revisor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='revisiones')
    puntuacion = models.IntegerField(default=0)  # Valor predeterminado para puntuacion
    comentarios = models.TextField(blank=True)  # Comentarios pueden estar en blanco
    fecha_revision = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Revisión de {self.revisor.username} para {self.trabajo.titulo}"


class Sesion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    trabajo = models.ForeignKey(Trabajo, null=True, blank=True, on_delete=models.SET_NULL)

    def clean(self):
        super().clean()
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError('La hora de inicio no puede ser igual o posterior a la hora de fin.')

        solapamiento = Sesion.objects.filter(evento=self.evento, hora_inicio__lt=self.hora_fin, hora_fin__gt=self.hora_inicio).exclude(id=self.id)
        if solapamiento.exists():
            raise ValidationError('Esta sesión se solapa con otra ya programada en el evento.')

# Añadir señal para actualizar configuración de correo dinámicamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Configuracion)
def actualizar_configuracion(sender, instance, **kwargs):
    settings.EMAIL_HOST = instance.email_host
    settings.EMAIL_PORT = instance.email_port
    settings.EMAIL_HOST_USER = instance.email_usuario
    settings.EMAIL_HOST_PASSWORD = instance.email_contraseña
