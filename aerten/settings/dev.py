from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dle3w*fcqaf40p9&+@+@!ixx7czyu)gfng#@0s%k-d!hw1sl#n'



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

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