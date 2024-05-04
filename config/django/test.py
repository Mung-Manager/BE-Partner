from config.django.base import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "github_actions",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "postgres-db",
        "PORT": "5432",
        "CONN_MAX_AGE": 60,
    }
}