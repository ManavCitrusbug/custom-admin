from django.urls import path
from .. import views


urlpatterns = [
    path("products/", views.ProductsListingAPIView.as_view(), name="products"),
    path("purchase-products/", views.PurchaseProductAPIView.as_view(), name="purchase-products"),
]