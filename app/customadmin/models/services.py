from django.db import models
from django.utils.translation import gettext as _
from numerology.models import ActivityTracking


class ServiceCategory(ActivityTracking):
    category_name = models.CharField(max_length=200, blank=True, null=True, default='')
    category_description = models.TextField(blank=True, null=True)
    method_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category_name}"

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ["-created_at"]

class CategoryImage(ActivityTracking):
    category_image = models.ImageField(upload_to="categories", null=True,  blank=True)
    service_category = models.ForeignKey("ServiceCategory", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category_image}"
        
    class Meta:
        verbose_name = "CategoryImage"
        verbose_name_plural = "Category Images"
        ordering = ["-created_at"]

class Service(ActivityTracking):
    service_image = models.ImageField(upload_to="services", null=True,  blank=True, verbose_name=_("Service images"))
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    booking_charge = models.FloatField(blank=True, null=True, default=50)
    detail = models.TextField(max_length=255, blank=True, null=True, default='')
    service_category = models.ForeignKey("ServiceCategory", on_delete=models.CASCADE)
    service_charge = models.FloatField(blank=True, null=True)
    related_to = models.ForeignKey('self', blank=True, null=True, related_name='related_service', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["-created_at"]


class TimeSlot(ActivityTracking):
    time_slot = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.time_slot}"

    class Meta:
        verbose_name = "Time Slot"
        verbose_name_plural = "Time Slots"
        ordering = ["-created_at"]
