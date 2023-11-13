from django.urls import reverse_lazy

from users.models import User


def generate_verify_url(user: User):
    return reverse_lazy('users:email_verify', args=[user.uid])


