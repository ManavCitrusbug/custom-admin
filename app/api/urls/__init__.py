# -*- coding: utf-8 -*-
from django.urls import include, path
from . import auth_url, testimonial_url, inquiry_url, product_url, service_url, plot_chart_url, cart_url, transaction_url

app_name="user"

urlpatterns = [
    path("", include(auth_url)),
    path("", include(testimonial_url)),
    path("", include(inquiry_url)),
    path("", include(product_url)),
    path("", include(service_url)),
    path("", include(plot_chart_url)),
    path("", include(cart_url)),
    path("", include(transaction_url)),
]