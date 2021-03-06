# Generated by Django 3.1.3 on 2020-11-19 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_consultorio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='medico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('apellido', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_turno', models.DateTimeField()),
                ('id_medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_consultorio.medico')),
                ('id_paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_consultorio.paciente')),
            ],
        ),
    ]
