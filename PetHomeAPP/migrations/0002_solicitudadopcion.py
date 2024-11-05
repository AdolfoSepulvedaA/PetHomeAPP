# Generated by Django 5.1.2 on 2024-11-02 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetHomeAPP', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudAdopcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]