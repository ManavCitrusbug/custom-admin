from rest_framework import fields, serializers
from customadmin.models import ServiceCategory, Service, TimeSlot


class ServiceCategoryListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'category_name']


class ServiceListingSerializer(serializers.ModelSerializer):
    service_category = ServiceCategoryListingSerializer()
    class Meta:
        model = Service
        fields = ['id', 'name', 'booking_charge', 'service_charge', 'detail', 'service_image', 'service_category']


class ServiceTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'time_slot']


class ServiceListingByCategorySerializer(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()
    class Meta:
        model = ServiceCategory
        fields = ['id', 'category_name', 'services']
    
    def get_services(self, instance):
        services = Service.objects.filter(service_category=instance.pk)
        serializer = ServiceListingSerializer(services, many=True, context={"request": self.context.get('request')})
        return serializer.data


class ServiceDetailSerializer(serializers.ModelSerializer):
    service_category = ServiceCategoryListingSerializer()
    related_services = serializers.SerializerMethodField()
    class Meta:
        model = Service
        fields = ['id', 'name', 'booking_charge', 'service_charge', 'detail', 'service_image', 'service_category', 'related_services']

    def get_related_services(self, instance):
        services = Service.objects.filter(related_to=instance.pk, active=True).exclude(pk=instance.pk)
        serializer = ServiceListingSerializer(services, many=True, context={"request": self.context.get('request')})
        return serializer.data