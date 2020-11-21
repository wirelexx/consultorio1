from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pacientes', views.pacientes, name='pacientes'),
    path('pedidos', views.pedidos, name='pedidos'),
    path('turnos', views.turnos, name='turnos'),
    path("<int:paciente_id>/eliminar_paciente", views.eliminar_paciente, name="eliminar_paciente"),
]