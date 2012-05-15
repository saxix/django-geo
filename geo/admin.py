# -*- coding: utf-8 -*-
from geo.models import Country, Location, AdministrativeArea, AdministrativeAreaType
try:
    from iadmin.options import IModelAdmin as ModelAdmin
    from iadmin.utils import tabular_factory
except ImportError:
    from django.contrib.admin import ModelAdmin
    tabular_factory = lambda o: None

class ICountry(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'continent', 'region', 'ISO_code', 'ISO3_code',)
    list_filter = ('continent', 'region',)
    cell_filter = ('continent', 'region', )
    inlines = (tabular_factory(Location),
               tabular_factory(AdministrativeArea),
               tabular_factory(AdministrativeAreaType), )

class ILocation(ModelAdmin):
    change_form_template = 'admin/geo/location/change_form.html'
    search_fields = ('name', )
    list_display = ('name', 'country',)
    list_display_rel_links = cell_filter = ('country', )

class IArea(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'parent', 'country','type')
    list_display_rel_links = cell_filter = ('country', )
    list_filter = ('type', )
    inlines = (tabular_factory(Location),
               )

class IAreaType(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'parent', 'country')
    list_display_rel_links = cell_filter = ('country', )
    list_filter = ('country', )
    inlines = (tabular_factory(AdministrativeArea),
        )

__iadmin__ = ((Country, ICountry), (Location, ILocation), (AdministrativeArea, IArea),
              (AdministrativeAreaType, IAreaType))
