import uuid

from django.db import models
from django.forms import ModelChoiceField
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.utils import timezone

from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter


# excellent src for polymorphism in django:
# https://realpython.com/modeling-polymorphism-django-python/


class Company(models.Model):

    name = models.CharField(max_length=120)
    uuid = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)
    address = models.CharField(max_length=120)
    postcode = models.IntegerField()
    city = models.CharField(max_length=120, blank=False)
    details = models.TextField(
        blank=True, null=False)
    mother_company = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name + ' aus ' + self.city


class Employee(models.Model):
    username = None  # remove the usual primary field at it is not needed
    email = None
    mail = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, default=32, blank=False, null=True)
    uuid = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)

    def __str__(self):
        return self.mail


class ArticleGroup(models.Model):
    name = models.CharField(max_length=128)
    mother_group = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)  # blank is important: NULL in forms

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    erp_id = models.CharField(max_length=128)
    website = models.URLField(null=True)
    support_mail = models.EmailField(null=True)
    notes = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=5000, null=True, blank=True)
    id_by_manufacturer = models.CharField(max_length=128)
    erp_id = models.CharField(
        max_length=128, null=True, blank=True)  # if distinct to above
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    group = models.ForeignKey(
        ArticleGroup, on_delete=models.PROTECT, null=True, blank=False)
    price = models.IntegerField()
    # in days, NULL stands for not-expiring
    duration = models.IntegerField(null=True, blank=True)
    end_of_sales = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ServiceGroup(models.Model):
    name = models.CharField(max_length=128)
    mother_group = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)  # blank is important: NULL in forms

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    notes = models.CharField(max_length=5000, blank=True, null=True)
    price = models.IntegerField()
    duration = models.IntegerField()
    booking_company = models.ManyToManyField(Company, through='Booking')
    group = models.ForeignKey(
        ServiceGroup, on_delete=models.PROTECT, null=True, blank=True)
    uuid = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)


class Booking(models.Model):
    uuid = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    assigned_employee = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # updated_by = models.ForeignKey(Responsible, on_delete=models.RESTRICT)
    notes = models.CharField(max_length=1000, null=True, blank=True)
    internal_notes = models.CharField(max_length=5000, null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    def com_name(self):
        return self.company.name

    def ser_name(self):
        return self.service.name


class CompanyChoiceField(ModelChoiceField):
    # overwritten this way, could also have been solved with __str__, but overwrites all(!) displays
    def label_from_instance(self, obj):
        return f"{ obj.name } in { obj.city }"


class EmployeeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{ obj.first_name } { obj.last_name }'
