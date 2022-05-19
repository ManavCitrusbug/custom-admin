from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import (User,
    Testimonial,
    InquiryType,
    Inquiry,
    ShopProduct, Service, ServiceCategory, UserPhoneNumber,
    PhoneNumberCode, ProductCart, ServiceCart, PersonalChart,
    PurchasedProduct, TransactionDetail, TimeSlot, BookedService,
    NumberCode, FamilyCode, SocialCode, FoundationCode, OtherCode, CategoryImage,
)
from .forms import AccountUpdateForm, AccountCreationForm
from django.utils.translation import ugettext_lazy as _


class UserAdmin(UserAdmin):
    form = AccountUpdateForm
    add_form = AccountCreationForm

    list_per_page = 10
    list_display = ["pk", "email", "username",]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "profile_image",
                    "date_of_birth",
                    "language",
                    "customer_id",
                    "address",
                    "otp",
                    "otp_expired_at",
                    "phone",
                    "email_verified",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "profile_image",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save()
        return instance


class TestimonialAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class InquiryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class InquiryTypeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class ShopProductAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class ServiceAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class UserPhoneNumberAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class PhoneNumberCodeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "code"]


class ProductCartAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class ServiceCartAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class PersonalChartAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class PurchasedProductAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class TransactionDetailAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class TimeSlotAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class BookedServiceAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk"]


class NumberCodeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "code", "meaning"]


class OtherCodeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "code", "meaning"]

class CategoryImageAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ["pk", "category_image"]

admin.site.register(User, UserAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(InquiryType, InquiryTypeAdmin)
admin.site.register(ShopProduct, ShopProductAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(UserPhoneNumber, UserPhoneNumberAdmin)
admin.site.register(PhoneNumberCode, PhoneNumberCodeAdmin)
admin.site.register(ProductCart, ProductCartAdmin)
admin.site.register(ServiceCart, ServiceCartAdmin)
admin.site.register(PersonalChart, PersonalChartAdmin)
admin.site.register(PurchasedProduct, PurchasedProductAdmin)
admin.site.register(TransactionDetail, TransactionDetailAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(BookedService, BookedServiceAdmin)
admin.site.register(NumberCode, NumberCodeAdmin)
admin.site.register(FamilyCode)
admin.site.register(FoundationCode)
admin.site.register(SocialCode)
admin.site.register(OtherCode, OtherCodeAdmin)
admin.site.register(CategoryImage, CategoryImageAdmin)