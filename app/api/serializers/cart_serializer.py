from rest_framework import fields, serializers
from customadmin.models import ProductCart, ServiceCart
from ..serializers import ProductsListingSerializer, ServiceListingSerializer


class ProductCartSerializer(serializers.ModelSerializer):
    product = ProductsListingSerializer()
    class Meta:
        model = ProductCart
        fields = ['id', 'user', 'product', 'quantity']


class ServiceCartSerializer(serializers.ModelSerializer):
    service = ServiceListingSerializer()
    class Meta:
        model = ServiceCart
        fields = ['id', 'user', 'service', 'service_date', 'service_time']