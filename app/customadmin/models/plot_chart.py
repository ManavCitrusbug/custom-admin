from django.db import models
from django.utils.translation import gettext as _
from numerology.models import ActivityTracking


class PhoneNumberCode(ActivityTracking):
    code = models.CharField(max_length=2, blank=True, null=True, unique=True)
    code_text = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Phone Number Code"
        verbose_name_plural = "Phone Number Codes"
        ordering = ["-created_at"]


class UserPhoneNumber(ActivityTracking):
    phone = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.phone}"

    class Meta:
        verbose_name = "User Phone Numer"
        verbose_name_plural = "User Phone Numers"
        ordering = ["-created_at"]


class PersonalChart(ActivityTracking):
    name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True, default='')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Personal chart Detail"
        verbose_name_plural = "Personal chart Detail"
        ordering = ["-created_at"]


class NumberCode(ActivityTracking):
    code =models.CharField(max_length=1, blank=True, null=True)
    meaning =models.TextField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Number Code"
        verbose_name_plural = "Number Codes"
        ordering = ["-created_at"]


class FoundationCode(ActivityTracking):
    code =models.CharField(max_length=4, blank=True, null=True)
    meaning =models.TextField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Foundation Code"
        verbose_name_plural = "Foundation Codes"
        ordering = ["-created_at"]


class SocialCode(ActivityTracking):
    code =models.CharField(max_length=4, blank=True, null=True)
    meaning =models.TextField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Social Code"
        verbose_name_plural = "Social Codes"
        ordering = ["-created_at"]


class FamilyCode(ActivityTracking):
    code =models.CharField(max_length=4, blank=True, null=True)
    meaning =models.TextField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Family Code"
        verbose_name_plural = "Family Codes"
        ordering = ["-created_at"]


class OtherCode(ActivityTracking):
    code =models.CharField(max_length=4, blank=True, null=True)
    meaning =models.TextField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = "Other Code"
        verbose_name_plural = "Other Codes"
        ordering = ["-created_at"]