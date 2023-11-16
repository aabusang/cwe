import os
from .base import *


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

SECRET_KEY = os.environ['SECRET_CWE_KEY']

DEBUG = False

ALLOWED_HOSTS = [
    # 'cwe-development10.up.railway.app',
    # 'cwe-production.up.railway.app',
    # 'localhost',
    # '127.0.0.1',
    '*'
    ]