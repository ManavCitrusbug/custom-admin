from django.urls import path
from .. import views


urlpatterns = [
    path("testimonials/", views.TestimonialsListingAPIView.as_view(), name="testimonials"),
]