from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.conf import settings

from users.forms import UserRegisterForm, UserForm
from users.models import User
from . import texts


class LoginView(BaseLoginView):
    pass


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('catalog:index')
    template_name = 'users/register.html'

    extra_context = {
        'title': texts.users_register_title
    }
    
    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject=texts.email_greeting_title,
            message=texts.email_message_text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user
