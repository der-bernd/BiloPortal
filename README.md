# BiloPortal

This is an hybrid of a portal and a webshop to enable customers of the company the booking of services, creating of employees, that stuff.

##### Requirements:
Python > 3.0 installed
- Getting started: https://www.python.org/about/gettingstarted/
- Directly to download page: https://www.python.org/downloads/

Django installed:
- To get started, visit https://www.djangoproject.com/start/

Some python packages:
- pandas
- dateutil
- mysqlclient
- django-multiselectfield

Setup: (ref: [https://stackoverflow.com/questions/29888046/django-1-8-create-initial-migrations-for-existing-schema])
+ create database bilobit_portal
+ create user bilobit-portal-admin an grant all privileges to bilobit_portal
+ try makemigrations and migrate

or
delete migrations folder of each app
reset migrations of built-in apps, so run for each built_in app:
``python manage.py migrate <app_name> zero``

ref: [https://www.delftstack.com/howto/django/django-reset-migrations/]

make new migrations for each app:
``py manage.py makemigrations <app_name>``
**Please do this in following order: auth, portal, accounts, info_pages, admin, frontend_admin**`

final step: py manage.py migrate --fake-initial (when failing, try using --fake instead)

make sure normal migrating works, run without --fake-initial again



XAMPP or other local server with MySQL running, creds are expected as constants in bilobit_portal/auth/db.py, see settings.py for which data is needed

**Please do make migrations and migrate after settings the credentials!**

And you will need lots of motivation. Have fun with it!
