from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import Responsible
from bilobit_portal.methods import is_valid_mail


class ResponsibleCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Responsible
        fields = ('mail', 'first_name', 'last_name')

    def clean_mail(self):
        mail = self.cleaned_data['mail']
        if not is_valid_mail(mail):
            raise ValidationError('Mail is not valid!')
        return mail


class ResponsibleChangeForm(UserChangeForm):
    class Meta:
        model = Responsible
        fields = ('mail', 'first_name', 'last_name')
