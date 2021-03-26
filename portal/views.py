from io import StringIO
import csv
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from dateutil.relativedelta import relativedelta

from .forms import CompanyForm, EmployeeForm, EmployeeImportForm, BookingConfigForm
from json import dumps

from .models import *
from accounts.models import Responsible
from .db_queries import *

from .methods import would_be_circle, mail


def re_slugify(slug):
    return str(slug).replace('-', '')


def app_overview(request):
    return render(request, 'portal/app.html', get_final_context(request))


def get_final_context(request, obj={}):
    obj['site_info'] = {
        'app': 'Bilobit',
        'page': 'Portal'
    }
    return obj


def company_delete(request, com_id):
    obj = get_object_or_404(Company, uuid=com_id)
    children = len(Company.objects.filter(
        mother_company__uuid=com_id).annotate(Count('id')))
    obj.children = children
    if request.method == 'POST':  # delete object only when POSTING to this url
        obj.delete()
        return redirect('../../')
    else:
        return render(request, 'portal/company/delete.html', get_final_context(request, {
            "object": obj,
        }))


def company_list_view(request):
    if not request.user.is_staff:
        raise Http404("You are not allowed to access this page")
    queryset = Company.objects.all()
    handled_ids = []
    arr = []

    for com in queryset:  # just convert queryset to list
        if com.id not in handled_ids:  # when id has already been handled, continue with next item
            handled_ids.append(com.id)

            obj = {
                'name': com.name,
                'address': com.address,
                'postcode': com.postcode,
                'city': com.city,
                'details': com.details,
                'link': com.link,
                'children': [],
            }

            children = Company.objects.filter(mother_company=com.id)

            children_arr = []
            for ch in children:
                if ch.id not in handled_ids:  # same procedure as above
                    handled_ids.append(ch.id)
                    ch_obj = {
                        'name': ch.name,
                        'address': ch.address,
                        'postcode': ch.postcode,
                        'city': ch.city,
                        'details': ch.details,
                        'link': ch.link,
                        'children': []
                    }

                    subchildren = Company.objects.filter(mother_company=ch.id)
                    for s in subchildren:
                        handled_ids.append(s.id)

                    ch_obj['children'] = subchildren

                    obj['children'].append(ch_obj)

            arr.append(obj)

    return render(request, 'portal/company/list.html', get_final_context(request, {
        "list": arr
    }))


def company_create(request):
    form = CompanyForm(request.POST or None)
    possible_mother_companies = Company.objects.all()
    """ can return all other companies, because the company which is going to be added
    is not in the db yet """
    if request.method == 'POST':
        print(request.body)
        if form.is_valid():
            form.save()
            return redirect('../')  # redirect directly to list
    else:
        return render(request, 'portal/company/create.html', get_final_context(request, {
            'form': form,
            'possible_mother_companies': possible_mother_companies
        }))


def company_update(request, id=0):
    form = CompanyForm(request.POST or None)
    # possible_mother_companies = Company.objects.all()
    """ can return all other companies, because the company which is going to be added
    is not in the db yet """
    if request.method == 'POST':
        print(request.body)
        if form.is_valid():
            form.save()
            return redirect('../')  # redirect directly to list
    else:
        return render(request, 'portal/company/create.html', get_final_context(request, {
            'form': form
        }))


def company_create_update(request, com_id=''):
    if request.method == 'POST':
        try:
            obj = Company.objects.get(uuid=com_id)
        except:
            obj = None
        # have to give obj as well, otherwise new record would be created
        form = CompanyForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()

            if obj is None:
                return redirect('../')  # redirect directly to list
            else:
                return redirect('../../')  # has to go one more level up

    # the part below will handle GET requests when not returned already
    try:
        obj = Company.objects.get(uuid=com_id)
    except:
        obj = None

    if obj is None:
        print('creating')
    else:
        print('updating')

    possible_mothers = Company.objects.all()
    if obj is not None:
        filtered = []
        for mother_com in possible_mothers:
            if not would_be_circle(com_id, mother_com.id):
                filtered.append(mother_com)
            else:
                print('sorted out ' + mother_com.name)
        possible_mothers = filtered

    form = CompanyForm(instance=obj)

    return render(request, 'portal/company/create_or_update.html', get_final_context(request, {
        'form': form,
        'possible_mothers': possible_mothers,
        'creating': obj is None
    }))


def company_detail(request, com_id=''):
    if com_id == '':  # select default company for this user
        root_company_uuid = request.user.company.uuid
        # when no uuid in url, then find out matching url and redirect to it
        return redirect(str(root_company_uuid) + '/')

    all_comps = Company.objects.raw(
        GET_COMPANY_HIERARCHY, [re_slugify(com_id)])

    if len(all_comps) == 0:
        raise Http404("Invalid ID: Company could not be found")
    comps = {}
    current_comp = None
    for comp in all_comps:
        if comp.level == 1:
            current_comp = comp
        if comp.level not in comps:
            comps[comp.level] = []
        comps[comp.level].append(comp)

    responsibles = Responsible.objects.filter(
        company=current_comp)
    employees = Employee.objects.filter(company=current_comp)

    query = str(GET_SERVICES_OF_COMPANY)

    articles = Booking.objects.raw(query, [re_slugify(com_id)])
    services = {}
    gantt_data = []

    for ar in articles:
        if ar.uuid not in services:
            services[ar.uuid] = []

        services[ar.uuid].append(ar)
        gar_obj = {
            'id': re_slugify(ar.uuid),
            'name': ar.service_name,
            'actualStart': ar.start_date_stamp,
            'actualEnd': ar.end_date_stamp,
            'progressValue': ar.progress
        }
        print(gar_obj)
        gantt_data.append(gar_obj)

    return render(request, 'portal/company/detail.html', get_final_context(request, {
        'companies': comps,
        'responsibles': responsibles,
        'employees': employees,
        'services': services,
        'current': current_comp,
        'gantt_data': dumps(gantt_data)
    }))


def employee_create_update(request, com_id, em_id=''):
    if request.method == 'POST':
        if not request.FILES:
            try:
                if em_id == '':
                    obj = None
                else:
                    obj = Employee.objects.get(uuid=em_id)
            except:
                obj = None
            # have to give obj as well, otherwise new record would be created
            form = EmployeeForm(request.POST, instance=obj)
        else:  # file(s) were uploaded

            company = Company.objects.get(uuid=com_id)
            csv_file = request.FILES['file']

            if not csv_file.name.endswith('.csv'):
                return None
            csv_data = csv_file.read().decode('utf-8')

            io_string = StringIO(csv_data)
            next(io_string)  # skip header

            for line in csv.reader(io_string, delimiter=','):
                _, created = Employee.objects.update_or_create(
                    first_name=line[0],
                    last_name=line[1],
                    mail=line[2],
                    company=company
                )

            return redirect('/portal/company/')

        if form.is_valid():
            empl = form.save(commit=False)
            empl.company = Company.objects.get(uuid=com_id)
            form.save()
            return redirect('portal:detail')

    try:
        if em_id == '':
            obj = None
        else:
            obj = Employee.objects.get(uuid=em_id)
    except:
        obj = None

    em_form = EmployeeForm(instance=obj)
    if em_id == '':
        file_form = EmployeeImportForm()
    else:
        file_form = None

    return render(request, 'portal/employee/create_or_update.html', get_final_context(request, {
        'em_form': em_form,
        'file_form': file_form,
        'creating': obj is None,
    }))


def employee_delete(request, com_id, em_id):
    obj = Employee.objects.get(uuid=em_id)

    if request.method == 'POST':  # delete object only when POSTING to this url
        obj.delete()
        return redirect('../../')
    else:
        return render(request, 'portal/employee/delete.html', get_final_context(request, {
            "employee": obj,
        }))


def service_store(request, com_id):
    company = Company.objects.get(uuid=com_id)
    print(company.id)

    query = str(GET_SERVICES_FROM_STORE)

    articles = Service.objects.raw(query, [company.id])
    services = {}
    for ar in articles:
        if ar.service_id not in services:
            services[ar.service_id] = []

        services[ar.service_id].append(ar)

    return render(request, 'portal/service/store.html', get_final_context(request, {
        'company': company,
        'services': services
    }))


def service_config(request, com_id, service_id):
    company = Company.objects.get(uuid=com_id)
    service = Service.objects.get(uuid=service_id)
    if request.method == 'POST':
        form = BookingConfigForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.company_id = company.id
            obj.service_id = service.id
            obj.end_date = obj.start_date + \
                relativedelta(months=service.duration)
            form.save()
            return redirect('../../../')

    query = str(GET_SERVICES_FROM_STORE)

    articles = Service.objects.raw(query, [company.id])
    service = []
    for ar in articles:
        service.append(ar)

    form = BookingConfigForm()

    return render(request, 'portal/service/config.html', get_final_context(request, {
        'form': BookingConfigForm,
        'service': service
    }))


def booking_edit(request, booking_id):
    booking = Booking.objects.get(uuid=booking_id)
    if request.method == 'POST':
        try:
            months_to_be_added = int(request.POST['months_to_be_added'])
        except:
            raise ValidationError('Could not convert to string')
        booking.end_date = booking.end_date + \
            relativedelta(months=months_to_be_added)
        booking.save()
        return redirect('../../')

    # query =
    # articles = Service.objects.raw(query, [booking.company.id])
    # service = []
    # for ar in articles:
    #     service.append(ar)

    return render(request, 'portal/service/lengthen.html', get_final_context(request, {

    }))
