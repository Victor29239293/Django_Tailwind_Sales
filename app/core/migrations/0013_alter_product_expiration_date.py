# Generated by Django 4.2 on 2024-07-22 01:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_product_expiration_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2024, 8, 21, 1, 28, 40, 391634, tzinfo=datetime.timezone.utc), verbose_name='Caducidad'),
        ),
    ]
