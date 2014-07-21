import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import sys


def pytest_collection_modifyitems(items):
    pass


def pytest_configure(config):
    here = os.path.dirname(__file__)
    sys.path.insert(0, here)
    from django.conf import settings

    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    import django
    if django.VERSION[:2] >= [1, 7]:
        from django.apps import AppConfig

        settings.INSTALLED_APPS = ['django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   # 'django.contrib.sites',
                                   #               'django.contrib.messages',
                                   #               'django.contrib.staticfiles',
                                   'django.contrib.admin.apps.SimpleAdminConfig',
                                   # 'south',
                                   # 'modeltranslation',
                                   'geo.apps.GeoConfig']
        django.setup()


def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('concurrency')

    sys.exit(pytest.main(args))


if __name__ == '__main__':
    runtests(sys.argv)
