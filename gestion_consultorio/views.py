from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect    
from .models import paciente, medico, turno, historia_medica, producto, venta_temporal, venta, detalle_venta
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta
import datetime
from django.db.models import Sum,Count,Q


@login_required(login_url='login_view')
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login_view"))
    else: 
        return render(request,"index.html")
   

def errorpermisos(request):
    return render(request,"errorpermisos.html")


def acceso_pacientes(user):
    #define que grupos pueden acceder a la vista de pacientes
    return user.groups.filter(name__in=['Medicos','Secretarias']).exists()
    

@login_required(login_url='login_view')
@user_passes_test(acceso_pacientes, login_url='errorpermisos')
def pacientes(request):
    if request.method == "POST":
        form = FormNuevoPaciente(request.POST)
        if form.is_valid():
            p = paciente()
            p.nombre = form.cleaned_data["nombre"]
            p.apellido = form.cleaned_data["apellido"]
            p.save()
            return HttpResponseRedirect(reverse('pacientes'))
        
        if request.POST['id_post'] == "form_nuevo_turno":
            t = turno()
            t.id_paciente=paciente.objects.get(pk=int(request.POST['id_paciente']))
            t.id_medico=medico.objects.get(pk=int(request.POST['id_medico']))
            t.hora_turno=request.POST['hora_turno']
            t.fecha_turno=request.POST['fecha_turno']
            t.save()
            return HttpResponseRedirect(reverse('pacientes'))

        if request.POST['id_post'] == "form_editar_paciente":
            p = paciente()
            p = paciente.objects.get(pk=int(request.POST['id_paciente']))
            p.nombre=request.POST['nombre_paciente']
            p.apellido=request.POST['apellido_paciente']
            p.save()
            return HttpResponseRedirect(reverse('pacientes'))
    
    return render(request,"pacientes.html", {"medicos":medico.objects.all(),"pacientes": paciente.objects.all().order_by('apellido'), "form": FormNuevoPaciente()})

def acceso_pedidos(user):
    #define que grupos pueden acceder a la vista de turnos
    return user.groups.filter(name__in=['Vendedores']).exists()

@login_required(login_url='login_view')
@user_passes_test(acceso_pedidos, login_url='errorpermisos')
def pedidos(request,paciente_id):
    subtotal=venta_temporal.objects.aggregate(Sum('id_producto__precio'))
    return render(request,"pedidos.html",{"paciente": paciente.objects.get(pk=paciente_id), "pedido_actual": venta_temporal.objects.all(), "subtotal": subtotal})

def acceso_ventas(user):
    #define que grupos pueden acceder a la vista de turnos
    return user.groups.filter(name__in=['Vendedores']).exists()

@login_required(login_url='login_view')
@user_passes_test(acceso_ventas, login_url='errorpermisos')
def ventas(request):
    if request.method == "POST":
        v = venta()
        v.id_paciente = paciente.objects.get(pk=int(request.POST['id_paciente']))
        v.fecha_venta = datetime.date.today()
        v.total_vent = request.POST['total_venta']
        v.id_User = request.user
        if request.POST['opcion_pago']=="efectivo":
            v.forma_de_pago="EFECTIVO"
        elif request.POST['opcion_pago']=="tcredito":
            v.forma_de_pago="TARJETA DE CREDITO"
        elif request.POST['opcion_pago']=="tdebito":
            v.forma_de_pago="DEBITO"
        elif request.POST['opcion_pago']=="virtual":
            v.forma_de_pago="BILLETERA VIRTUAL"
        
        if 'taller' in request.POST:
            v.estado="PEDIDO"
        else:
            v.estado="FINALIZADO"

        v.save()
        venta_id=v.pk

        vtemp = venta_temporal.objects.all()
        for vt in vtemp:
            idpro=int(vt.id_producto.id)
            id_producto=producto.objects.get(pk=idpro)
            movimiento=detalle_venta.objects.create(id_producto=id_producto)
            movimiento.id_venta.add(venta_id)
        venta_temporal.objects.all().delete()
    else:
        venta_temporal.objects.all().delete()
    return render(request,"ventas.html",{"pacientes": paciente.objects.all().order_by('apellido','nombre')})

def agregar_articulo(request,paciente_id):
    return render(request,"agregar_articulo.html",{"productos": producto.objects.all(), "paciente":paciente_id})

def eliminar_articulo(request,producto_id,paciente_id):
    venta_temporal.objects.get(pk=producto_id).delete()
    return HttpResponseRedirect(reverse('pedidos', args=[paciente_id]))


def venta_temp(request,producto_id,paciente_id):
    venta=venta_temporal()
    venta.id_producto=producto.objects.get(pk=int(producto_id))
    venta.save() 
    return HttpResponseRedirect(reverse('pedidos', args=[paciente_id]))


def acceso_turnos(user):
    #define que grupos pueden acceder a la vista de turnos
    return user.groups.filter(name__in=['Medicos','Secretarias']).exists()
    
@login_required(login_url='login_view')
@user_passes_test(acceso_turnos, login_url='errorpermisos')
def turnos(request):
    hoy=datetime.date.today()
    fecha_filtro = {'fecha_turno': hoy}
    if request.method == "POST":
        if request.POST['id_post'] == "form_editar_turno":
            t = turno()
            t = turno.objects.get(pk=int(request.POST['id_turno']))
            t.id_medico=medico.objects.get(pk=int(request.POST['id_medico']))
            t.hora_turno=request.POST['hora_turno']
            t.fecha_turno=request.POST['fecha_turno']
            t.save()
            return HttpResponseRedirect(reverse('turnos'))
        
        elif request.POST['id_post'] == "form_filtrar_turno":
            fecha_dividida=request.POST['fecha'].split("-")
            if request.POST['opcion_fecha_filtro']=="dia":
                fecha_filtro = {'fecha_turno': request.POST['fecha']}
            elif request.POST['opcion_fecha_filtro']=="mes":
                fecha_filtro = {'fecha_turno__month': fecha_dividida[1], 'fecha_turno__year': fecha_dividida[0]}
            elif request.POST['opcion_fecha_filtro']=="anio":
                fecha_filtro = {'fecha_turno__year': fecha_dividida[0]}
            elif request.POST['opcion_fecha_filtro']=="todos":
                fecha_filtro = {}


    usuario = None
    if request.user.is_authenticated:
        usuario_nombre = request.user.first_name
        usuario_apellido = request.user.last_name
        try:
            medico_filtro=medico.objects.get(nombre=usuario_nombre,apellido=usuario_apellido)
            consulta = turno.objects.filter(id_medico=medico_filtro).filter(**fecha_filtro).order_by('fecha_turno','hora_turno')
        except: 
            consulta = turno.objects.filter(**fecha_filtro).order_by('fecha_turno','hora_turno')
    return render(request,"turnos.html", {"medicos":medico.objects.all(),"turnos": consulta})

def acceso_eliminar_pacientes(user):
    #define que grupos pueden acceder a la vista de elipacientes
    return user.groups.filter(name__in=['Secretarias']).exists()
   
@login_required(login_url='login_view')
@user_passes_test(acceso_eliminar_pacientes, login_url='errorpermisos')
def eliminar_paciente(request, paciente_id):
    p =  paciente.objects.get(pk=paciente_id)
    p.delete()
    return HttpResponseRedirect(reverse('pacientes'))

@login_required(login_url='login_view')
def historia_clinica(request, paciente_id):
    return render(request,"historia_clinica.html",{"paciente":paciente.objects.get(pk=paciente_id),"historia_clinica": historia_medica.objects.filter(id_paciente=paciente_id)})

@login_required(login_url='login_view')
def atender_paciente(request, turno_id):
    paciente_id= turno.objects.get(pk=turno_id).id_paciente
    return render(request,"atender_paciente.html",{"turno":turno.objects.get(pk=turno_id),"historia_clinica": historia_medica.objects.filter(id_paciente=paciente_id)})

class FormNuevoPaciente(forms.Form):
    nombre = forms.CharField(label="Nombre")
    apellido =forms.CharField(label="Apellido")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "mensaje": "Credenciales no validas."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"mensaje": "Desconectado."})

@login_required(login_url='login_view')
def graba_hclinica(request):
    if request.method == "POST":
        m = historia_medica()
        m.id_medico=turno.objects.get(pk=int(request.POST['id_turno'])).id_medico
        m.id_paciente=turno.objects.get(pk=int(request.POST['id_turno'])).id_paciente   
        m.fecha=request.POST['fecha']
        m.descripcion=request.POST['movimiento']
        m.save()
        id_turno=request.POST['id_turno']
        t = turno()
        t = turno.objects.get(pk=int(id_turno))
        t.estado_turno = "ATENDIDO"
        t.save()
    return HttpResponseRedirect(reverse('turnos'))

@login_required(login_url='login_view')
def ausente_paciente(request, turno_id):
    t = turno.objects.get(pk=turno_id)
    t.estado_turno = "AUSENTE"
    t.save()
    return HttpResponseRedirect(reverse('turnos'))

@login_required(login_url='login_view')
def eliminar_turno(request, turno_id):
    t = turno.objects.get(pk=turno_id)
    t.delete()
    return HttpResponseRedirect(reverse('turnos'))

def acceso_taller(user):
    #define que grupos pueden acceder a la vista de taller
    return user.groups.filter(name__in=['Tecnicos']).exists()

@user_passes_test(acceso_taller, login_url='errorpermisos')
@login_required(login_url='login_view')
def detalleventa(request, venta_id):
    return render(request,"detalle_venta.html",{"detalle":detalle_venta.objects.filter(id_venta=venta_id)})


@user_passes_test(acceso_taller, login_url='errorpermisos')
@login_required(login_url='login_view')
def taller(request):
    return render(request,"taller.html",{"ventas":venta.objects.filter(estado="PEDIDO").order_by('fecha_venta')})#, "detalle_ventas":detalle_venta.objets.all()})


@login_required(login_url='login_view')
def finalizar_pedido(request, venta_id):
    v = venta()
    v = venta.objects.get(pk=int(venta_id))
    v.estado = "FINALIZADO"
    v.save()
    return HttpResponseRedirect(reverse('taller'))


def acceso_gerencia(user):
    #define que grupos pueden acceder a la vista de gerencia
    return user.groups.filter(name__in=['Gerentes']).exists()

@user_passes_test(acceso_gerencia, login_url='errorpermisos')
@login_required(login_url='login_view')
def gerencia(request):
    return render(request,"gerencia.html")

def informe_paciente(request,seleccion,rango):
    print(seleccion)
    print(rango)
    titulo="Informe"
    if seleccion=="asistencia":
        tipo_informe="turnos"
        if rango=="semana":
            hoy = datetime.date.today() 
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = hoy + timedelta(days=6)
            contexto=turno.objects.filter(fecha_turno__range=[inicio_semana, fin_semana]).filter(estado_turno="ATENDIDO").order_by('fecha_turno')
            titulo="Pacientes que asistieron a turnos en la semana en curso"
        else:
            mes=datetime.date.today().month

            contexto=turno.objects.filter(fecha_turno__month=mes).filter(estado_turno="ATENDIDO").order_by('fecha_turno')
            titulo="Pacientes que asistieron a turnos en el mes en curso"
    elif seleccion=="ausente":
        tipo_informe="turnos"
        if rango=="semana":
            hoy = datetime.date.today() 
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = hoy + timedelta(days=6)
            contexto=turno.objects.filter(fecha_turno__range=[inicio_semana, fin_semana]).filter(estado_turno="AUSENTE").order_by('fecha_turno')
            titulo="Pacientes que no asistieron a turnos en la semana en curso"
        else:
            mes=datetime.date.today().month
            contexto=turno.objects.filter(fecha_turno__month=mes).filter(estado_turno="AUSENTE").order_by('fecha_turno')
            titulo="Pacientes que asistieron a turnos en el mes en curso"               
    elif seleccion=="compra":
        tipo_informe="compras"
        if rango=="semana":
            hoy = datetime.date.today() 
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            fin_semana = hoy + timedelta(days=6)
            contexto=venta.objects.filter(fecha_venta__range=[inicio_semana,fin_semana]).order_by('fecha_venta')
            titulo="Pacientes que hicieron compras en la semana en curso"
        else:
            mes=datetime.date.today().month
            contexto=venta.objects.filter(fecha_venta__month=mes).order_by('fecha_venta')
            titulo="Pacientes que hicieron compras en el mes en curso" 

    return render(request,"informes_paciente.html",{"titulo":titulo, "contexto": contexto, "tipo_informe": tipo_informe})

def mas_vendidos(request):
    mes=datetime.date.today().month
    #Item.objects.values("contest").annotate(Count("id"))
    #a=detalle_venta.objects.annotate(c=Count('id_producto__nombre_producto'))#.order_by('-num_books')[:5]
    #subtotal=venta_temporal.objects.aggregate(Sum('id_producto__precio'))
    #print(a)
    #b=detalle_venta.objects.count()
    #print(b)
    #ventas_del_mes = detalle_venta.objects.filter(id_venta__fecha_venta__month=mes)
    #productos = producto.objects.all().annotate(ventas_totales=Count('detalle_venta'))
    ventas1 = producto.objects.all().annotate(ventas_totales=Count('detalle_venta',filter=Q(detalle_venta__id_venta__fecha_venta__month=mes)))
        #distinct=True))
    
    #for unProducto in productos:
    #    unProducto.

    print(ventas1[1].ventas_totales)
    
    #print(ventas_totales)
    return render(request,"informes_paciente.html")

def ventas_por_vendedor(request):
    return render(request,"informes_paciente.html")   

