from django.db import models
from django.utils.translation import gettext as _
from numerology.models import ActivityTracking


class InquiryType(ActivityTracking):
    inquiry_type = models.CharField(max_length=200, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.inquiry_type}"

    class Meta:
        verbose_name = "Inquiry Type"
        verbose_name_plural = "Inquiry Types"
        ordering = ["-created_at"]


class Inquiry(ActivityTracking):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    email = models.EmailField(null=True, blank=True, unique=False)
    inquiry_type = models.ForeignKey("InquiryType", on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True, default='')
    note = models.CharField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
        ordering = ["-created_at"]

