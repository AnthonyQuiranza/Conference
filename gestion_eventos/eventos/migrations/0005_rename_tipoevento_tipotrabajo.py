# Generated by Django 5.0.6 on 2024-06-03 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_tipoevento_remove_evento_tipos_trabajo_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TipoEvento',
            new_name='TipoTrabajo',
        ),
    ]
