from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where mail is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, mail, password, **extra_fields):
        """
        Create and save a User with the given mail and password.
        """
        if not mail:
            raise ValueError(_('The mail must be set'))
        mail = self.normalize_email(mail)
        user = self.model(mail=mail, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mail, password, **extra_fields):
        """
        Create and save a SuperUser with the given mail and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(mail, password, **extra_fields)
