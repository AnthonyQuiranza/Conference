
from django import forms
from .models import Evento, Trabajo, Revision, Configuracion, Sesion
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado
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
        fields = ['nombre', 'logo', 'fecha_inicio', 'fecha_fin', 'descripcion', 'tipos_trabajo']

    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            tipos = self.instance.tipos_trabajo_list()
            self.fields['tipos_trabajo'].initial = ', '.join(tipos)



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
        fields = ['evento', 'titulo', 'hora_inicio', 'hora_fin', 'ubicacion', 'trabajo']
        widgets = {
            'evento': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'hora_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'trabajo': forms.Select(attrs={'class': 'form-control'}),
        }

class AsignarRevisorForm(forms.Form):
    revisor = forms.ModelChoiceField(queryset=UsuarioPersonalizado.objects.filter(rol='revisor'), widget=forms.Select(attrs={'class': 'form-control'}))

class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision
        fields = ['puntuacion', 'comentarios']
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control'}),
        }