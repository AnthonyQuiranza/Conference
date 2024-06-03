
from django.contrib import admin
from .models import *

admin.site.register(Configuracion)
admin.site.register(Evento)
admin.site.register(UsuarioPersonalizado)
admin.site.register(Trabajo)
admin.site.register(Revision)
admin.site.register(Sesion)
class TipoTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

admin.site.register(TipoTrabajo, TipoTrabajoAdmin)
