from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .methods import mail as send_mail


def test(request):  # just for some small backend tests
    send_mail(subject='Hello', to='test@bernd.one', message='Hello there')

    return render(request, 'test.html', {
        'data': 'hello'
    })
