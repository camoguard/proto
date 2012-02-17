from proto.settings.base import *

from S3 import CallingFormat


DEBUG = False
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = not DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"),
    },
}

STATIC_URL = 'http://cbsi-proto.s3.amazonaws.com/'
COMPRESS_URL = STATIC_URL
STATICFILES_STORAGE = 'proto.core.storage.CachedS3BotoStorage'
COMPRESS_STORAGE = STATICFILES_STORAGE

MEDIA_ROOT = 'http://cbsi-proto.s3.amazonaws.com/'
MEDIA_URL = 'http://cbsi-proto.s3.amazonaws.com/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
FILEBROWSER_DIRECTORY = ''

ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

AWS_ACCESS_KEY_ID = 'AKIAJZFJLRNQNCJWGHIQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'cbsi-proto'
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
