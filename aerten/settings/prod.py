import os
from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['web-xa1s8fkrksww.up-de-fra1-k8s-1.apps.run-on-seenode.com', '127.0.0.1', 'localhost', 'apable-rolypoly-a4e40e.netlify.app']



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('NAME'),
        'USER': os.environ.get('USER'),
        'HOST': os.environ.get('HOST'),
        'PASSWORD': os.environ.get('PASSWORD'),
        'PORT': '11550',
    }
}


CORS_ALLOWED_ORIGINS = ["https://web-xa1s8fkrksww.up-de-fra1-k8s-1.apps.run-on-seenode.com", "https://capable-rolypoly-a4e40e.netlify.app", "http://localhost:5173"]