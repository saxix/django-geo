import os
from tempfile import mktemp

GEO_CACHE = '~build/cache'

DEBUG = True
STATIC_URL = '/static/'

SITE_ID = 1
ROOT_URLCONF = 'tests.urls'
SECRET_KEY = 'abc'
STATIC_ROOT = mktemp('static')
MEDIA_ROOT = mktemp('media')

gettext = lambda s: s
LANGUAGES = (
    ('de', gettext('German')),
    ('en', gettext('English')),
)

INSTALLED_APPS = ['django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.admin',
                  'south',
                  'modeltranslation',
                  'geo']

TEMPLATE_DIRS = ['tests/templates']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format': '%(levelname)-8s: %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '%(levelname)-8s: %(asctime)s %(name)-25s %(message)s'
        },
        'simple': {
            'format': '%(levelname)-8s %(asctime)s %(name)-25s %(funcName)s %(message)s'
        },
        'debug': {
            'format': '%(levelno)s:%(levelname)-8s %(name)s %(funcName)s:%(lineno)s:: %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug'
        }
    },
    'loggers': {
        'concurrency': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG'
        }
    }
}

DBNAME = os.environ.get('DBNAME', 'geo')
db = os.environ.get('DBENGINE', None)
if db == 'pg':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DBNAME,
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'postgres',
            'PASSWORD': ''}}
elif db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DBNAME,
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'root',
            'PASSWORD': '',
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci'}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '%s.sqlite' % DBNAME,
            'HOST': '',
            'PORT': ''}}
