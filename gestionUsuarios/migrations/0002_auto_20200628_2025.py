# Generated by Django 2.2.13 on 2020-06-28 18:25

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gestionUsuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioinfo',
            name='articulos',
            field=djongo.models.fields.ArrayReferenceField(null=True, on_delete=djongo.models.fields.ArrayReferenceField._on_delete, related_name='mis_articulos', to='gestionArticulos.Media'),
        ),
        migrations.AlterField(
            model_name='usuarioinfo',
            name='articulos_rec',
            field=djongo.models.fields.ArrayReferenceField(null=True, on_delete=djongo.models.fields.ArrayReferenceField._on_delete, related_name='rec_articulos', to='gestionArticulos.Media'),
        ),
    ]
