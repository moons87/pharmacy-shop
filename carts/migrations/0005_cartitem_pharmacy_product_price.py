# Generated by Django 4.1.1 on 2023-05-10 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0003_alter_pharmacyproductprice_product'),
        ('carts', '0004_remove_cartitem_variations'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='pharmacy_product_price',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='pharmacy.pharmacyproductprice'),
        ),
    ]