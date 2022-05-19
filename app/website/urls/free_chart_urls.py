from django.urls import path
from .. import views

urlpatterns = [
    path("free-charts/", views.FreeChartPageView.as_view(), name="free-charts"),
    path("phone-number-chart/", views.PhoneNumberChartView.as_view(), name="phone-number-chart"),
    
    path("personal-chart-tab/", views.PersonalChartTabPage.as_view(), name="personal-chart-tab"),
    path("personal-chart/", views.PersonalChartView.as_view(), name="personal-chart"),
]