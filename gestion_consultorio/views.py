from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect    
from .models import paciente, medico, turno, historia_medica
from django import forms
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
#def index(request):
#    return render(request,"index.html")


@login_required(login_url='login_view')
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login_view"))
    else: return render(request,"index.html")
   

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
    return user.groups.filter(name__in=['Secretarias']).exists()

@login_required(login_url='login_view')
@user_passes_test(acceso_pedidos, login_url='errorpermisos')
def pedidos(request):
    return render(request,"pedidos.html")

def acceso_turnos(user):
    #define que grupos pueden acceder a la vista de turnos
    return user.groups.filter(name__in=['Medicos','Secretarias']).exists()
    
@login_required(login_url='login_view')
@user_passes_test(acceso_turnos, login_url='errorpermisos')
def turnos(request):
    if request.method == "POST":
        if request.POST['id_post'] == "form_editar_turno":
            t = turno()
            print(request.POST)
            t = turno.objects.get(pk=int(request.POST['id_turno']))
            t.id_medico=medico.objects.get(pk=int(request.POST['id_medico']))
            t.hora_turno=request.POST['hora_turno']
            t.fecha_turno=request.POST['fecha_turno']
            t.save()
            return HttpResponseRedirect(reverse('turnos'))
    usuario = None
    if request.user.is_authenticated:
        usuario_nombre = request.user.first_name
        usuario_apellido = request.user.last_name
        try:
            consulta = turno.objects.filter(id_medico=medico.objects.get(nombre=usuario_nombre,apellido=usuario_apellido)).order_by('fecha_turno','hora_turno')
        except: 
            consulta = turno.objects.all()
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
    return render(request,"atender_paciente.html",{"turno":turno.objects.get(pk=turno_id)})

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
            print(request.user.first_name)
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




