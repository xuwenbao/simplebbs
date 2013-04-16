from mongoengine import connect

from settings_base import *

DEBUG = False

connect('simplebbs')

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'simplebbsmail@gmail.com'
EMAIL_HOST_PASSWORD = 'simplebbs'
EMAIL_PORT = 587
