# Generated by Django 5.0.1 on 2025-07-17 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_metodo_pago_alter_order_estado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='auth0_user_id',
            new_name='auth0_id',
        ),
    ]
