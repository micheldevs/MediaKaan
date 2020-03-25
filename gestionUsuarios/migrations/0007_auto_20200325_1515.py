# Generated by Django 2.2.11 on 2020-03-25 14:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionUsuarios', '0006_usuario_fechacreacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='pathAvatar',
            field=models.CharField(max_length=150, validators=[django.core.validators.RegexValidator(message='El directorio escrito no es correcto.', regex='^(.+)\\/([^/]+)$')]),
        ),
    ]
