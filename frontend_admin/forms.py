from django import forms


class FileImportForm(forms.Form):
    # class Meta:
    #     fields = ['file_', 'type']
    file_ = forms.FileField()
    type_ = forms.MultipleChoiceField(
        choices=['Articles', 'Companies', 'Manufacturers'])
