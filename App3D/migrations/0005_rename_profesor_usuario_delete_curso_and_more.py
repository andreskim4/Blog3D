# Generated by Django 4.1.3 on 2023-01-03 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App3D', '0004_delete_message'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profesor',
            new_name='usuario',
        ),
        migrations.DeleteModel(
            name='Curso',
        ),
        migrations.DeleteModel(
            name='Entregable',
        ),
        migrations.DeleteModel(
            name='Estudiante',
        ),
    ]