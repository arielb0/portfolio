from typing import Any, Dict
from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .forms import UserAdminForm, UserForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .helpers import user_has_permission

# Create your views here.

class CreateUser(CreateView):
    model = User
    success_url = reverse_lazy('email_verification')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'Register'
        return context
    
    def get_form_class(self) -> type[BaseModelForm]:

        if self.request.user.is_superuser:
            return UserAdminForm
        
        return UserForm

class ReadUser(UserPassesTestMixin, DetailView):
    model = User

    def test_func(self) -> bool | None:
        return user_has_permission(self, 'auth.view_user')


class UpdateUser(UserPassesTestMixin, UpdateView):
    model = User
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context
    
    def get_form_class(self) -> BaseModelForm:
        if self.request.user.is_superuser:
            return UserAdminForm
        return UserForm

    def test_func(self) -> bool | None:
        return user_has_permission(self, 'auth.change_user')


class DeleteUser(UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('user_list')

    def test_func(self) -> bool | None:
        return user_has_permission(self, 'auth.delete_user')
    
class ListUser(UserPassesTestMixin, ListView):
    model = User
    template_name = 'auth/user_list.html'

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or self.request.user.has_perm('auth.view_user')