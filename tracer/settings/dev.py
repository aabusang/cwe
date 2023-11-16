import os
from .base import * 

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = True

ALLOWED_HOSTS = [
    # 'cwe-development10.up.railway.app',
    # 'localhost',
    # '127.0.0.1',
    '*'
    ]

CSRF_TRUSTED_ORIGINS = [
    'https://cwe-development10.up.railway.app', 
    'https://cwe-testenv.up.railway.app',
    'https://cwe-production.up.railway.app',
    ]
