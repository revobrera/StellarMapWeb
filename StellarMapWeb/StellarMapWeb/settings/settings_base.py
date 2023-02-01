"""
Django settings for StellarMapWeb project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import sys
from pathlib import Path

from cassandra import ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.71,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    environment=config('ENV'),
    _experiments={
        "profiles_sample_rate": 1.0,
    }
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Calculate the path to the root directory of the Django project
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Redirect all HTTP requests to HTTP
SECURE_SSL_REDIRECT = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cassandra_engine',
    'django_cassandra_engine.sessions',
    'rest_framework',
    'apiApp',
    'radialTidyTreeApp',
    'rest_framework_swagger',
    'webApp',
]

SESSION_ENGINE = 'django_cassandra_engine.sessions.backends.db'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StellarMapWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'StellarMapWeb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Cassandra database settings
CASSANDRA_DB_NAME = config('CASSANDRA_DB_NAME')
CASSANDRA_USERNAME = config('CASSANDRA_USERNAME')
CASSANDRA_PASSWORD = config('CASSANDRA_PASSWORD')
CASSANDRA_HOST = config('CASSANDRA_HOST')
CASSANDRA_REPLICATION_STRATEGY = config('CASSANDRA_REPLICATION_STRATEGY')
CASSANDRA_REPLICATION_FACTOR = config('CASSANDRA_REPLICATION_FACTOR')
CLIENT_ID=config('CLIENT_ID')
CLIENT_SECRET=config('CLIENT_SECRET')
ASTRA_DB_ID=config('ASTRA_DB_ID')
ASTRA_DB_APPLICATION_TOKEN=config('ASTRA_DB_APPLICATION_TOKEN')

# Controls the fallback behavior when sorting query results.
# It's worth mentioning that when this option is set to true, 
# it will increase the time of execution and also it will 
# consume a lot of memory, also it's not recommended to 
# use it on large datasets.
CASSANDRA_FALLBACK_ORDER_BY_PYTHON = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/'.join([str(BASE_DIR), 'db.sqlite3']),
        'SUPPORTS_TRANSACTIONS': True,
    },
    'cassandra': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': CASSANDRA_DB_NAME,
        'TEST_NAME': 'test_db',
        'OPTIONS': {
            'replication': {
                'strategy_class': CASSANDRA_REPLICATION_STRATEGY,
                'replication_factor': CASSANDRA_REPLICATION_FACTOR
            },
            'connection': {
                'auth_provider': PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET),
                'cloud': {
                    'secure_connect_bundle': os.path.join(BASE_DIR, 'secure-connect-stellarmapdb.zip'),
                },
                'consistency': ConsistencyLevel.LOCAL_ONE,
                'retry_connect': True
                # + All connection options for cassandra.cluster.Cluster()
            },
            'session': {
                'default_timeout': 10,
                'default_fetch_size': 10000
                # + All options for cassandra.cluster.Session()
            }
        },
        'SUPPORTS_TRANSACTIONS': True,
    }
}

DATABASE_APPS_MAPPING = {
    'apiApp': 'cassandra',
    'radialTidyTreeApp': 'internal',
    'webApp': 'internal'
}

DATABASE_ROUTERS = ['StellarMapWeb.router.DatabaseAppsRouter']

TEST_RUNNER = 'StellarMapWeb.testrunner.NoDbTestRunner'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# default static files settings for PythonAnywhere.
# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
MEDIA_ROOT = '/home/revobrera/StellarMapWeb/StellarMapWeb/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/revobrera/StellarMapWeb/StellarMapWeb/static'
STATIC_URL = '/static/'

VENV_PATH = os.path.dirname(BASE_DIR)

# load static files
STATICFILES_DIRS = [
    os.path.join(VENV_PATH, 'static'),
    os.path.join(VENV_PATH, "webApp"),
    os.path.join(VENV_PATH, "radialTidyTreeApp"),
]

#STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/stellarmap/django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# swagger
REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema' }

# control how long your Django app's pages are cached by client browsers.
# setting to 0 will not cache pages by client browsers.
CACHE_MIDDLEWARE_SECONDS = 0
