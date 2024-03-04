from rest_framework import serializers
from .models import Product, ProductProperty, Size, ProductCategory, ProductColor
# create your serializers here


DERHAM_TO_RIALS = 100000
DERHAM_TO_TOMAN = 10000


class LinkSerializer(serializers.Serializer):
    link = serializers.CharField()


class ProductPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProperty
        fields = ['name', 'value']


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['category']


class ProductColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['color']


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['size']


class ProductSerializer(serializers.ModelSerializer):
    properties = ProductPropertiesSerializer(many=True)
    price_toman = serializers.SerializerMethodField()
    price_rial = serializers.SerializerMethodField()
    available_size = ProductSizeSerializer(many=True)
    category = ProductCategorySerializer(many=True)
    colors = ProductColorsSerializer(many=True)

    class Meta:
        model = Product
        fields = ['title', 'price_AED', 'size', 'price_rial', 'price_toman', 'colors', 'category', 'available_size', 'properties']

    def get_price_toman(self, product):
        if product.price_AED < 100.00 and product.category.get(category='Vitamins, Minerals & Supplements'):
            price = (product.price_AED * 30 / 100) + product.price_AED
            return int(price * DERHAM_TO_TOMAN + 100000)
        if product.price_AED < 100.00:
            price = (product.price_AED * 30 / 100) + product.price_AED
            return int(price * DERHAM_TO_TOMAN + 400000)

    def get_price_rial(self, product):
        if product.price_AED < 100.00:
            price = (product.price_AED * 30 / 100) + product.price_AED
            return int(price * DERHAM_TO_RIALS + 4000000)
        else:
            price = (product.price_AED * 30 / 100) + product.price_AED
            return int(price * DERHAM_TO_RIALS + 1000000)

