# dev.py
from .base import *

SITE_ROOT = ''
SITE_NAME = 'Teaching Analytics @ the Center for Language & Technology'
SITE_HOST = 'http://localhost:8000'

# Secret key stored in your local environment variable not here.
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'analyticstestdb', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Append apps used in development not production.
INSTALLED_APPS += (
    'debug_toolbar',
)

LOGIN_URL = 'login-select'
