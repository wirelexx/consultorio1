from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pacientes', views.pacientes, name='pacientes'),
    path('<int:paciente_id>/pedidos', views.pedidos, name='pedidos'),
    path('ventas', views.ventas, name='ventas'),
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
    path("<int:paciente_id>/agregar_articulo", views.agregar_articulo, name="agregar_articulo"),
    path("<int:producto_id>/<int:paciente_id>/venta_temp", views.venta_temp, name="venta_temp"),
    path("<int:producto_id>/<int:paciente_id>/eliminar_articulo", views.eliminar_articulo, name="eliminar_articulo"),
    path("<int:venta_id>/detalle_venta", views.detalleventa, name="detalleventa"),
    path("taller", views.taller, name="taller"),
    path("gerencia", views.taller, name="gerencia"),
]