from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from portal.models import Company
from accounts.models import Responsible
from django.conf import settings

from bilobit_portal.methods import mail, responsible_added_text

from .forms import ResponsibleCreationForm, ResponsibleChangeForm


class SignUpView(CreateView):
    form_class = ResponsibleCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def responsible_create_update(request, com_id):
    company = Company.objects.get(uuid=com_id)
    if request.method == 'POST':
        form = ResponsibleCreationForm(request.POST)
        if form.is_valid():

            obj = form.save(commit=False)
            obj.company = company
            form.save()

            mail(to=obj.mail, subject='Bilobit Portal: Your account has been created',
                 message=responsible_added_text(obj.mail, obj.first_name))

            return redirect('portal:home')

    form = ResponsibleCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form,
        'company': company
    })


def responsible_delete(request, resp_id):
    resp = Responsible.objects.get(uuid=resp_id)
    if request.method == 'POST':
        resp.delete()

        return redirect('portal:home')

    return render(request, 'registration/delete.html', {
        'responsible': resp
    })
