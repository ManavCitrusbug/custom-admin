from django.urls import path
from .. import views

urlpatterns = [
    path("profile/", views.ProfilePageView.as_view(), name="profile"),
    path("edit-profile-form/", views.EditProfileFormView.as_view(), name="edit-profile-form"),
    path("transaction-filter/", views.TransactionFilterAjaxView.as_view(), name="transaction-filter"),
]