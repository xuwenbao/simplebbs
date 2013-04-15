from mongoengine import connect

from settings_base import *

DEBUG = False

connect('simplebbs')

SESSION_ENGINE = 'django.contrib.sessions.backends.file'