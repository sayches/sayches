
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import sys
from .celery_beat import setup_periodic_tasks

DEBUG = os.environ.get('DEBUG')
if eval(DEBUG) == True:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery('config',)
app.config_from_object('django.conf:settings')
dirspot = os.getcwd()


sas = sys.path.append(os.path.join(os.getcwd(), "sayches"))
app.autodiscover_tasks(sas)
TASK_SERIALIZER = 'json'
setup_periodic_tasks(app)
