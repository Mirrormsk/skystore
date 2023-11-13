from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    PasswordResetConfirmView,
)
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import (
    PasswordResetView as BasePasswordResetView,
    PasswordResetDoneView as BasePasswordResetDoneView,
)
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserForm, CustomPasswordResetForm
from users.models import User
from . import texts
from .services import generate_verify_url
from .texts import password_has_been_reset_title, new_password_message


class LoginView(BaseLoginView):
    pass


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("catalog:index")
    template_name = "users/register.html"

    extra_context = {"title": texts.users_register_title}

    def form_valid(self, form):
        user = form.save()
        verify_url = self.request.build_absolute_uri(generate_verify_url(user))
        send_mail(
            subject=texts.email_greeting_title,
            message=texts.email_message_text.format(verify_url),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy("users:profile")
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


class ActivationSuccessfulView(TemplateView):
    template_name = "users/activation_successful.html"


class PasswordResetView(BasePasswordResetView):
    email_template_name = 'users/password_reset_email'
    template_name = "users/password_reset_page.html"
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("users:password_reset_done")


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = "users/password_reset_done.html"


def activate_user(request, uid):
    user = get_object_or_404(User, uid=uid)
    user.is_active = True
    user.save()
    return redirect(reverse("users:activation_successful"))
