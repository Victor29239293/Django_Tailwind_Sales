# Generated by Django 4.2 on 2024-07-22 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purcharse', '0002_purchase_state_purchasedetail_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='change',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Cambio'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='payment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Pago'),
        ),
    ]
