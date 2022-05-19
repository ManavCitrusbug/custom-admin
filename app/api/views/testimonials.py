from rest_framework.views import APIView
from customadmin.models import Testimonial
from ..serializers import TestimonialListingSerializer
from numerology.permissions import get_pagination_response
from numerology.helpers import custom_response
from rest_framework import status


class TestimonialsListingAPIView(APIView):
    """
    Testimonials listing View
    """
    serializer_class = TestimonialListingSerializer

    def get(self, request):
        testimonials = Testimonial.objects.filter(active=True)
        result = get_pagination_response(testimonials, request, self.serializer_class, context = {"request": request})
        message = "Testimonials fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)
