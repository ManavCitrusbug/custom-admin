from django.urls import path
from .. import views

urlpatterns = [
    path("shop/", views.ShopPageView.as_view(), name="shop"),
    path("services/<int:pk>/", views.ServicePageView.as_view(), name="services"),
    path("services-category", views.ServiceCategoryPageView.as_view(), name="services-category"),
    path("service-details/<int:pk>/", views.ServiceDetailPageView.as_view(), name="service-details"),
    path("purchase-product/", views.PurchaseProductView.as_view(), name="purchase-product"),
    path("book-service/", views.ServiceBookingView.as_view(), name="book-service"),

]