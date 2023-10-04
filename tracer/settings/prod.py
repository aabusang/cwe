import os
from .base import *


SECRET_KEY = os.environ['SECRET_CWE_KEY']

DEBUG = False

ALLOWED_HOSTS = ['localhost', 'cwe-development10.up.railway.app', 'cwe-production.up.railway.app']

# DATABASES = {
#         'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ['PGDATABASE'],
#         'USER': os.environ['PGUSER'],
#         'PASSWORD': os.environ['PGPASSWORD'],
#         'HOST': os.environ['PGHOST'],
#         'PORT': os.environ['PGPORT'],
#     },
# }