from rest_framework.views import APIView
from ..serializers import InquirySerializer, InquiryCategoryListingSerializer
from numerology.helpers import custom_response, serialized_response
from rest_framework import status
from customadmin.models import Inquiry, InquiryType
from numerology.permissions import get_pagination_response



class InquiryAPIView(APIView):
    """
    User Sign up view
    """
    serializer_class = InquirySerializer

    def post(self, request, *args, **kwargs):
        message = "Inquiry sent successfully!"
        print(request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        # TODO Email
        return custom_response(response_status, status_code, message)


class InquirycategoryListing(APIView):
    """
    Inquiry category listing View
    """
    serializer_class = InquiryCategoryListingSerializer

    def get(self, request):
        inquiry_types = InquiryType.objects.filter(active=True)
        result = self.serializer_class(inquiry_types, many=True, context = {"request": request})
        message = "Inquiry types fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result.data)
