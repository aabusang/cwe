import os
from .base import * 

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = True

ALLOWED_HOSTS = ['localhost']