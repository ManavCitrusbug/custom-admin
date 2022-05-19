from django.shortcuts import render, redirect
from django.views import View
from customadmin.models import BookedService, ServiceCart, ProductCart, Service, ShopProduct, User
from django.http import JsonResponse
from django.contrib.auth import login, logout


class AddServiceToCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        try:
            service_id = request.POST.get('service_id')
            if not service_id:
                response = {
                        "message": "Service not found" ,
                        "status": False
                    }
                return JsonResponse(response)
                
            service_type = request.POST.get('service_type')
            service_date = request.POST.get('service_date')
            service_time = request.POST.get('service_time')
            if not service_date or not service_time:
                response = {
                        "message": "Please select date and time" ,
                        "status": False
                    }
                return JsonResponse(response)

            if not service_type:
                response = {
                        "message": "Please select service type" ,
                        "status": False
                    }
                return JsonResponse(response)

            check_booking = BookedService.objects.filter(service_date=service_date, service_time=service_time)
            if check_booking:
                response = {
                        "message": "The date or time you have selected is unavailable. Please reselect or check the service page to find out on the possible booking slots.",
                        "status": False
                    }
                return JsonResponse(response)

            service_in_cart = ServiceCart.objects.filter(user=user.pk)
            if service_in_cart:
                response = {
                        "message": "Your already have a service in your cart. Remove that first to add another.",
                        "status": False
                    }
                return JsonResponse(response)

            product_in_cart = ProductCart.objects.filter(user=user.pk)
            if product_in_cart:
                response = {
                        "message": "Your already have a product in your cart. Remove that first to add service.",
                        "status": False
                    }
                return JsonResponse(response)

            service = Service.objects.filter(pk=service_id)
            if not service:
                response = {
                        "message": "Service not found!",
                        "status": False
                    }
                return JsonResponse(response)
            ServiceCart.objects.create(user=user, service=service[0], service_date=service_date, service_time=service_time, service_type=service_type)
            response = {
                        "message": "Service added to cart",
                        "status": True
                    }
            return JsonResponse(response)
        except Exception as inst:
                print(inst)
                response = {
                            "message": str(inst),
                            "status": False
                        }
                return JsonResponse(response)


class BookingPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        service_in_cart = ServiceCart.objects.filter(user=user.pk)
        if service_in_cart:
            return render(request,"user/booking.html",{'page_title': 'Checkout', 'service':service_in_cart[0], 'cart_count': service_in_cart.count()})
        return render(request,"user/booking.html",{'page_title': 'Checkout', 'cart_count': service_in_cart.count()})


class CartPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        service_in_cart = ServiceCart.objects.filter(user=user.pk)
        if service_in_cart:
            return render(request,"user/booking.html",{'page_title': 'Checkout', 'service':service_in_cart[0], 'cart_count': service_in_cart.count()})
        product_in_cart = ProductCart.objects.filter(user=user.pk)
        if product_in_cart:
            if product_in_cart:
                count =0
                for product in product_in_cart:
                    count += product.quantity
            return render(request,"user/add-to-cart.html",{'page_title': 'Cart', 'products':product_in_cart, 'cart_count': count})
        return redirect('/')


class RemoveServiceFromCart(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        services  = ServiceCart.objects.filter(user=user.pk, service=pk)
        if services:
            services[0].delete()
        return redirect('services-category')


class AddProductToCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        service_in_cart = ServiceCart.objects.filter(user=user.pk)
        if service_in_cart:
            response = {
                "message": "Your already have a service in your cart. Remove that first to add products.",
                "status": False
            }
            return JsonResponse(response)
        quantity = request.POST.get('quantity') if 'quantity' in request.POST else 1
        product_in_cart = ProductCart.objects.filter(user=user.pk, product=request.POST.get('product'))
        if product_in_cart:
            product_in_cart[0].quantity = product_in_cart[0].quantity + quantity
            product_in_cart[0].save()
        else:
            product = ShopProduct.objects.filter(pk=request.POST.get('product'))
            if not product:
                response = {
                    "message": "Product not found!",
                    "status": False
                }
                return JsonResponse(response)
            ProductCart.objects.create(user=user, product=product[0], quantity=quantity)
        response = {
                    "message": "Product added to cart",
                    "status": True
                }
        return JsonResponse(response)


class RemoveProductFromCart(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        products  = ProductCart.objects.filter(user=user.pk, product=pk)
        if products:
            products[0].quantity = products[0].quantity - 1
            products[0].save()
            if products[0].quantity <= 0:
                products.delete()
                cart_products  = ProductCart.objects.filter(user=user.pk)
                if cart_products:
                    return redirect('../cart-page/')            
                return redirect('../shop/')        
        return redirect('../cart-page/')


class PaymentSuccessPage(View):
    def get(self, request):
        if request.user:
            return render(request,"user/payment-success.html",{'page_title': 'Payment success', 'cart_count': 0})            
        return render(request,"user/login.html",{'page_title': 'Login', 'cart_count': 0})
