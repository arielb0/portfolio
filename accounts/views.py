from typing import Any, Dict
from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from .forms import UserAdminForm, UserForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .helpers import user_has_permission
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

# Create your views here.

class CreateUser(CreateView):
    model = User
    success_url = reverse_lazy('email_verification')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = _('Register')
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
        context['action'] = _('Update')
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
    
class ApiLoginView(APIView):
    '''
        This view class allow login using REST API and store
        JWT access and refresh token on cookies.
    '''
    permission_classes = [AllowAny]

    def post(self, request: Request, format = None):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username = username, password = password)
        if user is None:
            return Response({'detail': 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)
        
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        response = Response({'detail': 'Login successful'}, status = status.HTTP_200_OK)

        response.set_cookie(
            key = 'access_token',
            value = access_token,
            httponly = True,
            secure = True, 
            samesite = 'Strict',
            max_age = 300
        )

        response.set_cookie(
            key = 'refresh_token',
            value = refresh_token,
            path = 'accounts/api/refresh',
            httponly = True,
            secure = True,
            samesite = 'Strict',
            max_age = 86400
        )

        return response
    
class RefreshTokenView(APIView):
    '''
        This view class allow refresh JWT access token using refresh token stored on a cookie.
    '''

    def get(self, request: Request, format = None):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            try:
                refresh_token = RefreshToken(refresh_token)
            except Exception as e:
                raise AuthenticationFailed('Invalid or expired token')
        
            response = Response({'detail': 'Access token refreshed successfully'}, status = status.HTTP_200_OK)

            response.set_cookie(
                key = 'access_token',
                value = str(refresh_token.access_token),
                httponly = True,
                secure = True, 
                samesite = 'Strict',
                max_age = 300
            )

        else:
            response = Response({'detail': 'You need to provide an refresh token to do this action'}, status = status.HTTP_400_BAD_REQUEST)

        return response
