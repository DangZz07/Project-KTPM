from pathlib import Path
import os 

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1v+fbc!rdrq=tbamx4myhnd!#n4ww2rkq1##qqnoxy+xwubf7d'

DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'nmcnpmapp.SuperUser'

CORS_ALLOW_ALL_ORIGINS = True



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = "/" 

INSTALLED_APPS = [
    'unfold',
    'widget_tweaks',
    "unfold.contrib.filters",
    # 'django_admin_interface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nmcnpmapp',
    #...
    "admin_interface",
    "colorfield",
    #...
    #...
]
AUTHENTICATION_BACKENDS = [
    'nmcnpmapp.backends.MultiUserModelBackend',  # Custom backend for RoomUser and SuperUser
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

X_FRAME_OPTIONS = "SAMEORIGIN"              # allows you to use modals insated of popups
SILENCED_SYSTEM_CHECKS = ["security.W019"]  # ignores redundant warning messages

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # Bắt buộc
]

ROOT_URLCONF = 'myproject.urls'

LOGIN_REDIRECT_URL = 'home'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'nmcnpmapp/templates'],
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
TEMPLATE_LOADERS = ['apptemplates.Loader',]
WSGI_APPLICATION = 'myproject.wsgi.application'
# Ensure these settings are in your settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database-backed sessions
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keeps the session active after closing the browser

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CSRF_TRUSTED_ORIGINS = ['https://cf4532ce-9c5a-44a5-bee7-2dc6ef097c67-00-yqmj3xhjeze5.pike.replit.dev','https://serval-main-lizard.ngrok-free.app','https://33ac-2405-4802-1cdd-85d0-d99d-ec56-4ae6-952d.ngrok-free.app', 'https://78df-2401-d800-257-6fc-e8d9-70a5-94f0-cc63.ngrok-free.app']


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

LANGUAGE_CODE = 'vi'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / "nmcnpmapp/static"]
STATIC_ROOT = BASE_DIR / "nmcnpmapp/static"

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
