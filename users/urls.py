from django.urls import path

from .apps import UsersConfig
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserUpdateView,
    activate_user,
    ActivationSuccessfulView,
    PasswordResetView,
    PasswordResetDoneView, CustomPasswordResetConfirmView
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserUpdateView.as_view(), name="profile"),
    # path("profile/generatepassword/", generate_new_password, name="generate_new_password"),
    path("profile/<uuid:uid>/verify/", activate_user, name="email_verify"),
    path("activation_successful/", ActivationSuccessfulView.as_view(), name="activation_successful"),
    path("profile/password-reset/", PasswordResetView.as_view(), name="password_reset"),
    # path('reset-password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("profile/password-reset-done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
]
