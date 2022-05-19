from django.urls import path
from .. import views

urlpatterns = [
    path("product-cart/", views.ProductCartAPIView.as_view(), name="add-product-cart"),
    path("service-cart/", views.ServiceCartAPIView.as_view(), name="add-service-cart"),
    path("shopping-cart/", views.ShoppingCartAPIView.as_view(), name="shopping-cart"),
]