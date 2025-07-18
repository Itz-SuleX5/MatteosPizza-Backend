# Generated by Django 5.0.1 on 2025-07-17 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='metodo_pago',
            field=models.CharField(default='Efectivo', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('preparando', 'Preparando'), ('enviado', 'Enviado'), ('entregado', 'Entregado'), ('cancelado', 'Cancelado')], default='Pendiente', max_length=20),
        ),
    ]
