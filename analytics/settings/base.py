"""
Django settings for analytics project.

This application is the upgrade version from django 1.6.x on python2.7
to Django 1.11.x on Python 3.6.x

For more information on this file, see 
https://github.com/llcit/clt-analytics-dev-py
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configparser import RawConfigParser
config = RawConfigParser()

#Copy the server.conf.eaxmple to server.conf and add server's information
config.read(os.path.join(BASE_DIR,'analytics/settings/server.conf'))

# Secret key stored in your local environment variable not here.
SECRET_KEY = config.get('secrets', 'SECRET_KEY')

"""
Use the DEBUG option to check it is production or not
If the DEBUG is True, then it is not production server.
Check and configure the debug section of 'server.conf' file correctly.
"""
DEBUG = config.get('debug', 'DEBUG')

# SSL/HTTPS
if DEBUG:
    CSRF_COOKIE_SECURE=False
    SECURE_SSL_REDIRECT = False
else:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [config.get('hosts', 'HOST1'),]

# ! SACRED DO NOT EDIT THESE IN DEVELOPMENT!
SITE_ROOT = config.get('site', 'SITE_ROOT')
SITE_NAME = config.get('site', 'SITE_NAME')
SITE_HOST = config.get('site', 'SITE_HOST')
DOC_ROOT = config.get('site', 'DOC_ROOT')

SITE_ID = 1


AUTH_PROFILE_MODULE = 'review.UserProfile'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    
    'django_cas_ng',
    'review',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    

    # Uncomment to use CAS 3 authentication at UH
    #'django_cas.middleware.CASMiddleware',
]

ROOT_URLCONF = 'analytics.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'review/templates'),
                 os.path.join(BASE_DIR, 'analytics/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # Added to allow access to SITE_ROOT parameter in templates
                'analytics.analytics_context_processors.site_root',
            ],
        },
    },
]

WSGI_APPLICATION = 'analytics.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'DATABASE_ENGINE'),
        'NAME': config.get('database', 'DATABASE_NAME'),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': config.get('database', 'DATABASE_HOST'),
        'PORT': config.get('database', 'DATABASE_PORT'),
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
TIME_ZONE = 'Pacific/Honolulu'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Project staticfiles directory
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "analytics/static"),
        os.path.join(BASE_DIR, "review/static"),
    ]

# Production staticfiles directory    
STATIC_URL = '/static/analytics/'
MEDIA_URL = '/media/analytics/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/analytics')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/analytics')

# Login with CAS
LOGIN_REDIRECT_URL = config.get('cas', 'LOGIN_REDIRECT_URL')
LOGIN_URL = config.get('cas', 'LOGIN_URL')
CAS_SERVER_URL = config.get('cas', 'CAS_SERVER_URL')
CAS_REDIRECT_URL = config.get('cas', 'CAS_REDIRECT_URL')
CAS_VERSION = config.get('cas', 'CAS_VERSION')

