from django.urls import path
from .. import views

urlpatterns = [
    path("service-cart/", views.AddServiceToCartView.as_view(), name="service-cart"),
    path("booking/", views.BookingPage.as_view(), name="booking"),
    path("cart-page/", views.CartPage.as_view(), name="cart-page"),
    path("remove-service/<int:pk>", views.RemoveServiceFromCart.as_view(), name="remove-service"),
    path("add-product/", views.AddProductToCartView.as_view(), name="add-product"),
    path("remove-product/<int:pk>", views.RemoveProductFromCart.as_view(), name="remove-product"),
    path("payment-success/", views.PaymentSuccessPage.as_view(), name="payment-success"),
]