# Generated by Django 3.1.3 on 2020-11-27 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_consultorio', '0019_auto_20201126_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='estado',
        ),
        migrations.AddField(
            model_name='producto',
            name='armazon',
            field=models.CharField(default='NO', max_length=2),
        ),
        migrations.AddField(
            model_name='venta',
            name='estado',
            field=models.CharField(choices=[('PENDIENTE', 'pendiente'), ('FINALIZADO', 'finalizado')], default='PENDIENTE', max_length=32),
        ),
    ]
