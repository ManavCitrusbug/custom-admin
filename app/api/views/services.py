from rest_framework.views import APIView
from customadmin.models import ServiceCategory, Service, TimeSlot, BookedService, TransactionDetail
from ..serializers import ServiceCategoryListingSerializer, ServiceListingSerializer, ServiceTimeSlotSerializer, TransactionDetailSerializer, ServiceListingByCategorySerializer, ServiceDetailSerializer
from numerology.permissions import get_pagination_response
from numerology.helpers import custom_response
from rest_framework import status
from numerology.permissions import IsAccountOwner
from numerology.utils import MyStripe, create_card_object, create_customer_id, create_charge_object


class ServiceCategoryListingAPIView(APIView):
    """
    Service Category listing View
    """
    serializer_class = ServiceCategoryListingSerializer

    def get(self, request):
        service_categories = ServiceCategory.objects.filter(active=True)
        result = get_pagination_response(service_categories, request, self.serializer_class, context = {"request": request})
        message = "Service Categories fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class ServiceListingAPIView(APIView):
    """
    Service listing View
    """
    serializer_class = ServiceListingByCategorySerializer

    def get(self, request):
        categories = ServiceCategory.objects.filter(active=True)
        result = get_pagination_response(categories, request, self.serializer_class, context = {"request": request})
        message = "Services fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class PackageListingAPIView(APIView):
    """
    Service listing View
    """
    serializer_class = ServiceListingSerializer

    def get(self, request):
        services = Service.objects.filter(active=True)
        result = self.serializer_class(services, many=True, context = {"request": request})
        message = "Services fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result.data)



class ServiceDetailAPI(APIView):
    """
    Service listing View
    """
    serializer_class = ServiceDetailSerializer

    def get(self, request, pk):
        service = Service.objects.filter(active=True, pk=pk)
        if not service:
            message = "Service not found!"
            return custom_response(True, status.HTTP_200_OK, message)
        serializer = self.serializer_class(service[0], context = {"request": request})
        message = "Service fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class ServiceTimeSlotsAPIView(APIView):
    """
    Service listing View
    """
    serializer_class = ServiceTimeSlotSerializer

    def get(self, request):
        time_slots = TimeSlot.objects.filter(active=True)
        result = get_pagination_response(time_slots, request, self.serializer_class, context = {"request": request})
        message = "Service time slots fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, result)


class ServiceBookingAPIView(APIView):
    """
    API View to purchase product
    """
    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        """POST method to create the data"""
        try:
            if "service" not in request.data:
                message = "Service are required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            if "service_date" not in request.data or "service_time" not in request.data:
                message = "Service date and time are required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            if "total_amount" not in request.data :
                message = "total_amount is required!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            check_booking = BookedService.objects.filter(service_date=request.data['service_date'], service_time=request.data['service_time'])
            if check_booking:
                message = "This time slot is already booked. Please select another."
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


            if "card_id" in request.data:
                card_id = request.data["card_id"]
                stripe = MyStripe()
                customer_id = request.user.customer_id

                if not customer_id:
                    newcustomer = create_customer_id(request.user)
                    customer_id = newcustomer.id
                    print("<<<-----|| CUSTOMER CREATED ||----->>>")
                newcard = stripe.create_card(customer_id, request.data)
                data = create_card_object(newcard, request)
                card_id = newcard.id
                print("<<<-----|| CARD CREATED ||----->>>")

                newcharge = stripe.create_charge(request.data, card_id, customer_id)
                charge_object = create_charge_object(newcharge, request)

                chargeserializer = TransactionDetailSerializer(data=charge_object)
                if chargeserializer.is_valid():
                    chargeserializer.save()
                    print("<<<-----|| TransactionDetail CREATED ||----->>>")

                    transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])

                    service = Service.objects.filter(pk=request.data['service'])
                    booked_service = BookedService()
                    booked_service.service = service[0]
                    booked_service.booking_charge = service[0].booking_charge
                    booked_service.user = request.user
                    booked_service.service_date = request.data['service_date']
                    booked_service.service_time = request.data['service_time']
                    booked_service.transaction_detail = transaction[0]
                    booked_service.save()
                    message = "Service booked successfully!"
                    return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message = "Card_id is required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)