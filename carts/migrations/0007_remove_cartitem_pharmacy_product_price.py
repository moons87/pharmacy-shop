# Generated by Django 4.1.1 on 2023-05-11 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_alter_cartitem_pharmacy_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='pharmacy_product_price',
        ),
    ]