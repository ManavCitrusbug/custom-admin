from django.urls import path
from .. import views
from django.views.generic import TemplateView


urlpatterns = [
    path("register/", views.SignUpApiView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),    
    path("profile/", views.UserProfileAPI.as_view(), name="logout"),
    path("forgot-password/", views.ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("set-password/", views.SetPasswordAPIView.as_view(), name="set-password"),
    path("about/", TemplateView.as_view(template_name="static-pages/about-page.html"), name="about"),
    path("privacy-policy/", TemplateView.as_view(template_name="static-pages/privacy-policy-page.html"), name="privacy-policy"),
    path("terms-and-conditions/", TemplateView.as_view(template_name="static-pages/terms-and-condition-page.html"), name="terms-and-conditions"),
    path("home-page/", TemplateView.as_view(template_name="static-pages/home-page.html"), name="home-page"),
]


