# Generated by Django 3.1.7 on 2021-03-29 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_booking_assigned_employee'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='booking',
        #     name='updated',
        # ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]