# -*- coding: utf-8 -*-
from django.contrib.admin.util import unquote
from geo.models import Country, Location, AdministrativeArea, AdministrativeAreaType
from geo.templatetags.geo import flag

try:
    from iadmin.options import IModelAdmin as ModelAdmin
    from iadmin.utils import tabular_factory
    from iadmin.api import site
except ImportError:
    from django.contrib.admin import ModelAdmin, site

    def tabular_factory(model, fields=None, inline=None, form=None, **kwargs):
        """ factory for TabularInline

        >>> class MD(IModelAdmin):
        ...     inlines = [tabular_factory(Permission)]
        """
        from django.contrib.admin import TabularInline

        Inline = inline or TabularInline
        name = "%sInLine" % model.__class__.__name__
        attrs = {'model': model, 'fields': fields}
        if form:
            attrs['form'] = form
        attrs.update(kwargs)
        Tab = type(name, (Inline,), attrs)
        return Tab


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
        context = {'nodes': obj.areas.all()}
        context.update(extra_context or {})
        return super(ICountry, self).change_view(request, object_id, form_url, context)


class ILocation(ModelAdmin):
    change_form_template = 'admin/geo/location/change_form.html'
    search_fields = ('name', )
    list_display = ('name', 'country', 'area', 'is_administrative')
    list_display_rel_links = cell_filter = ('country', 'area', 'is_administrative')


class IArea(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'parent', 'country', 'type', 'code')
    list_display_rel_links = cell_filter = ('country', 'type', 'code')
    list_filter = ('type', )
    inlines = (tabular_factory(Location),
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        context = {'nodes': obj.areas.all()}
        context.update(extra_context or {})
        return super(IArea, self).change_view(request, object_id, form_url, context)


class IAreaType(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'parent', 'country')
    list_display_rel_links = cell_filter = ('country', )
    list_filter = ('country', )
    inlines = (tabular_factory(AdministrativeArea),
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        context = {'nodes': obj.children.all()}
        context.update(extra_context or {})
        return super(IAreaType, self).change_view(request, object_id, form_url, context)


reg = ((Country, ICountry), (Location, ILocation), (AdministrativeArea, IArea),
       (AdministrativeAreaType, IAreaType))

for model, model_admin in reg:
    site.register(model, model_admin)
