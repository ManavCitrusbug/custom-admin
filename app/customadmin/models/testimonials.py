from django.db import models
from django.utils.translation import gettext as _
from numerology.models import ActivityTracking


class Testimonial(ActivityTracking):
    logo = models.ImageField(upload_to="testimonials", null=True,  blank=True, verbose_name=_("testimonial logo"))
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    testimonial_text = models.TextField(max_length=500, blank=True, null=True, default='')
    designation = models.CharField(max_length=200, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["-created_at"]
