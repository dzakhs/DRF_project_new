from celery import shared_task

from users.models import User
from datetime import timedelta
from django.utils import timezone


@shared_task
def check_user():
    user_list = User.objects.all().filter(is_active=True)
    for item in user_list:
        one_month_ago = timezone.now() - timedelta(days=30)
        if item.last_login < one_month_ago:
            item.is_active = False
            print("Пользователь деактивирован !!!!")
            item.save()
        else:
            print('Пользователей для деактивации нет !!!')