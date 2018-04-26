# dev.py
from .base import *

SITE_ROOT = ''
SITE_NAME = 'Teaching Analytics @ the Center for Language & Technology'
SITE_HOST = 'http://localhost:8000'

# Secret key stored in your local environment variable not here.
try:
    # PRODUCTION SHOULD use this 'SECRET_KEY'!!!
    SECRET_KEY = os.environ['SECRET_KEY']
except:
    # DO NOT USE THIS 'SECRET_KEY' because it is a sample and published in the github repo.
    SECRET_KEY =['5jrad@)cbj&af%a3h8l#0+086x%b)4u)7$+2=5)#pu$&u*tk=e']

DEBUG = True

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

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

LOGIN_URL = 'login-screen'
