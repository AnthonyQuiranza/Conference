# Generated by Django 5.0.6 on 2024-06-03 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0007_remove_evento_revisores_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='capacidad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='es_virtual',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='evento',
            name='organizador',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='evento',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='url_virtual',
            field=models.URLField(blank=True, null=True),
        ),
    ]
