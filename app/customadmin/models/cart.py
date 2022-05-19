from django.db import models
from django.utils.translation import gettext as _
from numerology.models import ActivityTracking


class ProductCart(ActivityTracking):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey("customadmin.ShopProduct", on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Product Cart"
        verbose_name_plural = "Product Cart"
        ordering = ["-created_at"]


class ServiceCart(ActivityTracking):
    SERVICE_CHOICE = (
        ('Local', 'Local'),
        ('Overseas', 'Overseas'),
    )

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    service = models.ForeignKey("customadmin.Service", on_delete=models.CASCADE)
    service_date = models.DateField(blank=True, null=True)
    service_time = models.TimeField(blank=True, null=True)
    service_type = models.CharField(max_length=100, blank=True, null=True, default='', choices = SERVICE_CHOICE)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Service Cart"
        verbose_name_plural = "Service Cart"
        ordering = ["-created_at"]