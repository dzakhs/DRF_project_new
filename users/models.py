from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR ='moderator', _('moderator')

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активация')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
