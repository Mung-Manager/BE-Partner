import os
import logging

from config.env import BASE_DIR, APPS_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env.partner"))

logger = logging.getLogger("django")

SECRET_KEY = "test"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# ==================================================================== #
#                     설치된 앱, 사용하는 앱 config                         #
# ==================================================================== #
LOCAL_APPS = [
    "mung_manager.common.apps.CommonConfig",
    "mung_manager.authentication.apps.AuthenticationConfig",
    "mung_manager.users.apps.UsersConfig",
    "mung_manager.pet_kindergardens.apps.PetKindergardensConfig",
    "mung_manager.files.apps.FilesConfig",
    "mung_manager.tickets.apps.TicketsConfig",
    "mung_manager.customers.apps.CustomersConfig",
    "mung_manager.reservations.apps.ReservationsConfig",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.APIProcessTimeMiddleware",
]

ROOT_URLCONF = "config.root_urls"

APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(APPS_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"

# Database
if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "password",
            "HOST": "postgres-db",
            "PORT": "5432",
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTH_USER_MODEL = "users.User"

APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Internationalization
LANGUAGE_CODE = "en-us"  # 언어 - 국가 설정

TIME_ZONE = "Asia/Seoul"  # 시간대 설정

USE_I18N = True  # 국제화

USE_L10N = True  # 지역화

USE_TZ = False  # 장고 시간대 사용 여부


# ==================================================================== #
#                  file system (static) config                         #
# ==================================================================== #
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/partner/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/partner/media/"

# ==================================================================== #
#                       DRF config                                     #
# ==================================================================== #
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("djangorestframework_camel_case.render.CamelCaseJSONRenderer",),
    "DEFAULT_PARSER_CLASSES": ("djangorestframework_camel_case.parser.CamelCaseJSONParser",),
    "EXCEPTION_HANDLER": "mung_manager.common.exception.exception_handler.default_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("mung_manager.common.authentication.CustomJWTAuthentication",),
}


# ==================================================================== #
#                       Logging config                                 #
# ==================================================================== #
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "django.server": {
            "format": "[%(asctime)s] %(levelname)s [PID: %(process)d - %(processName)s] | [TID: %(thread)d - %(threadName)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "django.server",
        },
        "file": {
            "level": "INFO",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,
            "formatter": "django.server",
        },
    },
    "loggers": {
        # "django": {
        #     "handlers": ["console", "file"],
        #     "level": "INFO",
        # },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

from config.settings.cors import *  # noqa
from config.settings.oauth import *  # noqa
from config.settings.jwt import *  # noqa
from config.settings.files_and_storages import *  # noqa

from config.settings.debug_toolbar.settings import *  # noqa
from config.settings.debug_toolbar.setup import DebugToolbarSetup  # noqa
from config.settings.swagger.settings import *  # noqa
from config.settings.swagger.setup import SwaggerSetup  # noqa

INSTALLED_APPS, MIDDLEWARE = DebugToolbarSetup.do_settings(INSTALLED_APPS, MIDDLEWARE)
INSTALLED_APPS = SwaggerSetup.do_settings(INSTALLED_APPS)
