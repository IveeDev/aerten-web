import os
from .common import *


SECRET_KEY =  'django-insecure-dle3w*fcqaf40p9&+@+@!ixx7czyu)gfng#@0s%k-d!hw1sl#n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aerten',
        'USER': 'root',
        'HOST': 'localhost',
        'PASSWORD': 'iviidev',
        'PORT': '3306',
        'TEST': {
            'NAME': 'test_aerten',  # Explicitly set the test database name
        },

    }
}