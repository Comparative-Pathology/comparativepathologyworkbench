#!/usr/bin/python3
###!
# \file         settings.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
# This exposes the WSGI callable as a module-level variable named
# ``application``. from "config.settings"
###
"""
Django settings for comparativepathologyworkbench project.
"""
import os

from decouple import config, Csv

import dj_database_url


from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

	'widget_tweaks',
    'rest_framework',
    'sortable_listview',
    'ckeditor',
    'inlineedit',

    'matrices.apps.MatricesConfig',
    'rest_framework.authtoken',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#
# UNCOMMENT for LIVE Server Configuration Settings
#
#ROOT_URLCONF = 'comparativepathologyworkbench.urls'

#
# UNCOMMENT for DEVELOPMENT Server Configuration Settings
#
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# These lines ensure all static files - CSS, images etc - come from a SINGLE base level
#  folder in the application

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Other stuff for the CPW

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
NOT_EMAIL_HOST_PASSWORD = config('NOT_EMAIL_HOST_PASSWORD')

#
# UNCOMMENT for LIVE Server Mailer
#
#EMAIL_HOST = config('EMAIL_HOST')
#EMAIL_PORT = config('EMAIL_PORT', cast=int)
#EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

#EMAIL_HOST_USER = config('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

#
# UNCOMMENT for DEVELOPMENT Server Mailer to File
#
EMAIL_FILE_PATH = config('EMAIL_FILE_PATH')
EMAIL_BACKEND = config('EMAIL_BACKEND')


LOCATION = config('LOCATION')

SETTINGS_EXPORT = [
    'LOCATION',
    'DEBUG',
]

# Django REST Framework
REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',

    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}

SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', cast=int)
SESSION_EXPIRE_AT_BROWSER_CLOSE = config('SESSION_EXPIRE_AT_BROWSER_CLOSE', cast=bool)


# CKEditor settings
#

import ckeditor.configs

CKEDITOR_CONFIGS = {
    "default": ckeditor.configs.DEFAULT_CONFIG,
    "empty_toolbar": {
        "toolbar": "Empty",
        "toolbar_Empty": []
    }
}


# Django Inlineedit settings
#

# This setting controls default editing access within Django-inlineedit
# In this case we are enabling editing to anyone using the example
INLINEEDIT_EDIT_ACCESS = lambda user, model, field: True

# Two custom adaptors are being registered below
INLINEEDIT_ADAPTORS = {
    "blocked": "matrices.adaptors.BlockedAdaptor",
}

# HighCharts Settings
#

HIGHCHARTS_TEMP_DIR = config('HIGHCHARTS_TEMP_DIR')
HIGHCHARTS_OUTPUT_DIR = config('HIGHCHARTS_OUTPUT_DIR')
HIGHCHARTS_HOST = config('HIGHCHARTS_HOST')
HIGHCHARTS_OUTPUT_WEB = config('HIGHCHARTS_OUTPUT_WEB')

# EBI SCA Settings
#

EBI_SCA_EXPERIMENTS_URL = config('EBI_SCA_EXPERIMENTS_URL')
