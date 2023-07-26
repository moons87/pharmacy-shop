from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
MEASUREMENT_CHOICES = (
    ('tablets', 'Таблетки'),
    ('liters', 'Литры'),
    ('grams', 'Граммы')
)
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    country         = models.TextField(max_length=100, blank=True)
    manufacturer    = models.TextField(max_length=100, blank=True)
    weight_per_tablet = models.FloatField(null=True, blank=True)
    volume_in_liters = models.FloatField(null=True, blank=True)
    price           = models.IntegerField()
    measurement = models.CharField(choices=MEASUREMENT_CHOICES, max_length=20, default='tablets')
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_data    = models.DateTimeField(auto_now_add=True)
    modified_data   = models.DateTimeField(auto_now_add=True)
    


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
    

