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

    try:
        from django.apps import AppConfig
        import django

        django.setup()
    except ImportError:
        pass


def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('concurrency')

    sys.exit(pytest.main(args))


if __name__ == '__main__':
    runtests(sys.argv)
