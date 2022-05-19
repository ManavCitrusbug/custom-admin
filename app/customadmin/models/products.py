from django.db import models
from django.utils.translation import gettext as _
from numerology.models import ActivityTracking


class ShopProduct(ActivityTracking):
    product_image = models.ImageField(upload_to="products", null=True,  blank=True, verbose_name=_("Product images"))
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    price = models.FloatField(blank=True, null=True)
    detail = models.TextField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Shop Product"
        verbose_name_plural = "Shop Products"
        ordering = ["-created_at"]
