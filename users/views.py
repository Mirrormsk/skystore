from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserForm
from users.models import User


class LoginView(BaseLoginView):
    pass


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'users/register.html'

    extra_context = {
        'title': 'Регистрация нового пользователя'
    }
