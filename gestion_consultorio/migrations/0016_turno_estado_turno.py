# Generated by Django 3.1.2 on 2020-11-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_consultorio', '0015_detalle_venta_producto_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='estado_turno',
            field=models.CharField(choices=[('PENDIENTE', 'pendiente'), ('AUSENTE', 'ausente'), ('ATENDIDO', 'atendido')], default='PENDIENTE', max_length=64),
        ),
    ]
