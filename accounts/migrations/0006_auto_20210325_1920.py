# Generated by Django 3.1.7 on 2021-03-25 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_responsible_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsible',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Admin'),
        ),
    ]
