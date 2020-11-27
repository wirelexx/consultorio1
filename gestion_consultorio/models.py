from django.db import models
from django.contrib.auth.models import User
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
    estado_turno = models.CharField(max_length=32, default='PENDIENTE', choices=[('PENDIENTE','pendiente'),('AUSENTE','ausente'),('ATENDIDO','atendido')])

class historia_medica(models.Model):
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    id_medico = models.ForeignKey(medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)


class producto(models.Model):
    nombre_producto = models.CharField(max_length=64)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    clasificacion = models.CharField(max_length=32, choices=[('LENTE','lente'),('ACCESORIO','accesorio'),('ETC','etc')])
    
    distacia_vision = models.CharField(max_length=10,choices=[('LEJOS','lejos'),('CERCA','cerca')])

    ojo_vision = models.CharField(max_length=32, choices=[('IZQUIERDO','izquierdo'),('DERECHO','derecho')])
  
    armazon = models.CharField(max_length=2,default="NO")

    
    def __str__(self):
        return f"{self.nombre_producto} {self.precio} {self.distacia_vision} {self.ojo_vision} {self.armazon} {self.estado}"


class venta(models.Model):
    id_paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fecha_venta = models.DateField(default=datetime.datetime(2000,1,31))
    total_vent = models.DecimalField(max_digits=8, decimal_places=2)
    id_User = models.ForeignKey(User, on_delete = models.CASCADE, blank=True)
    forma_de_pago = models.CharField(max_length=32, choices=[('EFECTIVO','efectivo'),('TARJETA DE CREDITO','tarjeta de credito'),('DEBITO','debito'),('BILLETERA VIRTUAL','billetera virtual')],blank=True)
    estado = models.CharField(max_length=32, choices=[('PENDIENTE','pendiente'),('FINALIZADO','finalizado')],default="PENDIENTE")

class detalle_venta(models.Model):
    id_venta = models.ForeignKey(venta, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(producto, on_delete=models.CASCADE)

class venta_temporal(models.Model):
    id_producto = models.ForeignKey(producto, on_delete=models.CASCADE)





