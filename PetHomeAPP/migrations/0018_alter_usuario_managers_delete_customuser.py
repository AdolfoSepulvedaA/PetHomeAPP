# Generated by Django 5.1.2 on 2024-11-05 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PetHomeAPP', '0017_alter_usuario_groups_alter_usuario_user_permissions_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
            ],
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
