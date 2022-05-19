import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext as _
from numerology.models import ActivityTracking
# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have a valid email address.")

        if not kwargs.get("username"):
            raise ValueError("Users must have a valid username.")

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get("username")
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=True, blank=True, unique=True)
    username = models.CharField(max_length=40, blank=True, null=True,default='')
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    profile_image = models.ImageField(upload_to="profile_image", default="../static/assets/images/profile.jpg", null=True,  blank=True, verbose_name=_("Profile Image"))
    customer_id = models.CharField(_("Customer Id"), blank=True, max_length=255)
    language = models.CharField(max_length=40, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_("Unique Id"),)
    otp_expired_at = models.DateTimeField(blank=True, null=True)
    otp = models.CharField(max_length=5, blank=True, null=True)
    password_reset_link = models.UUIDField(unique=True, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    device = models.CharField(max_length=200, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.email) if self.email else str(self.device)

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return " ".join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("customadmin:user-list")



class PurchasedProduct(ActivityTracking):
    product = models.ForeignKey("ShopProduct", on_delete=models.CASCADE)
    product_price = models.FloatField(blank=True, null=True) 
    quantity = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    total_amount = models.FloatField(blank=True, null=True)
    transaction_detail = models.ForeignKey("TransactionDetail", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Purchased Product"
        verbose_name_plural = "Purchased Products"
        ordering = ["-created_at"]


class BookedService(ActivityTracking):
    SERVICE_CHOICE = (
        ('Local', 'Local'),
        ('Overseas', 'Overseas'),
    )
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    booking_charge = models.FloatField(blank=True, null=True, default=50)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    service_date = models.DateField(blank=True, null=True)
    service_time = models.TimeField(blank=True, null=True)
    service_type = models.CharField(max_length=100, blank=True, null=True, default='', choices = SERVICE_CHOICE)
    transaction_detail = models.ForeignKey("TransactionDetail", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Booked Service"
        verbose_name_plural = "Booked Services"
        ordering = ["-created_at"]