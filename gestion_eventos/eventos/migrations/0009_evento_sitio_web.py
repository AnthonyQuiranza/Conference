# Generated by Django 5.0.6 on 2024-06-03 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0008_evento_capacidad_evento_es_virtual_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='sitio_web',
            field=models.URLField(blank=True, null=True),
        ),
    ]
