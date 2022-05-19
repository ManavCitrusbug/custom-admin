from django.urls import path
from .. import views


urlpatterns = [
    path("transactions/", views.TransactionListingAPIView.as_view(), name="transactions"),
    path("transaction-detail/<int:pk>/", views.TransactionDetailAPIView.as_view(), name="transaction-detail"),
]