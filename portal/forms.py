from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import NumberInput
from .models import Company, MyModelChoiceField, Employee, Booking

from .methods import would_be_circle, is_valid_mail


class CompanyForm(forms.ModelForm):
    possible_mothers = Company.objects.all()

    mother_company = MyModelChoiceField(queryset=possible_mothers,
                                        empty_label="- no mother company -", label="Mother company", required=False)

    class Meta:
        model = Company
        fields = [
            'name',
            'address',
            'postcode',
            'city',
            'details',
            'mother_company'
        ]

    """ def clean_mother_company(self, *args, **kwargs):
        mother_com = self.cleaned_data.get('mother_company')
        mother_id = mother_com.id
        try:
            own_id = self.cleaned_data.get('id')
            print(own_id)
        except:
            own_id = 0
        if own_id > 0:
            is_circle = would_be_circle(own_id, mother_id)
            if is_circle:
                raise ValidationError(str(
                    to_be_saved.mother_company.name) + ' is already a mother -> circle would be generated')
        return mother_com """

    def clean_postcode(self, *args, **kwargs):
        postcode = self.cleaned_data.get('postcode')
        if postcode > 10000 and postcode < 99999:
            return postcode
        else:
            raise ValidationError('Postcode not valid')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'mail',
        ]

    def clean_mail(self, *args, **kwargs):
        mail = self.cleaned_data.get('mail')
        if is_valid_mail(mail):
            return mail
        else:
            raise ValidationError('Mail not valid')


class EmployeeImportForm(forms.Form):
    file = forms.FileField()


class BookingConfigForm(forms.ModelForm):
    amount = forms.IntegerField(min_value=1, initial=1)
    start_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 3}), required=False)

    class Meta:
        model = Booking
        fields = [
            'amount',
            'start_date',
            'notes'
        ]

    def clean_date(self, *args, **kwargs):
        date = self.cleaned_data['start_date']
        return date
