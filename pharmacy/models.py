from django.db import models
from store.models import Product

class Pharmacy(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    products = models.ManyToManyField(Product, through='PharmacyProductPrice')
    url = models.URLField(max_length=200, null=True)
class PharmacyProductPrice(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()

    class Meta:
        unique_together = (('product', 'pharmacy'),)
    
    def __str__(self):
        return self.pharmacy.name


    