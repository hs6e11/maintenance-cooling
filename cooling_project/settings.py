"""
Django settings for cooling_project project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import Csv, config
from dotenv import load_dotenv
import environ

load_dotenv


# env = environ.Env()
# environ.Env.read_env()
env_schema = dict(
    # DEBUG=(bool, False),
    # LANGUAGE_CODE=(str, 'en-us'),
    # TIME_ZONE=(str, 'UTC'),
    # USE_I18N=(bool, True),
    # USE_L10N=(bool, True),
    # USE_TZ=(bool, True),
    # STATIC_URL=(str, 'static/'),
    # LOGIN_URL=(str, 'login/'),
    # LOG_LEVEL=(str, 'INFO'),      
    # AUTHEN_SECRET_KEY=(str, 'RL72rg9bPzajnmwP9cB8vrKuJaIN6Iy6N99gncjD8QE='),
    # EMAIL_HOST=(str, 'localhost'),
    # EMAIL_PORT=(str, '1025'),
    # EMAIL_USE_TLS=(bool, False),
    # EMAIL_HOST_USER=(str, 'your-email@gmail.com'),
    # EMAIL_HOST_PASSWORD=(str, 'your-gmail-password'),
    # WEB_PROTOCAL=(str, 'http'),
    # WEB_DOMAIN_NAME=(str, 'localhost:8000'),
    # IMAGE_SECRET_KEY=(str, 'yqiLYf3TF44eJGUkF7adm0K8pWs9iKg62FI6Wkmj0to='),
    # LIMIT_LOGIN_FAILED_ATTEMPTS=(int, 5)
)

root = environ.Path(__file__) - 3
env_src_file = root('.env')
if os.path.exists(env_src_file):
    environ.Env.read_env(env_file=env_src_file)
env = environ.Env(**env_schema)
for key in env_schema:
    exec("{} = env('{}')".format(key, key))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

production_host = os.getenv('PRODUCTION_HOST')
ALLOWED_HOSTS = [production_host] if production_host is not None else []


# Application definition

INSTALLED_APPS = [
    'coolingapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
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

ROOT_URLCONF = 'cooling_project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'cooling_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# DEBUG=True
# DB_NAME=dbcoolingapp
# SECRET_KEY=django-insecure-h$q$n36sjg@^lyy$-zfe%#f!14)2b7b_#b#&)a-@)_mw^npr$4
# DB_USER=postgres
# DB_PASSWORD=1234
# DB_HOST=localhost
# DB_PORT=5434

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

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'coolingapp/static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

# Define the directory where uploaded media files will be stored.
# MEDIA_ROOT = os.path.join(BASE_DIR, 'coolingapp', 'media')
#Auth

AUTH_USER_MODEL = "coolingapp.CustomUser"

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"
LOGIN_URL = "coolingapp:login"
# settings.py

LOGIN_REDIRECT_URL = 'password_change_done'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Replace with your SMTP server address
EMAIL_PORT = 587  # Use the appropriate port for your SMTP server
EMAIL_USE_TLS = True  # Use TLS encryption (or EMAIL_USE_SSL = True for SSL)
EMAIL_HOST_USER = 'lignum.locus@gmail.com'
EMAIL_HOST_PASSWORD = 'lguldlagimrjagrd'  # Replace with your email password


# EAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_FILE_PATH = BASE_DIR / "test_inbox"
PASSWORD_RESET_TIMEOUT = 60


# PASSWORD_RESET_EMAIL_TEMPLATE = 'registration/password_reset_email.html'