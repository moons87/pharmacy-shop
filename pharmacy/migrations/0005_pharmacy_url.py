# Generated by Django 4.1.1 on 2023-05-12 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0004_alter_pharmacyproductprice_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pharmacy',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
