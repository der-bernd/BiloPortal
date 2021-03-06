from django.core.exceptions import ValidationError
import pandas
from io import StringIO

def csv_upload_to_dict(request_FILE):
    csv_to_multiline(request_FILE)

    # https://stackoverflow.com/questions/59163616/read-a-django-uploadedfile-into-a-pandas-dataframe
    dataframe = pandas.read_csv(StringIO(csv_to_multiline), delimiter=',')
    
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
    dict_list = dataframe.to_dict('records')

    return dict_list

def csv_to_multiline(csv_file):

    if not csv_file.name.endswith('.csv'):
        raise ValidationError("Data can only be converted via CSV")
    csv_multiline = csv_file.read().decode('utf-8') # str() just to make sure that multi-line-string will be returned

    print(csv_multiline)

    return csv_multiline

def header_of_csv_upload(request_FILE):
    file = csv_to_multiline(request_FILE)

    if not file.name.endswith('.csv'):
        raise ValidationError("Data can only be converted via CSV")
    csv_multiline = str(file.read().decode('utf-8')) # str() just to make sure that multi-line-string will be returned
    print(csv_multiline)
    lines = csv_multiline.splitlines()
    print(lines)
    return lines[0]