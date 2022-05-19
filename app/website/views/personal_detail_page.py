from django.shortcuts import render
from django.views import View
from customadmin.models import User, TransactionDetail, BookedService, PurchasedProduct
from django.http import JsonResponse
from dateutil.parser import parse
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from numerology.helpers import get_cart_count


class ProfilePageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_count = get_cart_count(request.user)
            transactions = TransactionDetail.objects.filter(user=request.user.pk).order_by('-pk')
            transaction_list = []
            calendar_list = []
            for transaction in transactions:
                is_service = BookedService.objects.filter(transaction_detail=transaction.pk)
                transaction.item_type = "service" if is_service else "product"
                
                if is_service:
                    transaction.service_type = is_service[0].service_type
                    if transaction.service_type == "Overseas":
                        transaction.item_price = is_service[0].service.service_charge
                    else:
                        transaction.item_price = is_service[0].service.booking_charge
                    transaction.item_name = is_service[0].service.name
                    transaction.item_date = is_service[0].service_date
                    transaction.item_time = is_service[0].service_time
                    transaction.item_id = is_service[0].pk
                    transaction.quantity = 1
                    transaction_list.append(transaction)
                    calendar_list.append(transaction)
                else:
                    products = PurchasedProduct.objects.filter(transaction_detail=transaction.pk)
                    if products:
                        for product in products:
                            transaction.item_name = product.product.name
                            transaction.item_price = product.product_price
                            transaction.quantity = product.quantity
                            transaction.item_id = product.pk
                            transaction_list.append(transaction)
                            calendar_list.append(transaction)
                
            page = request.GET.get('page', 1)
            paginator = Paginator(transaction_list, 4)
            try:
                paginated_transaction = paginator.page(page)
            except PageNotAnInteger:
                paginated_transaction = paginator.page(1)
            except EmptyPage:
                paginated_transaction = paginator.page(paginator.num_pages)
            return render(request,"user/profile.html",{'page_title': 'Profile', 'user': request.user, 'transactions': paginated_transaction, 'cart_count': cart_count, 'calendar_list':calendar_list})
        else:
            return render('/')


class EditProfileFormView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.phone = request.POST.get('phone')
            user.address = request.POST.get('address')
            if request.POST.get('date_of_birth'):
                dob = request.POST.get('date_of_birth')
                if '/' in dob:
                    dob = dob.split('/')
                    user.date_of_birth = f"{dob[2]}-{dob[0]}-{dob[1]}"
                else:
                    parsed_dob = parse(dob)
                    user.date_of_birth = parsed_dob.strftime('%Y-%m-%d')
            if request.POST.get('profile_image'):
                profile_image =request.POST.get('profile_image').split('\\')[-1]
                user.profile_image=f'profile_image/{profile_image}'
            user.save()
            response = {
                    "message": "Profile updated successfully" ,
                    "status": True
                }
            return JsonResponse(response)
        else:
            return render('/')


class TransactionFilterAjaxView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_count = get_cart_count(request.user)
            month = request.GET.get('month', None)
            year = request.GET.get('year', None)
            print(month, year)
            transactions = TransactionDetail.objects.filter(user=request.user.pk).order_by('-pk')
            if year:
                transactions = transactions.filter(created_at__date__month=month)
            if month:
                transactions = transactions.filter(created_at__date__year=year)
            transaction_list = []
            for transaction in transactions:
                is_service = BookedService.objects.filter(transaction_detail=transaction.pk)
                transaction.item_type = "service" if is_service else "product"
                
                if is_service:
                    if is_service[0].service_type == "Overseas":
                        transaction.item_price = is_service[0].service_charge
                    else:
                        transaction.item_price = is_service[0].booking_charge
                    transaction.item_name = is_service[0].service.name
                    transaction.item_id = is_service[0].pk
                    transaction.quantity = 1
                    transaction_list.append(transaction)
                else:
                    products = PurchasedProduct.objects.filter(transaction_detail=transaction.pk)
                    if products:
                        for product in products:
                            transaction.item_name = product.product.name
                            transaction.item_price = product.product_price
                            transaction.quantity = product.quantity
                            transaction.item_id = product.pk
                            transaction_list.append(transaction)
                
            page = request.GET.get('page', 1)
            paginator = Paginator(transaction_list, 4)
            try:
                paginated_transaction = paginator.page(page)
            except PageNotAnInteger:
                paginated_transaction = paginator.page(1)
            except EmptyPage:
                paginated_transaction = paginator.page(paginator.num_pages)
            return render(request,"user/transaction-filter-ajax.html",{'page_title': 'Profile', 'user': request.user, 'transactions': paginated_transaction, 'cart_count': cart_count})
        else:
            return render(request,"user/profile.html",{'page_title': 'Profile', 'user': request.user, 'transactions': paginated_transaction})