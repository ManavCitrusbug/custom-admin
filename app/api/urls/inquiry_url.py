from django.urls import path
from .. import views

urlpatterns = [
    path("contact/", views.InquiryAPIView.as_view(), name="contact"),
    path("inquiry-types/", views.InquirycategoryListing.as_view(), name="inquiry-types"),
]