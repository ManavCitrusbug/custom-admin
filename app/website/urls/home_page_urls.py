from django.urls import path
from .. import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("privacy-policy/", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("terms-and-conditions/", views.TermsAndConditionsView.as_view(), name="terms-and-conditions"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
    path("submit-contact-form/", views.SubmitContactFormView.as_view(), name="submit-contact-form"),
    path("sign-up/", views.SignUpPageView.as_view(), name="sign-up"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("user-login/", views.UserLoginView.as_view(), name="user-login"),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.ForgotPasswordPageView.as_view(), name="forgot-password"),
    path('forgot-password-link/', views.SendChangePasswordLinkView.as_view(), name="forgot-password-link"),
    path('reset-password/<str:uuid>/', views.ResetPasswordPageView.as_view(), name="reset-password"),
    path('change-password/', views.ChangePasswordView.as_view(), name="change-password"),
    path('email-verification/<str:uuid>/', views.EmailverificationView.as_view(), name="email-verification"),
    path('email-verification-page/', views.EmailVerificationPage.as_view(), name="email-verification-page"),
    path('send-email-verification-link/', views.SendEmailVerificationLinkView.as_view(), name="send-email-verification-link"),
]