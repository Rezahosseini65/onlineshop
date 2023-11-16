from .common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'daphne',
    'drf_spectacular',
]+INSTALLED_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'onlineshop',
        'USER': 'onlineshop',
        'PASSWORD': '123@456',
        'HOST': 'db',
        'PORT': '5432',
    }
}