# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import FoundationCodeCreationForm, FoundationCodeChangeForm
from django.shortcuts import reverse

from ..models import FoundationCode

# -----------------------------------------------------------------------------
# FoundationCode
# -----------------------------------------------------------------------------

class FoundationCodeListView(MyListView):
    """View for FoundationCode listing"""

    ordering = ["id"]
    model = FoundationCode
    queryset = model.objects.all()
    template_name = "customadmin/foundation-code/foundation_code_list.html"
    permission_required = ("customadmin.view_foundation_code",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)

class FoundationCodeCreateView(MyCreateView):
    """View to create FoundationCode"""

    model = FoundationCode
    form_class = FoundationCodeCreationForm
    template_name = "customadmin/foundation-code/foundation_code_form.html"
    permission_required = ("customadmin.add_foundation_code",)

    def get_success_url(self):
        return reverse("customadmin:foundationcode-list")

class FoundationCodeUpdateView(MyUpdateView):
    """View to update FoundationCode"""

    model = FoundationCode
    form_class = FoundationCodeChangeForm
    template_name = "customadmin/foundation-code/foundation_code_form.html"
    permission_required = ("customadmin.change_foundation_code",)

    def get_success_url(self):
        return reverse("customadmin:foundationcode-list")

class FoundationCodeDeleteView(MyDeleteView):
    """View to delete FoundationCode"""

    model = FoundationCode
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_foundation_code",)

    def get_success_url(self):
        return reverse("customadmin:foundationcode-list")

class FoundationCodeAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = FoundationCode
    queryset = FoundationCode.objects.all().order_by("created_at")

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