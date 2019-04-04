import os
from celery import Celery 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','bodhiai.settings')

app =\
        Celery('bodhiai',backend='redis://localhost',broker='amqp://')
app.config_from_object('django.conf:settings',namespace='CELERY')
app.autodiscover_tasks()

