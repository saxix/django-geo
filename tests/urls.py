from django.contrib import admin
from django.conf.urls import patterns, include

try:
    from django.apps import AppConfig
    import django

    django.setup()
except ImportError:
    pass

admin.autodiscover()

urlpatterns = patterns('',
                       (r'', include(admin.site.urls)),
                       )
