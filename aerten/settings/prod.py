import os
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-local-secret-key')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aerten',  # Your local database name
        'USER': 'root',  # Your local MySQL username
        'PASSWORD': 'iviidev',  # Your local MySQL password
        'HOST': 'localhost',  # Connect to MySQL locally
        'PORT': '3306',
    }
}
