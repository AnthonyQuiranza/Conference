from django.urls import path
from . import views

urlpatterns = [
    path('enviar_trabajo/<int:evento_id>/', views.enviar_trabajo, name='enviar_trabajo'),
    path('personalizar_evento/<int:evento_id>/', views.personalizar_evento, name='personalizar_evento'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('revisar_trabajo/<int:trabajo_id>/', views.revisar_trabajo, name='revisar_trabajo'),
    path('configurar/', views.configurar, name='configurar'),
    path('registrar/', views.registrar, name='registrar'),
    path('crear_sesion/', views.crear_sesion, name='crear_sesion'),
    path('organizar_cronograma/<int:evento_id>/', views.organizar_cronograma, name='organizar_cronograma'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('asignar_revisores/<int:evento_id>/<int:trabajo_id>/', views.asignar_revisores, name='asignar_revisores'),
    path('quitar_revisor/', views.quitar_revisor, name='quitar_revisor'),

    path('gestionar_revision/<int:revision_id>/', views.gestionar_revision, name='gestionar_revision'),
    path('', views.dashboard, name='home'),  # URL raíz que apunta al dashboard
]
