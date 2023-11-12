from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm
from users.models import User
from . import texts
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
        send_mail(
            subject=texts.email_greeting_title,
            message=texts.email_message_text,
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


def generate_new_password(request):
    user = request.user

    new_password = BaseUserManager().make_random_password()
    user.set_password(new_password)
    user.save()

    send_mail(
        subject=password_has_been_reset_title,
        message=new_password_message.format(new_password),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    update_session_auth_hash(request, user)

    return redirect(reverse("users:profile"))
