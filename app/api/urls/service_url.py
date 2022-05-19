from django.urls import path
from .. import views


urlpatterns = [
    path("service-categories/", views.ServiceCategoryListingAPIView.as_view(), name="service-categories"),
    path("services/", views.ServiceListingAPIView.as_view(), name="services"),
    path("service-detail/<int:pk>/", views.ServiceDetailAPI.as_view(), name="service-detail"),
    path("services-time-slots/", views.ServiceTimeSlotsAPIView.as_view(), name="service-time-slots"),
    path("book-service/", views.ServiceBookingAPIView.as_view(), name="book-service"),
    path("package-listing/", views.PackageListingAPIView.as_view(), name="package-listing"),
]