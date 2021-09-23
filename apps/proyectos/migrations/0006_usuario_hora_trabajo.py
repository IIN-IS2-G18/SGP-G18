# Generated by Django 3.2.6 on 2021-09-22 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyectos', '0005_alter_proyecto_estado'),
    ]

    operations = [
        migrations.CreateModel(
            name='usuario_hora_trabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas', models.PositiveIntegerField(null=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyectos.proyecto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]