from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_categories')
    category = models.CharField(max_length=100)


class Size(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_sizes')
    size = models.CharField(max_length=100)


class ProductColor(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_color')
    color = models.CharField(max_length=100)


class Product(models.Model):
    category = models.ManyToManyField(ProductCategory, blank=True, related_name='cat_of_product')
    title = models.CharField(max_length=500)
    price_AED = models.DecimalField(max_digits=15, decimal_places=2)
    size = models.CharField(max_length=100, blank=True, null=True)
    available_size = models.ManyToManyField(Size, blank=True, related_name='sizes_of_product')
    colors = models.ManyToManyField(ProductColor, blank=True, related_name='color_of_product')

    def __str__(self):
        return self.title


class ProductProperty(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='properties', null=True)
    name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class SubLink(models.Model):
    link = models.CharField(max_length=2000)