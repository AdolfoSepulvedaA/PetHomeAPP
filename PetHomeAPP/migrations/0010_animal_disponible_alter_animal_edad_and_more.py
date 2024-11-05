# Generated by Django 5.1.2 on 2024-11-03 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetHomeAPP', '0009_alter_usuario_options_alter_usuario_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='disponible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='animal',
            name='edad',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='animal',
            name='especie',
            field=models.CharField(max_length=50),
        ),
    ]