from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import CreateUser, ReadUser, UpdateUser, DeleteUser, ListUser
from .views import ApiLoginView, RefreshTokenView
from .forms import CustomLoginForm

urlpatterns = [    
    path("login/",auth_views.LoginView.as_view(form_class=CustomLoginForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("home")), name="logout"),
    path("password_change/", auth_views.PasswordChangeView.as_view(template_name="registration/mod_password_change_form.html"), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="registration/mod_password_change_done.html"), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/mod_password_reset_form.html", email_template_name='registration/mod_password_reset_email.html'), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="registration/mod_password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="registration/mod_password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="registration/mod_password_reset_complete.html"), name="password_reset_complete"),
    # User CRUD
    path("register/", CreateUser.as_view(), name="register"),
    path("<int:pk>", ReadUser.as_view(), name="read_user"),
    path("<int:pk>/update", UpdateUser.as_view(), name="update_user"),
    path("<int:pk>/delete", DeleteUser.as_view(), name="delete_user"),
    path("", ListUser.as_view(), name = "user_list"),
    # Email verification
    path("email_verification/", TemplateView.as_view(template_name="registration/email_verification.html"), name="email_verification"),
    # API authentication
    path('api/login', ApiLoginView.as_view(), name = 'api_login'),
    path('api/refresh', RefreshTokenView.as_view(), name = 'api_refresh'),
]
