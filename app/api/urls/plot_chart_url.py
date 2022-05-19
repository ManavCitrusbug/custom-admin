from django.urls import path
from .. import views


urlpatterns = [
    path("phone-number-chart/", views.PhoneNumberChartAPIView.as_view(), name="phone-number-chart"),
    path("personal-detail-chart/", views.PersonalDetailChartAPIView.as_view(), name="personal-detail-chart"),
]