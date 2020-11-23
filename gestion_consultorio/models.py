from django.db import models
import datetime

# Create your models here.

class paciente(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class medico(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class turno(models.Model):
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fecha_turno =  models.DateField()
    hora_turno =  models.TimeField()
    id_medico = models.ForeignKey(medico, on_delete=models.CASCADE)

class historia_medica(models.Model):
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    id_medico = models.ForeignKey(medico, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.datetime(2000,1,31))
    descripcion = models.TextField(blank=True)





