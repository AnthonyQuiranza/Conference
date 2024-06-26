# Generated by Django 5.0.6 on 2024-06-02 01:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sitio', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('email_host', models.CharField(max_length=100)),
                ('email_port', models.IntegerField()),
                ('email_usuario', models.CharField(max_length=100)),
                ('email_contraseña', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='logos_eventos/')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('descripcion', models.TextField()),
                ('tipos_trabajo', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('resumen', models.TextField()),
                ('tipo', models.CharField(max_length=50)),
                ('archivo', models.FileField(upload_to='trabajos/')),
                ('fecha_envio', models.DateTimeField(default=django.utils.timezone.now)),
                ('aceptado', models.BooleanField(default=False)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.evento')),
            ],
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('hora_inicio', models.DateTimeField()),
                ('hora_fin', models.DateTimeField()),
                ('ubicacion', models.CharField(max_length=200)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.evento')),
                ('trabajo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eventos.trabajo')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioPersonalizado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('rol', models.CharField(choices=[('autor', 'Autor'), ('revisor', 'Revisor'), ('organizador', 'Organizador')], max_length=15)),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='fotos_perfil/')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('titulos_academicos', models.CharField(blank=True, max_length=200, null=True)),
                ('redes_sociales', models.JSONField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='usuario_personalizado_set', related_query_name='usuario_personalizado', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='usuario_personalizado_set', related_query_name='usuario_personalizado', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='trabajo',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trabajos', to='eventos.usuariopersonalizado'),
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField()),
                ('comentarios', models.TextField()),
                ('fecha_revision', models.DateTimeField(default=django.utils.timezone.now)),
                ('trabajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.trabajo')),
                ('revisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisiones', to='eventos.usuariopersonalizado')),
            ],
        ),
    ]
