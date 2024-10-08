import os
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Команда для создания админа в проекте"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv("SUPERUSER_EMAIL"),
            first_name="admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(os.getenv("SUPERUSER_PASSWORD"))
        user.save()
