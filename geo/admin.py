# -*- coding: utf-8 -*-
from django.contrib.admin.util import unquote
from django.core.exceptions import ValidationError
from mptt.exceptions import InvalidMove
from geo.models import Country, Location, AdministrativeArea, AdministrativeAreaType
from geo.templatetags.geo import flag

try:
    from iadmin.options import IModelAdmin as ModelAdmin
    from iadmin.utils import tabular_factory
except ImportError:
    from django.contrib.admin import ModelAdmin

    tabular_factory = lambda o: None


class ICountry(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'continent', 'region', 'iso_code', 'iso3_code', 'flag')
    list_filter = ('continent', 'region',)
    cell_filter = ('continent', 'region', )
    fieldsets = [(None, {'fields': (('name', 'fullname'),
                                    ('iso_code', 'iso3_code', 'num_code'),
                                    ('region', 'continent', 'currency'),
        ),

                         })]
    inlines = (tabular_factory(Location),
               tabular_factory(AdministrativeArea),
               tabular_factory(AdministrativeAreaType), )

    def flag(self, o):
        return flag(o)

    flag.allow_tags = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        extra_context = {'nodes': obj.areas.all()}
        return super(ICountry, self).change_view(request, object_id, form_url, extra_context)


class ILocation(ModelAdmin):
    change_form_template = 'admin/geo/location/change_form.html'
    search_fields = ('name', )
    list_display = ('name', 'country',)
    list_display_rel_links = cell_filter = ('country', )


class IArea(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'parent', 'country', 'type')
    list_display_rel_links = cell_filter = ('country', )
    list_filter = ('type', )
    inlines = (tabular_factory(Location),
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        extra_context = {'nodes': obj.areas.all()}
        return super(IArea, self).change_view(request, object_id, form_url, extra_context)


class IAreaType(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'parent', 'country')
    list_display_rel_links = cell_filter = ('country', )
    list_filter = ('country', )
    inlines = (tabular_factory(AdministrativeArea),
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        extra_context = {'nodes': obj.children.all()}
        return super(IAreaType, self).change_view(request, object_id, form_url, extra_context)

__iadmin__ = ((Country, ICountry), (Location, ILocation), (AdministrativeArea, IArea),
              (AdministrativeAreaType, IAreaType))
