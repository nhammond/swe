#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Django settings for swe project.
import os
import sys

RACK_ENV=os.environ['RACK_ENV'] #development, staging, production

BLOCK_SERVICE = False #unless True in environment
try:
    b = (os.environ['BLOCK_SERVICE'].upper()=='TRUE')
    BLOCK_SERVICE = b
except KeyError:
    pass

DEBUG = False #unless True in environment
try:
    d = (os.environ['DEBUG'].upper()=='TRUE')
    DEBUG = d
except KeyError:
    pass

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Nathan Hammond', 'support@sciencewritingexperts.com'),
    )

MANAGERS = ADMINS

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'
            }
        }
else:
    if RACK_ENV=='development':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'swe',                      # Or path to database file if using sqlite3.
                'USER': os.environ['PSQL_USER'],                      # Not used with sqlite3.
                'PASSWORD': os.environ['PSQL_PASSWORD'],                  # Not used with sqlite3.
                'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
                }
            }
    else:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(),
            }

TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
LOCALES = (
    #English
    ('en', u'English'),
    #Simplified Chinese
    ('zh-cn', u'简体中文'),
)
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/login/'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_URL = os.environ['ROOT_URL']

GEOIP_PATH = os.path.join(ROOT_DIR, 'geoip/')

STATICFILES_DIRS = (
    os.path.join(ROOT_DIR, 'static/'),
    )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

LOCAL_STORAGE = False
try:
    l = (os.environ['LOCAL_STORAGE'].upper()=='TRUE')
    LOCAL_STORAGE = l
except KeyError:
    pass


if LOCAL_STORAGE:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles/')
    STATICFILES_DIRS = [
        os.path.join(ROOT_DIR, 'static/')
        ]
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(ROOT_DIR,'media/')

else:
#    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
#    MEDIA_URL = 'http://'+AWS_STORAGE_BUCKET_NAME+'.s3.amazonaws.com/'
    STATIC_URL = 'http://'+AWS_STORAGE_BUCKET_NAME+'.s3.amazonaws.com/'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

try:
    GOOGLE_TRACKING_ID=os.environ['GOOGLE_TRACKING_ID']
except KeyError:
    GOOGLE_TRACKING_ID=None

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

PAYPAL_RECEIVER_EMAIL = os.environ['PAYPAL_RECEIVER_EMAIL']

CUSTOMER_SERVICE_NAME = "Nathan Hammond"
CUSTOMER_SERVICE_TITLE = "Managing Editor"

CONTENT_TYPES = ['text']
# 2.5MB - 2621440; 5MB - 5242880; 10MB - 10485760; 20MB - 20971520; 50MB - 5242880
# 100MB 104857600; 250MB - 214958080; 500MB - 429916160
MAX_UPLOAD_SIZE = "104857600"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9e$#^u)-7xkr8w0=qi**o*p&amp;pe!f*l#0st@bmul2invw*incc='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'swe.context_processors.global_context',
    )

TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'templates'),
    os.path.join(ROOT_DIR, 'templates', 'email'),
    os.path.join(ROOT_DIR, 'templates', 'errors'),
    )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'paypal.standard.ipn',
    'sendgrid',
    'storages',
    'south',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'swe',
    'coupons',
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

