from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pacientes', views.pacientes, name='pacientes'),
    path('pedidos', views.pedidos, name='pedidos'),
    path('turnos', views.turnos, name='turnos'),
    path("<int:paciente_id>/eliminar_paciente", views.eliminar_paciente, name="eliminar_paciente"),
    path("<int:paciente_id>/historia_clinica", views.historia_clinica, name="historia_clinica"),
    path("<int:turno_id>/atender_paciente", views.atender_paciente, name="atender_paciente"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("errorpermisos", views.errorpermisos, name="errorpermisos"),
    path("graba_hclinica", views.graba_hclinica, name="graba_hclinica"),
    path("<int:turno_id>/ausente_paciente", views.ausente_paciente, name="ausente_paciente"),
    path("<int:turno_id>/eliminar_turno", views.eliminar_turno, name="eliminar_turno"),
]