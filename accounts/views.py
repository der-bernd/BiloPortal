from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from portal.models import Company
from accounts.models import Responsible
from django.conf import settings

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

            return redirect('/portal/company/')

    form = ResponsibleCreationForm()

    return render(request, 'registration/signup.html', {
        'form': form,
        'company': company
    })


def responsible_delete(request, resp_id):
    resp = settings.AUTH_USER_MODEL
    print(resp)
    if request.method == 'POST':
        resp.delete()

        return reverse('portal:home')

    return render(request, 'registration/delete.html', {
        'responsible': resp
    })
