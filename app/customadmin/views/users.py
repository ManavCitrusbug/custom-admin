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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import TemplateView, DetailView
from django_datatables_too.mixins import DataTableMixin

from ..forms import UserChangeForm, UserCreationForm
from django.shortcuts import reverse, render

from customadmin.models import User, PurchasedProduct, BookedService

import csv

# Export CSV FILE

def export_user_csv(request):

    output = []
    response = HttpResponse (content_type='text/csv')
    filename = u"User.csv"
    response['Content-Disposition'] = u'attachment; filename="{0}"'.format(filename)

    writer = csv.writer(response)
    query_set = User.objects.all()

    #Header
    writer.writerow(['Name', "Username",'Bio', 'Email', 'Status','Phone','User Type',"is_staff", "is_superuser","avatar","company"])
    for user in query_set:
        if user.groups.all():
            gp = user.groups.all()[0].name
        else:
            gp = None

        if not user.profile_image:
            avatar = None
        else:
            avatar = user.profile_image.url


        output.append([user.first_name, user.last_name, user.username, user.email, user.is_active,gp,user.is_staff, user.is_superuser, request.build_absolute_uri(avatar),])
    #CSV Data
    writer.writerows(output)
    return response

class UserDetailView(MyDetailView):
    template_name = "customadmin/adminuser/user_detail.html"
    context = {}

    def get(self, request, pk):
        self.context['user_detail'] = User.objects.filter(pk=pk).first()
        self.context['purchased_products'] = PurchasedProduct.objects.filter(user=pk)
        self.context['booked_services'] = BookedService.objects.filter(user=pk)
        return render(request, self.template_name, self.context)



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "customadmin/index.html"
    context = {}

    def get(self, request):
        self.context['user_count']=User.objects.all().exclude(is_staff=True).count()
        return render(request, self.template_name, self.context)

# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------


class UserListView(MyListView):
    """View for User listing"""

    # paginate_by = 25
    ordering = ["id"]
    model = User
    queryset = model.objects.exclude(is_staff=True)
    template_name = "customadmin/adminuser/user_list.html"
    permission_required = ("customadmin.view_user",)

    def get_queryset(self):
        return self.model.objects.exclude(is_staff=True).exclude(email=self.request.user).exclude(email=None)


class UserCreateView(MyCreateView):
    """View to create User"""

    model = User
    form_class = UserCreationForm
    template_name = "customadmin/adminuser/user_form.html"
    permission_required = ("customadmin.add_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:user-list")

class UserUpdateView(MyUpdateView):
    """View to update User"""

    model = User
    form_class = UserChangeForm
    template_name = "customadmin/adminuser/user_form_update.html"
    permission_required = ("customadmin.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:user-list")

class UserDeleteView(MyDeleteView):
    """View to delete User"""

    model = User
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_user",)

    def get_success_url(self):
        # opts = self.model._meta
        return reverse("customadmin:user-list")

class UserPasswordView(MyUpdateView):
    """View to change User Password"""
    
    model = User
    form_class = AdminPasswordChangeForm
    template_name = "customadmin/adminuser/password_change_form.html"
    permission_required = ("customadmin.change_user",)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        kwargs["user"] = kwargs.pop("instance")
        return kwargs

    def get_success_url(self):
        opts = self.model._meta
        return reverse("customadmin:user-list")

class UserAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = User
    queryset = User.objects.all().order_by("last_name")

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

    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""


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