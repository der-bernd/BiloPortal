from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from portal.models import Article, Manufacturer, ArticleGroup, Company
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError

from my_utils.io import csv_upload_to_dict

def app_overview(request):
    return render(request, 'frontend/app.html', {})


def import_articles(request):
    if request.method == 'POST':
        type_ = request.POST.get('type')
        keep_items = request.POST.get('keep_items')

        dict_list = []
        try:
            dict_list = csv_upload_to_dict(request.FILES['file'])
        except Exception as e:
            print("error detected")
            return HttpResponseBadRequest("Error: " + e.message)

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
            failed_records = []
            for item in dict_list:
                try:
                    item['manufacturer'] = manus.get(name=item['manufacturer'])
                    item['group'] = art_group.get(name=item['group'])
                except:
                    failed_records.append(str(item))
                    continue
                new_obj = model_type(**item)
                bulk.append(new_obj)
            if len(failed_records) > 0:
                return HttpResponseBadRequest("""Not all records could have been stored properly.
                Skipped records:\n""" + str(failed_records))
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
