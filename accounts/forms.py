from typing import Any
from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User
import secrets

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms.widgets import TextInput, SelectMultiple
from django.forms import CharField

class UserAdminForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'groups']
        widgets = {
            'first_name': TextInput(attrs = {'class': 'form-control'}),
            'last_name': TextInput(attrs = {'class': 'form-control'}),
            'email': TextInput(attrs = {'class': 'form-control'}),
            'username': TextInput(attrs = {'class': 'form-control'}),
            'groups': SelectMultiple(attrs = {'class': 'form-select'})
        }

class UserForm(UserAdminForm):

    class Meta(UserAdminForm.Meta):
        exclude = ['groups']
    

class UserRegistrationForm(UserForm):

    def save(self, commit: bool = ...) -> Any:
        
        self.instance.set_password(secrets.token_urlsafe())
        return super().save(commit)

class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget = TextInput(attrs = {'class': 'form-control mb-3'}))
    password = CharField(widget = PasswordInput(attrs={"autocomplete": "current-password", "class": "form-control mb-3"}))