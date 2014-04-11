"""
Django settings for infohub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from configparser import RawConfigParser
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

config = RawConfigParser()
config.optionxform = str
config.read(BASE_DIR + '/infohub/settings.ini')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secrets','SECRET_KEY')
SESSION_COOKIE_SECURE = config.getboolean('secrets','SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = config.getboolean('secrets','CSRF_COOKIE_SECURE')
SESSION_EXPIRE_AT_BROWSER_CLOSE = config.getboolean('secrets','SESSION_EXPIRE_AT_BROWSER_CLOSE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('debug','DEBUG')
TEMPLATE_DEBUG = config.getboolean('debug','TEMPLATE_DEBUG')

ALLOWED_HOSTS = config.get('host','ALLOWED_HOSTS').split()
ADMINS = tuple(config.items('admins'))


# Application definition
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'south',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'infohub.urls'
WSGI_APPLICATION = 'infohub.wsgi.application'


# Database
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'assets'),
)
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Templates
TEMPLATE_DIRS = (
	os.path.join(BASE_DIR, 'templates'),
)
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
)