from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from portal.models import Company
import uuid


class Responsible(AbstractUser):
    username = None
    email = None
    mail = models.EmailField(unique=True)
    company = models.ForeignKey(
        Company, on_delete=models.RESTRICT, null=True, blank=False)
    is_admin = models.BooleanField(_('Admin'), default=False)

    uuid = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)

    USERNAME_FIELD = 'mail'  # one of the most important rows
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.mail
