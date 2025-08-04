from pathlib import Path

from decouple import config, Csv
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent


# Development settings.
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:8000',
    cast=Csv()
)

# Application definition.

MY_APPS = [
    # Created apps go here.
    'core',
    'accounts',
]

THIRD_PARTY_APPS = [
    # Installed third-party apps go here.
    'polymorphic',
    'django_bootstrap5',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = MY_APPS + THIRD_PARTY_APPS + DJANGO_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'commonplace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # My context processors.
                'core.processors.context',
            ],
        },
    },
]

WSGI_APPLICATION = 'commonplace.wsgi.application'


# Database.
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=config('DB_SSL_REQUIRE', default=False, cast=bool)
    )
}


# Password validation.
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization.
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images).
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'


# Default primary key field type.
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Deployment settings (if using WhiteNoise).

ENABLE_WHITENOISE = config('ENABLE_WHITENOISE', default=False, cast=bool)

if ENABLE_WHITENOISE:
    try:
        STATIC_ROOT = BASE_DIR / 'staticfiles'
        MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    except ImportError:
        raise ImportError("ENABLE_WHITENOISE is True but whitenoise package is not installed.")


# My settings.

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:index'
LOGOUT_REDIRECT_URL = 'core:index'
