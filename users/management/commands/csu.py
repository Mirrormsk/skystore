from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input("Enter superuser email: ")

        psw1 = input("Enter password: ")
        psw2 = input("Confirm password: ")

        while psw1 != psw2:
            print("Passwords didn't match!")
            psw1 = input("Enter password: ")
            psw2 = input("Confirm password: ")

        user = User.objects.create(
            email=email,
            first_name="Admin",
            last_name="Skystore",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(psw1)
        user.save()
