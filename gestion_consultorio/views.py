from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect    
from .models import paciente, medico, turno, historia_medica
from django import forms
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,"index.html")

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

def pedidos(request):
    return render(request,"pedidos.html")

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

    return render(request,"turnos.html", {"medicos":medico.objects.all(),"turnos": turno.objects.all().order_by('fecha_turno','hora_turno')})

def eliminar_paciente(request, paciente_id):
    p =  paciente.objects.get(pk=paciente_id)
    p.delete()
    return HttpResponseRedirect(reverse('pacientes'))

def historia_clinica(request, paciente_id):
    return render(request,"historia_clinica.html",{"paciente":paciente.objects.get(pk=paciente_id),"historia_clinica": historia_medica.objects.filter(id_paciente=paciente_id)})

def atender_paciente(request, turno_id):
    return render(request,"atender_paciente.html",{"turno":turno.objects.get(pk=turno_id)})

class FormNuevoPaciente(forms.Form):
    nombre = forms.CharField(label="Nombre")
    apellido =forms.CharField(label="Apellido")




