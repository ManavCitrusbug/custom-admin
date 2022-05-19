from django.shortcuts import render, redirect
from django.views import View
from customadmin.models import Testimonial, InquiryType, Inquiry, User, Service, TimeSlot, ProductCart, ServiceCart, ServiceCategory
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.conf import settings
import uuid
from numerology.helpers import send_email, get_cart_count


def format_time(hour):
    if len(hour)<2:
        hour = f"0{hour}"
    return hour

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            # cookie_exists = request.COOKIES.get('device', None)
            # if not cookie_exists:
                # device = uuid.uuid4()
                # request.set_cookie('device', device)
            device = uuid.uuid4()
            # device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        testimonials = Testimonial.objects.filter(active=True)
        time_slots = TimeSlot.objects.filter(active=True)
        available_time = [f"{format_time(str(time_slot.time_slot.hour))}:{format_time(str(time_slot.time_slot.minute))}" for time_slot in time_slots]
        service_category = ServiceCategory.objects.all()
        services = Service.objects.filter(active=True)
        return render(request,"user/index.html",{'testimonials': testimonials, 'page_title': 'Home' , 'TEST_VARIABLE':settings.TEST_VARIABLE, 'time_slots': available_time, 'cart_count': cart_count, 'services': services, 'service_category': service_category})


class AboutPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        return render(request,"user/about.html",{ 'page_title': 'About Me', 'cart_count': cart_count})


class PrivacyPolicyView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        return render(request,"user/privacy-policy.html",{ 'page_title': 'PrivacyPolicy', 'cart_count': cart_count})


class TermsAndConditionsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        return render(request,"user/terms-and-conditions.html",{ 'page_title': 'Terms and Conditions', 'cart_count': cart_count})


class ContactPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        inquiry_types = InquiryType.objects.filter(active=True)
        return render(request,"user/contact.html",{'inquiry_types': inquiry_types,
                                                    'page_title': 'Contact', 'cart_count': cart_count})


class SubmitContactFormView(View):
    def post(self, request):
        inquiry_type = request.POST.get('inquiry_type')
        if inquiry_type:
            get_inquiry = InquiryType.objects.filter(inquiry_type=inquiry_type)
            inquiry_type =get_inquiry[0] if get_inquiry else ""
            
        Inquiry.objects.create(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            inquiry_type = inquiry_type,
            phone = request.POST.get('phone'),
            note = request.POST.get('note'),
        )
        response = {
                "message": "Inquiry sent successfully" ,
                "status": True
            }
        return JsonResponse(response)


class SignUpPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        return render(request,"user/sign-up.html",{'page_title': 'Sign Up', 'cart_count': cart_count})


class RegisterView(View):
    def post(self, request):
        email = request.POST.get('email')
        email_exists = User.objects.filter(email=email)
        if email_exists:
            response = {
                "message": "Email already exits." ,
                "status": False
            }
            return JsonResponse(response)
        password = request.POST.get('password')
        user = User()
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.set_password(password)
        user.email_verified = False
        user.save()

        subject= "[EzierCode] Email verification"
        text_content = f"Hello, \nPlease click the below link to verify your email. \n {settings.EMAIL_VERIFICATION_LINK}{user.unique_id}/"
        send_email(user, subject, text_content)
        response = {
                "message": "Verify your email to continue." ,
                "status": True
            }
        return JsonResponse(response)


class LoginPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        return render(request,"user/login.html",{'page_title': 'Login', 'cart_count': cart_count})


class UserLoginView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        service_in_cart = ServiceCart.objects.filter(user=user.pk)
        product_in_cart = ProductCart.objects.filter(user=user.pk)

        dummy_user = user
        email =  request.POST.get('email')
        password =  request.POST.get('password')
        if not email:
            return JsonResponse({'message': 'Email is required.'})

        user = User.objects.filter(email=email).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')

        if user.exists() and user.count() ==1:
            user_obj=user.first()
        else:
            response = {
                "message": 'Email not found.',
                "status": False,
                "send_link": False
            }
            return JsonResponse(response)

        if user_obj and not user_obj.check_password(password):
            response = {
                "message": 'Invalid password.',
                "status": False,
                "send_link": False
            }
            return JsonResponse(response)

        if not user_obj.email_verified:
            response = {
                "message": 'Email not verified.',
                "status": False,
                "send_link": True
            }
            return JsonResponse(response)
        login(request,user_obj, backend='django.contrib.auth.backends.ModelBackend')
        
        service_exists = ServiceCart.objects.filter(user=user_obj.pk)
        if not service_exists:
            if product_in_cart:
                for obj in product_in_cart:
                    ProductCart.objects.create(user=user_obj, product=obj.product, quantity=obj.quantity)
            elif service_in_cart:
                product_exists = ProductCart.objects.filter(user=user_obj.pk)
                if not product_exists:
                    obj = service_in_cart.first()
                    ServiceCart.objects.create(user=user_obj, service=obj.service, service_date=obj.service_date, service_time=obj.service_time)
        dummy_user.delete()
        response = {
                "message": "Login Successfull" ,
                "status": True
            }
        return JsonResponse(response)


def logout_view(request):
    logout(request)
    return redirect('/')


class ForgotPasswordPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        return render(request,"user/forgot-password.html",{ 'page_title': 'Forgot Password', 'cart_count': cart_count})


class SendChangePasswordLinkView(View):
    def post(self, request):
        email = request.POST.get('email')
        if not email:
            response = {
                "message": "Email is required!" ,
                "status": False
            }
            return JsonResponse(response)

        user_exists = User.objects.filter(is_active=True, email=email)
        if user_exists:
            user_exists[0].password_reset_link = uuid.uuid4()
            user_exists[0].save()
            subject= "[EzierCode] Request to change Password"
            text_content = f"Hello, \nYou recently requested to reset your password for your EzierCode account. Please click the below link to change your password. \n {settings.RESET_PASSWORD_LINK}{user_exists[0].password_reset_link}/"
            email_response = send_email(user_exists[0], subject, text_content)     
            response = {
                    "message": email_response ,
                    "status": True
                }
            return JsonResponse(response)
        response = {
                    "message": "Email not found!" ,
                    "status": False
                }
        return JsonResponse(response)


class ResetPasswordPageView(View):
    def get(self, request, uuid):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        return render(request,"user/reset-password.html",{ 'page_title': 'Reset Password', 'cart_count': cart_count})


class ChangePasswordView(View):
    def post(self, request):
        password = request.POST.get('password')
        uuid_link = request.POST.get('uuid_link')

        if not uuid_link:
            response = {
                "message": "Invalid Link!" ,
                "status": False
            }
            return JsonResponse(response)

        user_exists = User.objects.filter(is_active=True, password_reset_link=uuid_link)
        if user_exists:
            user_exists[0].set_password(password)
            user_exists[0].password_reset_link = None
            user_exists[0].save()  
            response = {
                    "message": "Password Updated!" ,
                    "status": True
                }
            return JsonResponse(response)
        response = {
                    "message": "Invalid Link!" ,
                    "status": False
                }
        return JsonResponse(response)


class EmailverificationView(View):
    def get(self, request, uuid):
        try:
            user = User.objects.filter(unique_id=uuid)
            if not user:
                return render(request,"user/verify-email.html",{ 'page_title': 'Email Verification', 'status': False})
            if user[0].email_verified:
                return redirect('/')
            user[0].email_verified=True
            user[0].save()
            return render(request,"user/verify-email.html",{ 'page_title': 'Email Verification', 'status': True})
        except:
            return render(request,"user/verify-email.html",{ 'page_title': 'Email Verification', 'status': False})


class EmailVerificationPage(View):
    def get(self, request):
        return render(request,"user/email-verification-page.html",{'page_title': 'Email Verification', 'cart_count': 0})


class SendEmailVerificationLinkView(View):
    def post(self, request):
        email = request.POST.get('email')
        if not email:
            response = {
                "message": "Email is required!" ,
                "status": False
            }
            return JsonResponse(response)

        user_exists = User.objects.filter(is_active=True, email=email)
        if user_exists:
            user = user_exists.first()
            if user_exists[0].email_verified:
                response = {
                        "message": "Email already verified",
                        "status": False
                    }
                return JsonResponse(response)
            subject= "[EzierCode] Email verification"
            text_content = f"Hello, \nPlease click the below link to verify your email. \n {settings.EMAIL_VERIFICATION_LINK}{user.unique_id}/"
            email_response = send_email(user, subject, text_content)  
            response = {
                    "message": email_response ,
                    "status": True
                }
            return JsonResponse(response)
        response = {
                    "message": "Email not found!" ,
                    "status": False
                }
        return JsonResponse(response)