from proto.settings.base import *


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
STATICFILES_STORAGE = 'proto.common.storage.CachedS3BotoStorage'
COMPRESS_STORAGE = STATICFILES_STORAGE

MEDIA_ROOT = 'http://cbsi-proto.s3.amazonaws.com/uploads/'
MEDIA_URL = 'http://cbsi-proto.s3.amazonaws.com/uploads/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
FILEBROWSER_DIRECTORY = ''

ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'

AWS_ACCESS_KEY_ID = 'AKIAJZFJLRNQNCJWGHIQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'cbsi-proto'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
