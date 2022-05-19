from django.shortcuts import render
from django.views import View
from customadmin.models import ServiceCategory, Service, ShopProduct, TimeSlot, ProductCart, PurchasedProduct, User, TransactionDetail, ServiceCart, BookedService, CategoryImage
from api.serializers import TransactionDetailSerializer
from django.http import JsonResponse
from numerology.utils import MyStripe, create_card_object, create_customer_id, create_charge_object
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from numerology.helpers import get_cart_count

from numerology.helpers import createEvents, listEvents
import os



def format_time(hour):
    if len(hour)<2:
        hour = f"0{hour}"
    return hour


class ShopPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        product_list = ShopProduct.objects.filter(active=True)
        page = request.GET.get('page', 1)
        paginator = Paginator(product_list, 5)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        return render(request,"user/shop.html",{'products': products, 'page_title': 'Shop', 'cart_count': cart_count})


class ServicePageView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        service_categories = ServiceCategory.objects.filter(pk=pk, active=True)
        service_category = service_categories.first()
        services = Service.objects.filter(active=True, service_category=service_category.pk)
        category_img = CategoryImage.objects.filter(service_category=service_category.pk)
        return render(request,"user/services.html",{'service_category': service_category, 'page_title': 'Services', 'cart_count': cart_count, 'category_img': category_img, 'services': services})

class ServiceCategoryPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        services_list = []
        service_categories = ServiceCategory.objects.filter(active=True)
        for services_category in service_categories:
            services = Service.objects.filter(active=True, service_category=services_category)
            if services:
                services_category.services=services
                services_list.append(services_category)
        services = ServiceCategory.objects.all()
        return render(request,"user/service_category.html",{'service_categories': services_list, 'page_title': 'Service Category', 'cart_count': cart_count, 'services':services})


class ServiceDetailPageView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        service = Service.objects.filter(active=True, pk=pk)
        service_category = service[0].service_category.pk
        time_slots = TimeSlot.objects.filter(active=True)
        available_time = [f"{format_time(str(time_slot.time_slot.hour))}:{format_time(str(time_slot.time_slot.minute))}" for time_slot in time_slots]
        other_services = Service.objects.filter(active=True, related_to=service[0].pk).exclude(pk=service[0].pk)

        created_events = listEvents()
        ready_event = dict()
        for key, val in created_events.items():
            event_list = []
            time = key[11:16]
            event_list.append(val)
            event_list.append(time)
            ready_event.update({key:event_list})
        return render(request,"user/service-details.html",{'service': service[0], 'page_title': 'Service details', 'cart_count': cart_count,
                                                            'other_services': other_services, 'time_slots': available_time, 'service_category': service_category, 'ready_event':ready_event})


class PurchaseProductView(View):
    def post(self, request):
        try:
            if request.user.is_authenticated:
                user = User.objects.get(pk=request.user.pk)
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.phone = request.POST.get('phone')
                user.address = request.POST.get('address')
                user.save()

                stripe=MyStripe()
                data={}
                customer_id = user.customer_id
                if not customer_id:
                    newcustomer = create_customer_id(request.user)
                    customer_id = newcustomer.id
                    print("<<<-----|| CUSTOMER CREATED ||----->>>")

                card_token = stripe.create_token(
                    {
                        "number": request.POST.get('card_number'),
                        "exp_month": request.POST.get('month_number'),
                        "exp_year": request.POST.get('year_number'),
                        "cvc": request.POST.get('cvv_number'),
                    }
                )
                data['card_id'] = card_token.id
                newcard = stripe.create_card(customer_id, data)
                data = create_card_object(newcard, request)
                card_id = newcard.id
                print("<<<-----|| CARD CREATED ||----->>>")


                products = ProductCart.objects.filter(user=request.user.pk)
                total_amount = 0
                for item in products:
                    total_amount = total_amount + (item.product.price * item.quantity)
                data['total_amount'] = total_amount
                newcharge = stripe.create_charge(data, card_id, customer_id)
                charge_object = create_charge_object(newcharge, request)


                chargeserializer = TransactionDetailSerializer(data=charge_object)
                if chargeserializer.is_valid():
                    chargeserializer.save()
                    print("<<<-----|| TransactionDetail CREATED ||----->>>")
                    transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])
                    for product_item in products:
                        purchased_product = PurchasedProduct()
                        purchased_product.user = request.user
                        purchased_product.quantity = product_item.quantity
                        purchased_product.product = product_item.product
                        purchased_product.product_price = product_item.product.price
                        purchased_product.total_amount = product_item.product.price * float(product_item.quantity)
                        purchased_product.transaction_detail = transaction[0]
                        purchased_product.save()

                    ProductCart.objects.filter(user=request.user.pk).delete()

                    message = "Products purchased successfully!"
                    response = {
                        "message": message,
                        "status": True
                    }
                    return JsonResponse(response)
                else:
                    message = "Card_id is required"
                    return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            
            response = {
                        "message": "Login first to purchase products.",
                        "status": False
                    }
            return JsonResponse(response)
        except Exception as inst:
            message = str(inst)
            response = {
                    "message": message ,
                    "status": False
                }
            return JsonResponse(response)



class ServiceBookingView(View):
    def post(self, request):
        try:
            if request.user.is_authenticated:
                user = User.objects.get(pk=request.user.pk)
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.phone = request.POST.get('phone')
                user.address = request.POST.get('address')
                user.save()

                stripe=MyStripe()
                data={}
                customer_id = user.customer_id
                if not customer_id:
                    newcustomer = create_customer_id(request.user)
                    customer_id = newcustomer.id
                    print("<<<-----|| CUSTOMER CREATED ||----->>>")

                card_token = stripe.create_token(
                    {
                        "number": request.POST.get('card_number'),
                        "exp_month": request.POST.get('month_number'),
                        "exp_year": request.POST.get('year_number'),
                        "cvc": request.POST.get('cvv_number'),
                    }
                )
                data['card_id'] = card_token.id
                newcard = stripe.create_card(customer_id, data)
                data = create_card_object(newcard, request)
                card_id = newcard.id
                print("<<<-----|| CARD CREATED ||----->>>")

                service_cart = ServiceCart.objects.filter(user=request.user.pk)
                if service_cart[0].service_type == "Local":
                    data['total_amount'] = service_cart[0].service.booking_charge
                else:
                    data['total_amount'] = service_cart[0].service.service_charge
                check_booking = BookedService.objects.filter(service_date=service_cart[0].service_date, service_time=service_cart[0].service_time)
                if check_booking:
                    message = "This time slot is already booked. Please select another."
                    response = {
                        "message": message,
                        "status": False
                    }
                    return JsonResponse(response)

                newcharge = stripe.create_charge(data, card_id, customer_id)
                charge_object = create_charge_object(newcharge, request)

                chargeserializer = TransactionDetailSerializer(data=charge_object)
                if chargeserializer.is_valid():
                    chargeserializer.save()
                    print("<<<-----|| TransactionDetail CREATED ||----->>>")
                    transaction = TransactionDetail.objects.filter(pk=chargeserializer.data['id'])
                    booked_service = BookedService()
                    booked_service.service = service_cart[0].service
                    booked_service.booking_charge = service_cart[0].service.booking_charge
                    booked_service.user = request.user
                    booked_service.service_date = service_cart[0].service_date
                    booked_service.service_time = service_cart[0].service_time
                    booked_service.service_type = service_cart[0].service_type
                    booked_service.transaction_detail = transaction[0]
                    booked_service.save()

                    service_name = booked_service.service.name
                    service_date = booked_service.service_date
                    service_time = booked_service.service_time

                    ServiceCart.objects.filter(user=request.user.pk).delete()

                    name = str(user.first_name) + " " + user.last_name
                    address = user.address
                    phone = user.phone
                    email = user.email
                    createEvents(service_name, service_date, service_time, name, address, phone, email)

                    message = "Service booked succcessfully!"

                    response = {
                        "message": message,
                        "status": True,
                    }
                    return JsonResponse(response)
                else:
                    message = "Card_id is required"
                    return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
            
            response = {
                        "message": "Login first to book services.",
                        "status": False
                    }
            return JsonResponse(response)
        except Exception as inst:
            message = str(inst)
            response = {
                    "message": message ,
                    "status": False
                }
            return JsonResponse(response)