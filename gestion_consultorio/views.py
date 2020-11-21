from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect    
from .models import paciente, medico, turno
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
        
        t = turno()
        t.id_paciente=paciente.objects.get(pk=int(request.POST['id_paciente']))
        t.id_medico=medico.objects.get(pk=int(request.POST['id_medico']))
        t.hora_turno=request.POST['hora_turno']
        t.fecha_turno=request.POST['fecha_turno']
        t.save()

    return render(request,"pacientes.html", {"medicos":medico.objects.all(),"pacientes": paciente.objects.all(), "form": FormNuevoPaciente()})

def pedidos(request):
    return render(request,"pedidos.html")

def turnos(request):
    return render(request,"turnos.html", {"turnos": turno.objects.all()})

def eliminar_paciente(request, paciente_id):
    p =  paciente.objects.get(pk=paciente_id)
    p.delete()
    return HttpResponseRedirect(reverse('pacientes'))

class FormNuevoPaciente(forms.Form):
    nombre = forms.CharField(label="Nombre")
    apellido =forms.CharField(label="Apellido")



