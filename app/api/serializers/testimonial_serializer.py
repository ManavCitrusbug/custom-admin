from rest_framework import fields, serializers
from customadmin.models import Testimonial


class TestimonialListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'created_at', 'logo', 'name', 'designation', 'testimonial_text']
