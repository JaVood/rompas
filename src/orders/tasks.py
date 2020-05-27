from celery import task
from django.core.mail import send_mail
from celery import Celery


app = Celery('tasks', backend='amqp', broker='amqp://guest:guest@localhost:5672//')
