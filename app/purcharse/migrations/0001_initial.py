# Generated by Django 5.1.6 on 2025-03-06 04:24

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_document', models.CharField(blank=True, max_length=50, null=True, verbose_name='NumDocumento')),
                ('issue_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Fecha Emision')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Subtotal')),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Iva')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Total')),
                ('state', models.CharField(choices=[('N', 'Normal'), ('A', 'Anulada')], default='N', max_length=1, verbose_name='Estado')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_suppliers', to='core.supplier', verbose_name='Supplier')),
            ],
            options={
                'verbose_name': 'Compras de Producto ',
                'verbose_name_plural': 'Compras de Productos',
                'ordering': ('-issue_date',),
            },
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantify', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Cantidad')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Costo')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='subtototal')),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Iva')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_products', to='core.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_detail', to='purcharse.purchase', verbose_name='Compra')),
            ],
            options={
                'verbose_name': 'Detalle de Compra',
                'verbose_name_plural': 'Detalles de la Compra',
                'ordering': ('id',),
            },
        ),
    ]
