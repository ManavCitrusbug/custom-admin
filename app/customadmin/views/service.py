# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyDetailView,
    MyLoginRequiredView,
    MyUpdateView,
)
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import ServiceCreationForm, ServiceChangeForm
from django.shortcuts import reverse, render
from ..models import Service


class ServiceDetailView(MyDetailView):
    model = Service
    template_name = "customadmin/service/service_detail.html"
    permission_required = ("customadmin.view_service_detail",)
    context = {}

    def get(self, request, pk):
        self.context['service_detail'] = Service.objects.filter(pk=pk).first()
        self.context['service_image_url'] = request.build_absolute_uri(self.context['service_detail'].service_image)
        self.context['service_image_url'] = self.context['service_image_url'][:22] + 'media' + self.context['service_image_url'][51:]
        return render(request, self.template_name, self.context)

class ServiceListView(MyListView):
    """View for Service listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = Service
    queryset = model.objects.all()
    template_name = "customadmin/service/service_list.html"
    permission_required = ("customadmin.view_service",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)

class ServiceCreateView(MyCreateView):
    """View to create Service"""

    model = Service

    form_class = ServiceCreationForm
    template_name = "customadmin/service/service_form.html"
    permission_required = ("customadmin.add_service",)

    def get_success_url(self):
        return reverse("customadmin:service-list")

class ServiceUpdateView(MyUpdateView):
    """View to update Service"""

    model = Service
    form_class = ServiceChangeForm
    template_name = "customadmin/service/service_form.html"
    permission_required = ("customadmin.change_service",)

    def get_success_url(self):
        return reverse("customadmin:service-list")

class ServiceDeleteView(MyDeleteView):
    """View to delete Service"""

    model = Service
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_service",)

    def get_success_url(self):
        return reverse("customadmin:service-list")


class ServiceAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = Service
    queryset = Service.objects.all().order_by("created_at")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("customadmin/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def _get_actions(self, obj, **kwargs):
        """Get actions column markup."""
        # ctx = super().get_context_data(**kwargs)
        t = get_template("customadmin/partials/list_basic_actions.html")
        # ctx.update({"obj": obj})
        # print(ctx)
        return t.render({"o": obj})

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(username__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                # | Q(state__icontains=self.search)
                # | Q(year__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "username": o.username,
                    "first_name": o.first_name,
                    "last_name": o.last_name,
                    "is_superuser": self._get_is_superuser(o),
                    # "modified": o.modified.strftime("%b. %d, %Y, %I:%M %p"),
                    "actions": self._get_actions(o),
                }
            )
        return data