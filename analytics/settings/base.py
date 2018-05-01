# Django settings for analytics project.
# LOCAL HOST TEST SETTINGS. WILL NOT WORK ON PRODUCTION SERVER!
import os
from unipath import Path
PROJECT_DIR = Path(__file__).ancestor(3) # Points to top level directory

DEBUG = False

ADMINS = (
    ('CLT IT ADMIN', 'llcit@hawaii.edu'),
)

MANAGERS = ADMINS

AUTH_PROFILE_MODULE = 'review.UserProfile'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Pacific/Honolulu'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = os.path.join(DOC_ROOT, 'media/analytics/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = os.path.join(SITE_HOST, 'media/analytics/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = os.path.join(DOC_ROOT, 'static/analytics')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = os.path.join(PROJECT_DIR, '/static/analytics/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'analytics/static'),
    os.path.join(PROJECT_DIR, 'review/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                os.path.join(PROJECT_DIR, 'review/templates'),
                os.path.join(PROJECT_DIR, 'analytics/templates'),
            ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                "django.template.context_processors.debug",
                'django.template.context_processors.request',
                "django.contrib.auth.context_processors.auth",
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",

                # Added to allow access to SITE_ROOT parameter in templates
                'analytics.analytics_context_processors.site_root',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            #     'django.template.loaders.eggs.Loader',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Uncomment to use CAS 3 authentication at UH
    #'django_cas.middleware.CASMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
     'django.contrib.auth.backends.ModelBackend',
     'django_cas_ng.backends.CASBackend',
)
# set CAS SERVER FIRST
CAS_SERVER_URL = 'https://cas-test.its.hawaii.edu/cas/login'
# set CAS VERSION: default is CAS2
CAS_VERSION = 'CAS_2_SAML_1_0'
# set redirection after login
CAS_REDIRECT_URL = '/'

ROOT_URLCONF = 'analytics.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'analytics.wsgi.application'

# TEMPLATE_DIRS = (
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#     os.path.join(PROJECT_DIR, 'review/templates'),
#     os.path.join(PROJECT_DIR, 'analytics/templates'),
# )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django_cas_ng',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'review',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# LOGIN_REDIRECT_URL = '%s/review'%(SITE_ROOT)                          #'/review'
# LOGIN_URL = '%s/accounts/login' %(SITE_ROOT)            #'/accounts/login'
