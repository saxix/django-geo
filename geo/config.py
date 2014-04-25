from __future__ import absolute_import, unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import get_callable
from django.db.models import Model
from django.utils import six
from django.test.signals import setting_changed
import os


class AppSettings(object):
    """
    Class to manage application related settings
    How to use:

    >>> from django.conf import settings
    >>> settings.APP_OVERRIDE = 'overridden'
    >>> settings.MYAPP_CALLBACK = 100
    >>> class MySettings(AppSettings):
    ...     defaults = {'ENTRY1': 'abc', 'ENTRY2': 123, 'OVERRIDE': None, 'CALLBACK':10}
    ...     def set_CALLBACK(self, value):
    ...         setattr(self, 'CALLBACK', value*2)

    >>> conf = MySettings("APP")
    >>> conf.ENTRY1, settings.APP_ENTRY1
    ('abc', 'abc')
    >>> conf.OVERRIDE, settings.APP_OVERRIDE
    ('overridden', 'overridden')

    >>> conf = MySettings("MYAPP")
    >>> conf.ENTRY2, settings.MYAPP_ENTRY2
    (123, 123)
    >>> conf = MySettings("MYAPP")
    >>> conf.CALLBACK
    200

    """
    defaults = {
        'CACHE': './cache',
        'DATA': os.path.join(os.path.dirname(__file__), 'data'),
        'LOAD_CURRENCY_FUNC': 'geo.loaders.load_currency',
        'LOAD_COUNTRY_FUNC': 'geo.loaders.load_country',
    }

    def __init__(self, prefix):
        """
        Loads our settings from django.conf.settings, applying defaults for any
        that are omitted.
        """
        self.prefix = prefix
        from django.conf import settings

        for name, default in self.defaults.items():
            prefix_name = (self.prefix + '_' + name).upper()
            value = getattr(settings, prefix_name, default)
            self._set_attr(prefix_name, value)
            setattr(settings, prefix_name, value)
            setting_changed.send(self.__class__, setting=prefix_name, value=value, enter=True)

        setting_changed.connect(self._handler)
        if not os.path.isdir(self.CACHE):
            raise ImproperlyConfigured('%s is not a valid directory. Please change `settings.GEO_CACHE` value or create it', self.CACHE)

    def _set_attr(self, prefix_name, value):
        name = prefix_name[len(self.prefix) + 1:]
        if name == 'CACHE':
            value = os.path.abspath(os.path.expanduser(value))
        elif name == 'DATA':
            value = os.path.abspath(os.path.expanduser(value))

        setattr(self, name, value)

    def _handler(self, sender, setting, value, **kwargs):
        """
            handler for ``setting_changed`` signal.

        @see :ref:`django:setting-changed`_
        """
        if setting.startswith(self.prefix):
            self._set_attr(setting, value)


conf = AppSettings('GEO')
try:
    from django.apps import AppConfig

    class GeoConfig(AppConfig):
        pass
except ImportError:
    pass
