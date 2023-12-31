from django.contrib import admin
from . import models


# Register your models here.


class AdminProduct(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active']
    list_editable = ['price', 'is_active']


admin.site.register(models.Product, AdminProduct)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)
