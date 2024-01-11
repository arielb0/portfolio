from typing import Any, Dict
from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .forms import UserForm, UserRegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

class CreateUser(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy("email_verification")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'Register'
        return context


class ReadUser(UserPassesTestMixin, DetailView):
    model = User

    def test_func(self) -> bool | None:
        return get_permission(self)


class UpdateUser(UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def test_func(self) -> bool | None:
        return get_permission(self)


class DeleteUser(UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy("home")

    def test_func(self) -> bool | None:
        return get_permission(self)


def get_permission(self) -> bool:
    return self.request.user.id == self.get_object().id