from rest_framework.views import APIView
from ..serializers import ProductCartSerializer, ServiceCartSerializer
from numerology.helpers import custom_response, serialized_response
from rest_framework import status
from numerology.permissions import IsAccountOwner
from customadmin.models import ProductCart, ServiceCart, ShopProduct, Service, BookedService
from numerology.permissions import get_pagination_response



class ProductCartAPIView(APIView):
    """
    Product Cart API View
    """
    serializer_class = ProductCartSerializer
    permission_classes = (IsAccountOwner,)

    def post(self, request, *args, **kwargs):
        if 'product' not in request.data:
            message = "Product is required!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        
        service_in_cart = ServiceCart.objects.filter(user=request.user.pk)
        if service_in_cart:
            message = "Your already have a service in your cart. Remove that first to add products."
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        quantity = request.data['quantity'] if 'quantity' in request.data else 1

        product_in_cart = ProductCart.objects.filter(user=request.user.pk, product=request.data['product'])
        if product_in_cart:
            product_in_cart[0].quantity = product_in_cart[0].quantity + quantity
            product_in_cart[0].save()
        else:
            product = ShopProduct.objects.filter(pk=request.data['product'])
            if not product:
                message = "Product not found!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            ProductCart.objects.create(user=request.user, product=product[0], quantity=quantity)
        message = "Product added to cart"
        data = {}
        data['cart_type'] = "product_cart"
        cart_count = ProductCart.objects.filter(user=request.user.pk)
        data['cart_count'] = cart_count.count()
        return custom_response(True, status.HTTP_201_CREATED, message, data)

    
    def delete(self, request):
        if 'product' not in request.data:
            message = "Product is required!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        products  = ProductCart.objects.filter(user=request.user.pk, product=request.data['product'])
        if products:
            products[0].quantity = products[0].quantity - 1
            products[0].save()

            if products[0].quantity <= 0:
                products.delete()
        message = "Product removed from cart successfully!"
        data = {}
        data['cart_type'] = "product_cart"
        cart_count = ProductCart.objects.filter(user=request.user.pk)
        data['cart_count'] = cart_count.count()
        return custom_response(True, status.HTTP_200_OK, message, data)


class ServiceCartAPIView(APIView):
    """
    Service Cart API View
    """
    serializer_class = ProductCartSerializer
    permission_classes = (IsAccountOwner,)

    def post(self, request, *args, **kwargs):
        try:
            if 'service' not in request.data:
                message = "Service is required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            
            if 'service_date' not in request.data or 'service_time' not in request.data:
                message = "service_date and service_time are required"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            check_booking = BookedService.objects.filter(service_date=request.data['service_date'], service_time=request.data['service_time'])
            if check_booking:
                message = "This time slot is already booked. Please select another."
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            service_in_cart = ServiceCart.objects.filter(user=request.user.pk)
            if service_in_cart:
                message = "Your already have a service in your cart. Remove that first to add another."
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

            product_in_cart = ProductCart.objects.filter(user=request.user.pk)
            if product_in_cart:
                message = "Your already have a product in your cart. Remove that first to add service."
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            service = Service.objects.filter(pk=request.data['service'])
            if not service:
                message = "Service not found!"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            ServiceCart.objects.create(user=request.user, service=service[0], service_date=request.data['service_date'], service_time=request.data['service_time'])
            message = "Service added to cart"
            data = {}
            data['cart_type'] = "service_cart"
            data['cart_count'] = 1
            return custom_response(True, status.HTTP_201_CREATED, message, data)
        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
    
    def delete(self, request):
        if 'service' not in request.data:
            message = "Service is required!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        services  = ServiceCart.objects.filter(user=request.user.pk, service=request.data['service'])
        if services:
            services[0].delete()

        data = {}
        data['cart_type'] = "service_cart"
        data['cart_count'] = 0
        message = "Service removed from cart successfully!"
        return custom_response(True, status.HTTP_200_OK, message, data)


class ShoppingCartAPIView(APIView):
    """
    Shopping cart API View
    """

    serializer_class = ProductCartSerializer
    permission_classes = (IsAccountOwner,)

    def get(self, request):
        message = "Shopping cart fetched Successfully!"
        products  = ProductCart.objects.filter(user=request.user.pk)
        if products:
            result = get_pagination_response(products, request, self.serializer_class, context = {"request": request})
            return custom_response(True, status.HTTP_200_OK, message, result)
        
        services = ServiceCart.objects.filter(user=request.user.pk)
        if services:
            serializer = ServiceCartSerializer(services[0], context = {"request": request})
            return custom_response(True, status.HTTP_200_OK, message, serializer.data)
        
        return custom_response(True, status.HTTP_200_OK, message)
