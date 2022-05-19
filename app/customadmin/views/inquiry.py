# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyDetailView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import InquiryCreationForm, InquiryChangeForm, InquiryTypeCreationForm, InquiryTypeChangeForm
from django.shortcuts import reverse, render

from ..models import Inquiry , InquiryType
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory

from django.contrib import messages

MSG_CREATED = '"{}" created successfully.'
MSG_UPDATED = '"{}" updated successfully.'
MSG_DELETED = '"{}" deleted successfully.'
MSG_CANCELED = '"{}" canceled successfully.'

# -----------------------------------------------------------------------------
# Inquiry
# -----------------------------------------------------------------------------

class InquiryDetailView(MyDetailView):
    model = Inquiry
    template_name = "customadmin/inquiry/inquiry_detail.html"
    permission_required = ("customadmin.view_inquiry_detail",)
    context = {}

    def get(self, request, pk):
        self.context['inquiry'] = pk
        self.context['inquiry_detail'] = Inquiry.objects.filter(pk=pk).first()
        return render(request, self.template_name, self.context)

class InquiryListView(MyListView):
    """View for Inquiry listing"""

    ordering = ["id"]
    model = Inquiry
    queryset = model.objects.all()
    template_name = "customadmin/inquiry/inquiry_list.html"
    permission_required = ("customadmin.view_inquiry",)

    def get_queryset(self):
        return self.model.objects.all()

class InquiryTypeInline(InlineFormSetFactory):
    """Inline view to show Cover within the Parent View"""

    model = InquiryType
    form_class = InquiryTypeCreationForm
    factory_kwargs = {'extra': 1, 'max_num': 1, 'can_order': False, 'can_delete': True}

class InquiryCreateView(MyNewFormsetCreateView):
    """View to create Inquiry"""

    model = Inquiry
    inline_model = InquiryType
    inlines = [InquiryTypeInline, ]
    form_class = InquiryCreationForm
    template_name = "customadmin/inquiry/inquiry_form.html"
    permission_required = ("customadmin.add_inquiry",)

    def get_success_url(self):
        messages.success(self.request, MSG_CREATED.format(self.object))
        return reverse("customadmin:inquiry-list")

class InquiryTypeUpdateInline(InlineFormSetFactory):
    """View to update Cover which is a inline view"""

    model = InquiryType
    form_class = InquiryTypeChangeForm
    factory_kwargs = {'extra': 1, 'max_num': 1, 'can_order': False, 'can_delete': True}

class InquiryUpdateView(MyNewFormsetUpdateView):
    """View to update Inquiry"""

    model = Inquiry
    inline_model = InquiryType
    inlines = [InquiryTypeInline, ]
    form_class = InquiryChangeForm
    template_name = "customadmin/inquiry/inquiry_form.html"
    permission_required = ("customadmin.change_inquiry",)

    def get_success_url(self):
        messages.success(self.request, MSG_UPDATED.format(self.object))
        return reverse("customadmin:inquiry-list")

class InquiryDeleteView(MyDeleteView):
    """View to delete inquiry"""

    model = Inquiry
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_inquiry",)

    def get_success_url(self):
        return reverse("customadmin:inquiry-list")

class InquiryAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = Inquiry
    queryset = Inquiry.objects.all().order_by("created_at")

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