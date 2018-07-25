import os
import dj_database_url
import sys
import whitenoise
import chartkick

# When Tests Are Being Run
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Displays Errors In Development Mode
if os.environ.get('DEVELOPMENT'):
    development = True
    
else:
    development = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

#Debug mode is dependent on development variable
DEBUG = development

ALLOWED_HOSTS = [os.environ.get('C9_HOSTNAME'), os.environ.get('HOSTNAME')]

host = os.environ.get('SITE_HOST')
if host: 
    ALLOWED_HOSTS.append(host)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_forms_bootstrap',
    'accounts',
    'tickets',
    'graphs',
    'chartkick',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
]

ROOT_URLCONF = 'issuetracker.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'issuetracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# Use sqlite when testing otherwise use Heroku postgres database

if TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }

else:
    DATABASES = {
         'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL'))}


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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# Static Files Directory
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    chartkick.js(),
    os.path.join(BASE_DIR, "static"),
    ]
    
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Email Host Settings
EMAIL_HOST ='smtp.gmail.com'
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# STRIPE Keys
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE')
STRIPE_SECRET = os.getenv('STRIPE_SECRET')

# Custom Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.EmailAuth'
]