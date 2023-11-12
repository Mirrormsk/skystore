from django.urls import path

from .apps import UsersConfig
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    UserUpdateView,
    generate_new_password,
)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", UserUpdateView.as_view(), name="profile"),
    path("profile/generatepassword", generate_new_password,name="generate_new_password",),
]
