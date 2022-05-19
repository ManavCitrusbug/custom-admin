# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyCreateView,
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyUpdateView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView,
    MyDetailView
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin

from customadmin.forms import ServiceCategoryCreationForm, ServiceCategoryChangeForm, CategoryImageCreationForm, CategoryImageChangeForm
from django.shortcuts import reverse, render

from ..models import ServiceCategory, CategoryImage
from extra_views import InlineFormSetFactory

# -----------------------------------------------------------------------------
# Service Categories
# -----------------------------------------------------------------------------

class ServiceCategoryListView(MyListView):
    """View for Testimonial listing"""

    ordering = ["id"]
    model = ServiceCategory
    queryset = model.objects.all()
    template_name = "customadmin/service-category/service_category_list.html"
    permission_required = ("customadmin.view_service_category",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False)

class ServiceCategoryDetailView(MyDetailView):
    template_name = "customadmin/service-category/service_category_detail.html"
    context = {}

    def get(self, request, pk):
        self.context['servicecategory_detail'] = ServiceCategory.objects.filter(pk=pk).first()
        self.context['category_images'] = CategoryImage.objects.filter(service_category=pk)
        return render(request, self.template_name, self.context)


class ClassCategoryImageInline(InlineFormSetFactory):
    """Inline view to show Image within the Parent View"""

    model = CategoryImage
    form_class = CategoryImageCreationForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}


class ServiceCategoryCreateView(MyNewFormsetCreateView):
    """View to create Service category"""

    model = ServiceCategory
    inline_model = CategoryImage
    inlines = [ClassCategoryImageInline, ]
    form_class = ServiceCategoryCreationForm
    template_name = "customadmin/service-category/service_category_form.html"
    permission_required = ("customadmin.add_service_category",)

    def get_success_url(self):
        return reverse("customadmin:servicecategory-list")

class ClassCategoryImageUpdateInline(InlineFormSetFactory):
    """Inline view to show Image within the Parent View"""

    model = CategoryImage
    form_class = CategoryImageChangeForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class ServicecategoryUpdateView(MyNewFormsetUpdateView):
    """View to update Service category"""

    model = ServiceCategory
    inline_model = CategoryImage
    inlines = [ClassCategoryImageInline, ]
    form_class = ServiceCategoryChangeForm
    template_name = "customadmin/service-category/service_category_form.html"
    permission_required = ("customadmin.change_service_category",)

    def get_success_url(self):
        return reverse("customadmin:servicecategory-list")

class ServiceCategoryDeleteView(MyDeleteView):
    """View to delete Service Category"""

    model = ServiceCategory
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_service_category",)

    def get_success_url(self):
        return reverse("customadmin:servicecategory-list")

class ServiceCategoryAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = ServiceCategory
    queryset = ServiceCategory.objects.all().order_by("created_at")

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