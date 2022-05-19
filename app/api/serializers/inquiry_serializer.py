from rest_framework import fields, serializers
from customadmin.models import Inquiry


class InquirySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    note = serializers.CharField(required=True)
    class Meta:
        model = Inquiry
        fields = ['id', 'name', 'email', 'inquiry_type', 'phone', 'note']


class InquiryCategoryListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['id', 'inquiry_type']
