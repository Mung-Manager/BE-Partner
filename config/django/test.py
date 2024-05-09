from config.env import env
from config.django.base import *  # noqa
import platform

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("TEST_POSTGRESQL_DATABASE", default="github_actions"),
        "USER": env("TEST_POSTGRESQL_USER", default="postgres"),
        "PASSWORD": env("TEST_POSTGRESQL_PASSWORD", default="password"),
        "HOST": env("TEST_POSTGRESQL_HOST", default="postgres-db"),
        "PORT": env("TEST_POSTGRESQL_PORT", default="5432"),
        "CONN_MAX_AGE": 60,
    }
}


if platform.system() == "Darwin":
    GEOS_LIBRARY_PATH = env.str("GEOS_LIBRARY_PATH")
    GDAL_LIBRARY_PATH = env.str("GDAL_LIBRARY_PATH")
