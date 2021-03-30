from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import NumberInput
from .models import Company, CompanyChoiceField, Employee, Booking, EmployeeChoiceField

from bilobit_portal.methods import would_be_circle, is_valid_mail


class CompanyPostForm(forms.ModelForm):
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

    def clean_postcode(self, *args, **kwargs):
        postcode = self.cleaned_data.get('postcode')
        if postcode > 10000 and postcode < 99999:
            return postcode
        else:
            raise ValidationError('Postcode not valid')


class CompanyForm(forms.ModelForm):
    mother_company = forms.CharField()  # just to have a field

    def __init__(self, instance, current_mother, possible_mothers, *args, **kwargs):
        super(CompanyForm, self).__init__(instance=instance, *args, **kwargs)
        # print(possible_mothers)
        self.fields['mother_company'] = CompanyChoiceField(
            initial=current_mother,
            queryset=possible_mothers, empty_label="- no mother company set -", label="Mother Company", required=False)

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

    # """ def clean_mother_company(self, *args, **kwargs):
    #     mother_com = self.cleaned_data.get('mother_company')
    #     mother_id = mother_com.id
    #     try:
    #         own_id = self.cleaned_data.get('id')
    #         print(own_id)
    #     except:
    #         own_id = 0
    #     if own_id > 0:
    #         is_circle = would_be_circle(own_id, mother_id)
    #         if is_circle:
    #             raise ValidationError(str(
    #                 to_be_saved.mother_company.name) + ' is already a mother -> circle would be generated')
    #     return mother_com """

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


def get_employees_of_company(company):
    return Employee.objects.filter(company=company)


class EmployeeAssignmentForm(forms.ModelForm):
    employee = forms.CharField()  # just to have a field

    def __init__(self, company_obj, current, *args, **kwargs):
        super(EmployeeAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['employee'] = EmployeeChoiceField(initial=current,
                                                      queryset=get_employees_of_company(company_obj), empty_label="- no employee assigned -", label="Employee", required=False)

    class Meta:
        model = Booking
        fields = [
            'employee'
        ]
