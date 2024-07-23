# Generated by Django 4.2 on 2024-06-30 16:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iva',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='ivas/', verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 30, 16, 36, 17, 102824, tzinfo=datetime.timezone.utc), verbose_name='Caducidad'),
        ),
    ]
