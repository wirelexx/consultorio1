# Generated by Django 3.1.3 on 2020-11-23 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_consultorio', '0013_auto_20201123_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='historia_medica',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
    ]
