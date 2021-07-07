from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from portal.models import Article, Manufacturer, ArticleGroup, Company
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError

from my_utils.io import csv_upload_to_dict, header_of_csv_upload

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

        bulk = [] # init bulk array, objects in there will be stored in mass together at end


        # auto-detect type depending of col names
        
        type_switch = {
            "name,id_by_manufacturer,manufacturer,group,price": "article",
            "name": "ag",
            "name,address,postcode,city": "company",
            "name,erp_id,website,support_mail": "manu"
        }
        try:
            csv_header = header_of_csv_upload(request.FILES['file'])
        except Exception as e:
            return HttpResponseBadRequest("Error: " + e.message)
        print(csv_header)

        type_ = type_switch.get(csv_header, "")
        if type_ == "":
            return HttpResponseBadRequest("Type could not been detected automatically, found following cols:\n" + 
            csv_header)
        elif type_ == 'article':
            # basic config, easier than switch or stuff like this
            type_ = Article # overwrite type, we don't need original information any more            

            manus = Manufacturer.objects.all()
            art_group = ArticleGroup.objects.all()
            failed_records = []
            header_handled =False
            for item in dict_list:
                if not header_handled:
                    header_handled = True
                    continue
                try:
                    item['manufacturer'] = manus.get(name=item['manufacturer'])
                    item['group'] = art_group.get(name=item['group'])
                except:
                    failed_records.append(str(item))
                    continue
                new_obj = type_(**item)
                bulk.append(new_obj)
        else:
            bulk = [  # https://stackoverflow.com/questions/18383471/django-bulk-create-function-example
                type_(**item)
                for item in dict_list
            ]

        if keep_items:
            start_index = type_.objects.all().order_by("-id")[0].id
        else:
            start_index = 0

        for key, item in enumerate(dict_list):
            key += start_index
            item['pk'] = key

        type_.objects.bulk_create(bulk) # and finally store all gathered objects

        if len(failed_records) > 0:
            return HttpResponseBadRequest("""Not all records could have been stored properly.
            Skipped records:\n""" + str(failed_records))
        else:
            return redirect('frontend_admin:home')

    return render(request, 'frontend/import.html', {

    })
