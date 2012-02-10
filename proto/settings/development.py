import os

from proto.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'