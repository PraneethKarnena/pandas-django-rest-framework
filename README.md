# Pandas - Django Rest Framework

A Django API project built using Django Rest Framework for demonstrating basic usage of Pandas.

## Features:

- Upload a dataset
- Extract dataset details
- Export dataframe as excel
- Export stats
- Plot histogram

## Run:

This project depends on Celery and RabbitMQ. Please follow the links below for configuration:

- http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
- http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html

* Clone - `git clone`

* Set environment variables from `ENV_VARS.txt` file

* Install requirements - `pip install -r requirements.txt`

* Run database ops:
    - `python manage.py makemigrations`
    - `python manage.py migrate`

* Run the server: `python manage.py runserver`
