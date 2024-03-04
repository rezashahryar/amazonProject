from django.contrib import admin
from .models import Product, ProductProperty, SubLink, Size
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(ProductProperty)
admin.site.register(Size)
admin.site.register(SubLink)