from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import FAQ

# just redirects to home/, could also have integrated it directly in url, but this is better practice
def redirect_to_home(request):
    return redirect('home/')


def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', {})


def about_view(request, *args, **kwargs):
    return render(request, 'pages/about.html', {})

def support_view(request, *args, **kwargs):
    faq = FAQ.objects.all()
    print(faq)
    return render(request, 'pages/support.html', {
        'faq': faq
    })
