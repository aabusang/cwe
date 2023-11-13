import os
from .base import * 

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'https://cwe-development10.up.railway.app']
# CSRF_TRUSTED_ORIGINS = ['https://cwe-development10.up.railway.app']
