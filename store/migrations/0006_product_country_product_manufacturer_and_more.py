# Generated by Django 4.1.1 on 2023-05-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_reviewrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='country',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='measurement',
            field=models.CharField(choices=[('tablets', 'Таблетки'), ('liters', 'Литры'), ('grams', 'Граммы')], default='tablets', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='volume_in_liters',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight_per_tablet',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
