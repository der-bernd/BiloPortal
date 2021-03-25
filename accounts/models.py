from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class Responsible(AbstractUser):
    username = None
    email = None
    mail = models.EmailField(_('mail address'), unique=True)

    USERNAME_FIELD = 'mail'  # one of the most important rows
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.mail
