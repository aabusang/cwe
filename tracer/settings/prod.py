import os
from .base import *


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['cwe-production.up.railway.app']