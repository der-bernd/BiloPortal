from bilobit_portal.methods import would_be_circle, mail
from .db_queries import *
from accounts.models import Responsible
from .models import *
from json import dumps
from .forms import CompanyForm, CompanyPostForm, EmployeeForm, EmployeeImportForm, BookingConfigForm, EmployeeAssignmentForm
from dateutil.relativedelta import relativedelta
from io import StringIO
import csv
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from django.db.models.expressions import RawSQL


def re_slugify(slug):
    return str(slug).replace('-', '')  # just remove all the hyphens


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
        return redirect('/')
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


def company_create_update(request, com_id=''):
    if request.method == 'POST':
        try:
            obj = Company.objects.get(uuid=com_id)
        except:
            obj = None
        # have to give obj as well, otherwise new record would be created
        form = CompanyPostForm(request.POST, instance=obj)

        if form.is_valid():
            form.save()

            return redirect('portal:home')

    try:
        obj = Company.objects.get(uuid=com_id)
    except:
        obj = None

    if obj is not None:
        print(obj.uuid)
        arr = Company.objects.raw(GET_POSSIBLE_MOTHER_COMPANIES, [
                                  re_slugify(obj.uuid)])
        arr_1 = [b.id for b in arr]

        possible_mothers = Company.objects.filter(id__in=arr_1)
    else:
        possible_mothers = Company.objects.all()

    form = CompanyForm(current_mother=obj.mother_company,
                       possible_mothers=possible_mothers, instance=obj)

    return render(request, 'portal/company/create_or_update.html', get_final_context(request, {
        'form': form,
        'possible_mothers': possible_mothers,
        'creating': obj is None
    }))


def company_detail(request, com_id=''):
    if com_id == '':  # select default company for this user
        root_company_uuid = request.user.company.uuid
        # when no uuid in url, then find out matching url and redirect to it
        return redirect('portal:home-uuid', com_id=root_company_uuid)

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

    articles = Booking.objects.raw(
        GET_SERVICES_OF_COMPANY, [re_slugify(com_id)])
    services = {}
    gantt_data = []

    for ar in articles:
        if ar.uuid not in services:
            services[ar.uuid] = []
            gar_obj = {
                'id': re_slugify(ar.uuid),
                'name': ((ar.employee_first_name + ' ' + ar.employee_last_name + ' › ') if ar.employee_first_name else '') + ar.service_name,
                'actualStart': ar.start_date_stamp,
                'actualEnd': ar.end_date_stamp,
                'progressValue': ar.progress
            }
            # only append first item, otherwise for each article would a line be generated
            gantt_data.append(gar_obj)

        services[ar.uuid].append(ar)

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

            next(io_string)  # skip header

            for line in csv.reader(io_string, delimiter=','):
                _, created = Employee.objects.update_or_create(
                    first_name=line[0],
                    last_name=line[1],
                    mail=line[2],
                    company=company
                )

            return redirect('portal:home')

        if form.is_valid():
            empl = form.save(commit=False)
            empl.company = Company.objects.get(uuid=com_id)
            form.save()
            return redirect('portal:home')

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

    if request.method == 'POST':
        obj.delete()
        return redirect('portal:home')

    return render(request, 'portal/employee/delete.html', get_final_context(request, {
        "employee": obj,
    }))


def service_store(request, com_id):
    company = Company.objects.get(uuid=com_id)

    articles = Service.objects.raw(GET_SERVICES_FROM_STORE, [company.id])
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
        return redirect('portal_home', comp_id=booking.company.uuid)

    return render(request, 'portal/service/lengthen.html', get_final_context(request, {

    }))


def assign_employee(request, booking_id):
    booking = Booking.objects.get(uuid=booking_id)

    if request.method == 'POST':
        mail = request.POST['employee']

        try:
            booking.assigned_employee = Employee.objects.get(mail=mail)
        except:
            booking.assigned_employee = None
        booking.save()
        return redirect('portal:home-uuid', com_id=booking.company.uuid)

    form = EmployeeAssignmentForm(
        booking.company, current=booking.assigned_employee)

    return render(request, 'portal/service/assign_employee.html', get_final_context(request, {
        'form': form,
        'booking': booking
    }))
