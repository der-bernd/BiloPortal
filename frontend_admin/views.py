from django.shortcuts import render, redirect
from portal.models import Article, Manufacturer, ArticleGroup
from .forms import FileImportForm
from io import StringIO
import csv
import io
import pandas


def import_articles(request):
    if request.method == 'POST':
        type_ = request.POST.get('type')
        keep_items = request.POST.get('keep_items')
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return None
        csv_data = csv_file.read().decode('utf-8')

        paramFile = request.FILES['file'].file

        # https://stackoverflow.com/questions/59163616/read-a-django-uploadedfile-into-a-pandas-dataframe
        dataframe = pandas.read_csv(io.StringIO(csv_data), delimiter=',')

        print(dataframe)
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
        dict_list = dataframe.to_dict('records')

        switcher = {
            'article': Article,
            'manu': Manufacturer,
            'group': ArticleGroup
        }

        model_type = switcher[type_]

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

        print(dict_list)

        model_type.objects.bulk_create(bulk)

        # for line in csv.reader(io_string, delimiter=','):
        #     bulk.append(Entry())

        #     type_model = switcher[type_]
        #     if type_model is None:
        #         print('Fail')
        #         return

        #     print(line)

        #     # elif type_ == 'manufacturer':
        #     #     Manufacturer.objects.create(
        #     #         name=line[0], erp_id=line[1], website=line[2], support_mail=line[3])
        # switcher = {
        #     'article': Article,
        #     'manu': Manufacturer,
        #     'group': ArticleGroup
        # }
        # obj = type_model.objects.get(name=line[0])
        # if not obj:
        #         print('ERROR at importing: of ' +
        #               line[0] + ' not found!')
        # else:
        # type_model.objects.create(line)

        return redirect('frontend_admin:import-articles')

    return render(request, 'frontend/import.html', {

    })
