from rest_framework.views import APIView
from ..serializers import UserRegisterSerializer, UserLoginSerializer
from numerology.helpers import custom_response, serialized_response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from numerology.permissions import IsAccountOwner
from customadmin.models import User
from numerology.helpers import get_object
import math
import datetime
import random
import pytz
utc = pytz.UTC


class SignUpApiView(APIView):
    """
    User Sign up view
    """
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        if 'email' in request.data:
            email_check = User.objects.filter(email=request.data['email']).distinct()
            if email_check.exists():
                message = "Email already exists!"
                return custom_response(True, status.HTTP_400_BAD_REQUEST, message)
            message = "Account created successfully!"
            serializer = self.serializer_class(data=request.data, context={'request': request})
            response_status, result, message = serialized_response(serializer, message)
            status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
            # TODO Email
            return custom_response(response_status, status_code, message, result)
        else:
            return custom_response(False, status.HTTP_400_BAD_REQUEST, "Email is required")



class LoginAPIView(APIView):
    """
    User Login View
    """
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        account = authenticate(email=email, password=password)
        
        if account is not None:
            login(request, account)
            serializer = self.serializer_class(account, context={'request':request})
            return custom_response(True, status.HTTP_200_OK, "Login Successful!", serializer.data)
        else:
            message = "Email/password combination invalid"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class LogoutAPIView(APIView):
    """
    User Logout View
    """
    permission_classes = (IsAccountOwner,)

    def post(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        message = "Logout successful!"
        return custom_response(True, status.HTTP_200_OK, message)



class UserProfileAPI(APIView):
    """
    User Profile view
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (IsAccountOwner,)

    def put(self, request, *args, **kwargs):
        user_profile = get_object(User, request.user.pk)
        if not user_profile:
            message = "User not found!"
            return custom_response(True, status.HTTP_200_OK, message)
        message = "User Profile updated successfully!"
        serializer = self.serializer_class(user_profile, data=request.data, partial=True, context={"request": request})
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201_CREATED if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)

    def get(self, request):
        user_profile = get_object(User, request.user.pk)
        if not user_profile:
            message = "Requested account details not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        serializer = self.serializer_class(user_profile, context={"request": request})
        message = "User Profile fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)



class ForgotPasswordAPIView(APIView):
    """
    Send password reset OTP to email
    """
    def post(self, request, format=None):
        if "email" not in request.data.keys():
            message = "Email field is missing!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            user = None
        if not user:
            message = "User not found!"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        if user:
                digits = "0123456789"
                OTP = "" 
                for i in range(4) : 
                    OTP += digits[math.floor(random.random() * 10)]

                user.otp_expired_at = datetime.datetime.now() + datetime.timedelta(days=1)
                user.unique_id = user.unique_id
                user.otp = OTP
                user.save()
                #TODO send email
        message = "Email with OTP to change password sent successfully!"                
        return custom_response(True, status.HTTP_200_OK, message)


class SetPasswordAPIView(APIView):
    """
    Set password view
    """
    def post(self, request, format=None):
        if "password" not in request.data:
            message = "Password field is missing!"
        if "otp" not in request.data:
            message = "OTP field is missing!"
        else:
            user = User.objects.filter(otp=request.data["otp"]).first()
            print(user)
            if user:
                today = datetime.datetime.utcnow()
                today = utc.localize(today)
                today = today.replace(tzinfo=utc)
                if today >  user.otp_expired_at:
                    message = "OTP has been expired."
                    return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
                user.set_password(request.data["password"])
                user.otp=None
                user.save()
                message = "Password Changed Successfully!"
                return custom_response(True, status.HTTP_200_OK, message)
        message = "Invalid OTP!"
        return custom_response(False, status.HTTP_400_BAD_REQUEST, message)



