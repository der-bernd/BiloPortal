from django.shortcuts import render, redirect
from portal.models import Article, Manufacturer, ArticleGroup, Company
from .forms import FileImportForm
from io import StringIO
import csv
import io
import pandas


def csv_upload_to_dict_list(request_FILE):
    csv_file = request_FILE

    if not csv_file.name.endswith('.csv'):
        return None
    csv_data = csv_file.read().decode('utf-8')

    # https://stackoverflow.com/questions/59163616/read-a-django-uploadedfile-into-a-pandas-dataframe
    dataframe = pandas.read_csv(io.StringIO(csv_data), delimiter=',')

    print(dataframe)
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
    dict_list = dataframe.to_dict('records')

    return dict_list


def app_overview(request):
    return render(request, 'frontend/app.html', {})


def import_articles(request):
    if request.method == 'POST':
        type_ = request.POST.get('type')
        keep_items = request.POST.get('keep_items')

        dict_list = csv_upload_to_dict_list(request.FILES['file'])

        switcher = {
            'article': Article,
            'manu': Manufacturer,
            'group': ArticleGroup,
            'company': Company
        }

        model_type = switcher[type_]
        bulk = []
        if type_ == 'article':
            manus = Manufacturer.objects.all()
            art_group = ArticleGroup.objects.all()
            for item in dict_list:
                try:
                    item['manufacturer'] = manus.get(name=item['manufacturer'])
                    item['group'] = art_group.get(name=item['group'])
                except:
                    print('Could not import ' + str(item))
                    continue
                new_obj = model_type(**item)
                bulk.append(new_obj)
        else:
            bulk = [  # https://stackoverflow.com/questions/18383471/django-bulk-create-function-example
                model_type(**item)
                for item in dict_list
            ]

        if keep_items:
            start_index = model_type.objects.all().order_by("-id")[0].id
        else:
            start_index = 0

        for key, item in enumerate(dict_list):
            key += start_index
            item['pk'] = key

        model_type.objects.bulk_create(bulk)

        return redirect('frontend_admin:home')

    return render(request, 'frontend/import.html', {

    })
