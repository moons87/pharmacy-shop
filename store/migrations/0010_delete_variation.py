# Generated by Django 4.1.1 on 2023-05-13 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_orderproduct_variations'),
        ('store', '0009_product_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Variation',
        ),
    ]
