# -*- coding: utf-8 -*-
from django.urls import include, path
from . import home_page_urls, product_page_urls, personal_details_url, free_chart_urls, cart_page_urls


urlpatterns = [
    path("", include(home_page_urls)),
    path("", include(product_page_urls)),
    path("", include(personal_details_url)),
    path("", include(free_chart_urls)),
    path("", include(cart_page_urls)),

]