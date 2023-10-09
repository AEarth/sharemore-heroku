"""
Django settings for sharemore project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

enviro_set = 'prod'

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com', '.share-more.org' ]

LOGIN_REDIRECT_URL = 'myaccount'
LOGOUT_REDIRECT_URL = 'frontpage'
CART_SESSION_ID = 'cart'
SESSION_COOKIE_AGE = 86400

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', #whitenoise setting
    'django.contrib.staticfiles',
    'core',
    'userprofile',
    'store',
    'django_htmx',
    'django_fsm',
    'django_extensions',    
    # 'simple_deploy', 
]

# NPM_BIN_PATH = r"C:\Users\Arthur\AppData\Roaming\npm"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'threadlocals.middleware.ThreadLocalMiddleware', # custom threadlocals middleware
    #'sharemore.middleware.CurrentUserMiddleware', # custom current user middleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     "django_htmx.middleware.HtmxMiddleware",
]    

if enviro_set == 'local':
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]



ROOT_URLCONF = 'sharemore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'string_if_invalid': 'INVALID VAR/EXP: %s', #added this for debug not production
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # my additions
                'core.context_processors.navigation',
                'core.context_processors.base_bell'
            ],
            
        },
    },
]

WSGI_APPLICATION = 'sharemore.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_prod') #tells ngix where to find static files. this is useless in dev only required for deployment

STATICFILES_DIRS = [BASE_DIR / "static"] #provides additional directories for collectstatic to look for static files

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}


INTERNAL_IPS = [
    "127.0.0.1",
]


if enviro_set == 'local':
    print("Running Local Apps")
    INSTALLED_APPS.insert(4,'livereload')
    MIDDLEWARE += ['livereload.middleware.LiveReloadScript',]
    
test='test'

import os
if 'ON_HEROKU' in os.environ:
    ALLOWED_HOSTS.append('sharemore1-*.herokuapp.com')
    #import dj_database_url
    #DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
    i = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
    MIDDLEWARE.insert(i + 1, "whitenoise.middleware.WhiteNoiseMiddleware")
    DEBUG = os.getenv('DEBUG') == 'TRUE'
    SECRET_KEY = os.getenv('SECRET_KEY')
