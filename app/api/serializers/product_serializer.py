from rest_framework import fields, serializers
from customadmin.models import ShopProduct


class ProductsListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ['id', 'name', 'price', 'detail', 'product_image']
