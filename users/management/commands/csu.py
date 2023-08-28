from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='dok@mail.ru',
            first_name='Dmitry',
            last_name='Dok',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()
