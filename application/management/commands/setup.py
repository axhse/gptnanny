import secrets
from os import environ

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


def create_manager():
    user, _ = User.objects.get_or_create(username="manager")
    environ.setdefault("MANAGER_TOKEN", secrets.token_hex(20))
    user.set_password(environ["MANAGER_TOKEN"])
    content_type = ContentType.objects.get_for_model(User)
    manager_permission, _ = Permission.objects.get_or_create(
        codename="manage", content_type=content_type
    )
    manager_permission.save()
    user.user_permissions.add(manager_permission)
    user.save()


class Command(BaseCommand):
    help = "Initializes the application"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        create_manager()
