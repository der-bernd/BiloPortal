from django.core.mail import send_mail
from django.shortcuts import redirect
from portal.models import Company
import re


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
    # stolen from stackoverflow, as you can imagine; wasn't heavy to find, so link was omitted
    match = re.search(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', mail, re.I)
    return len(match.group()) > 0


def mail(to, message, subject="Bilobit Portal | Information"):
    send_mail(
        subject=subject,
        message=message,
        from_email='bilobit-noreply@bernd.one',
        recipient_list=[to],
        fail_silently=False
    )


def html_mail(to, html, subject="Bilobit Portal | Information"):
    send_mail(
        subject=subject,
        html_message=html,
        from_email='bilobit-noreply@bernd.one',
        recipient_list=[to],
        fail_silently=False
    )


def responsible_added_text(mail, first_name):
    greeting = 'Hello'
    if first_name:
        greeting += ', ' + first_name
    greeting += '!\n\n'
    text1 = 'You account has been created by an for you company authorized admin and can now be used to use the portal.\n\n'
    text2 = 'Please use your mail address ' + mail + \
        ' as username and the password entered by your admin.\n\n'
    text3 = 'Login mask can be found under http://127.0.0.1:8000/accounts/login\n\n'
    text4 = 'Kind regards, your support team'
    return greeting, text1, text2, text3, text4


# contants and parameters you can use in the functions above
