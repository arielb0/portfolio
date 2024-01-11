from typing import Any
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
import secrets

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms.widgets import TextInput
from django.forms import CharField


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]


class UserRegistrationForm(UserForm):

    def save(self, commit: bool = ...) -> Any:
        
        self.instance.set_password(secrets.token_urlsafe())
        return super().save(commit)

class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget = TextInput(attrs = {'class': 'form-control mb-3'}))
    password = CharField(widget = PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control mb-3"}))