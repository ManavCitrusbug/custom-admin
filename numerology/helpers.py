from __future__ import print_function

import datetime
from datetime import timedelta
from django.conf import settings
from rest_framework.pagination import PageNumberPagination

from rest_framework import status
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
from customadmin.models import ServiceCart, ProductCart, User


import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle


# Pagination
PAGINATOR = PageNumberPagination()
PAGINATOR.page_size = 10
PAGINATOR_PAGE_SIZE = PAGINATOR.page_size


def get_object(model ,pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None

def custom_response(status_value, code, message, result={}):
    return Response({
                    'status': status_value,
                    'code': code,
                    'message': message,
                    'data': result
                }, status=status.HTTP_200_OK)


def dict_obj_list_to_str(data):
    for key, value in data.items():
        data[key] = "".join(value)
    return data


def get_pagination_response(model_class, request, serializer_class, context):
    result = {}
    model_response = PAGINATOR.paginate_queryset(model_class, request)
    serializer = serializer_class(model_response, many=True, context=context)
    result.update({'data':serializer.data})
    current = PAGINATOR.page.number
    next_page = 0 if PAGINATOR.get_next_link() is None else current + 1
    previous_page = 0 if PAGINATOR.get_previous_link() is None else current - 1
    result.update({'links': {
        'current': current,
        'next': next_page,
        'previous': previous_page,
        'total': PAGINATOR.page.paginator.count,
        'last' : PAGINATOR.page.paginator.num_pages,
    }})
    return result


def serialized_response(serializer, message):
    if serializer.is_valid():
        serializer.save()
        result = serializer.data
        response_status = True
    else:
        result = dict_obj_list_to_str(serializer.errors)
        response_status = False
        message = "Please resolve error(s) OR fill Missing field(s)!"
    return response_status, result, message


def send_email(user, subject, text_content):
    from_email= settings.EMAIL_HOST_USER
    to= user.email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
    return "Mail has been sent successfully"


def get_cart_count(user):
    if not user:
        return 0
    cart_count = 0
    service_in_cart = ServiceCart.objects.filter(user=user.pk)
    if service_in_cart:
        return service_in_cart.count()
    product_in_cart = ProductCart.objects.filter(user=user.pk)
    if product_in_cart:
        count =0
        for product in product_in_cart:
            count += product.quantity
        return count
    return cart_count


credentials = pickle.load(open("numerology/token.pkl", "rb"))

def listEvents():
    service = build('calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    created_event = dict()
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        created_event.update({start:event["summary"]})
    return created_event

def createEvents(service_name, service_date, service_time, name, address, phone, email):
    service = build("calendar", "v3", credentials=credentials)
    result = service.calendarList().list().execute()

    calendar_id = result['items'][0]['id']
    result = service.events().list(calendarId=calendar_id).execute()

    start = datetime.datetime(service_date.year, service_date.month, service_date.day, service_time.hour, service_time.minute, service_time.second)
    end = start + timedelta(hours=1)
    timezone = 'Asia/Kolkata'
    
    description = f"Name: {name} | Phone No: {phone} | Address: {address}"
    
    event = {
    'summary': service_name,
    'description': description,
    'start': {
        'dateTime': start.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': timezone,
    },
    'end': {
        'dateTime': end.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': timezone,
    },
    'attendees': [
        {'email': email}
    ],
    }

    service.events().insert(calendarId='primary', body=event).execute()
