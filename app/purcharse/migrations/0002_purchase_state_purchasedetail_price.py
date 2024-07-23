# Generated by Django 4.2 on 2024-07-22 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purcharse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='state',
            field=models.CharField(choices=[('N', 'Normal'), ('A', 'Anulada')], default='N', max_length=1, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]
