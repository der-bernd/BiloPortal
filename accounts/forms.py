from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Responsible


class ResponsibleCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Responsible
        fields = ('mail',)


class ResponsibleChangeForm(UserChangeForm):
    class Meta:
        model = Responsible
        fields = ('mail',)
