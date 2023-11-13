from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordResetForm,
)
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from users import texts
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "country",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()


class CustomPasswordResetForm(PasswordResetForm):
    def save(
        self,
        *args,
        **kwargs,
    ):
        email = self.cleaned_data["email"]
        users = self.get_users(email)

        for user in users:

            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()

            send_mail(
                subject=texts.password_has_been_reset_title,
                message=texts.new_password_message.format(new_password),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_model: User = get_user_model()
        if email not in user_model.objects.values_list("email", flat=True):
            raise forms.ValidationError("Email не найден")
        return email
