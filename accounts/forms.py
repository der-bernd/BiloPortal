from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Responsible


class ResponsibleCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Responsible
        fields = ('mail', 'first_name', 'last_name')


class ResponsibleChangeForm(UserChangeForm):
    class Meta:
        model = Responsible
        fields = ('mail', 'first_name', 'last_name')
