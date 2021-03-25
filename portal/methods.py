from django.core.mail import send_mail
from django.shortcuts import redirect
from .models import Company
import re
import itertools


def would_be_circle(child_id, mother_id):
    current_id = mother_id  # start at mother and look for her mothers
    current = Company.objects.get(id=current_id)
    print(str(child_id) + str(mother_id))
    """ res = Company.objects.filter(
        mother_company__mother_company__mother_company__mother_company__mother_company__mother_company=child_id)
    try:
        res.get(id=mother_id)
        return True
    except:
        return False """
    while current.mother_company:
        if current.mother_company.id == child_id:
            return True
        else:
            current_id = current.mother_company.id
            # pretty bad way, hits the database every time!
            current = Company.objects.get(id=current_id)

    return False


def is_valid_mail(mail):
    # stolen from stackoverflow, as you can imagine
    match = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', mail, re.I)
    return len(match.group()) > 0


def mail(to, text, subject="Mail sent by django"):
    send_mail(
        'subject',
        'hallo',
        'bilobit-noreply@bernd.one',
        [to],
        fail_silently=False,
    )
