from django.contrib.auth.views import LoginView
from django.urls import path

from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name='users/login.html'), name='login'),
    # path("", LoginView.as_view(), name='logout'),
]
