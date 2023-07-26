from django.contrib import admin
from .models import Pharmacy, PharmacyProductPrice
# Register your models here.

class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

class PharmacyProductPriceAdmin(admin.ModelAdmin):
    list_display = ('get_pharmacy_name', 'product', 'price')
    def get_pharmacy_name(self, obj):
        return obj.pharmacy.name

    get_pharmacy_name.short_description = 'Pharmacy'
admin.site.register(Pharmacy, PharmacyAdmin)
admin.site.register(PharmacyProductPrice, PharmacyProductPriceAdmin)