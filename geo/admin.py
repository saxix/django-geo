# -*- coding: utf-8 -*-
from django.contrib.admin.options import TabularInline
from django.contrib.admin.util import unquote
from django.core.urlresolvers import reverse
from geo.forms import CountryForm, AreaForm, administrativeareatypeform_factory_for_country, LocationForm
from geo.models import Country, Location, AdministrativeArea, AdministrativeAreaType, Currency
from geo.templatetags.geo import flag
from django.contrib.admin import ModelAdmin, site, TabularInline


def tabular_factory(model, fields=None, inline=None, form=None, **kwargs):
    """ factory for TabularInline

    >>> class MD(IModelAdmin):
    ...     inlines = [tabular_factory(Permission)]
    """
    attrs = {'model': model, 'fields': fields}
    read_only = kwargs.pop('read_only', False)
    if read_only:
        attrs['readonly_fields'] = fields
        attrs['can_delete'] = False

    Inline = inline or TabularInline
    name = "%sInLine" % model.__class__.__name__
    if form:
        attrs['form'] = form
    attrs.update(kwargs)
    Tab = type(name, (Inline,), attrs)
    return Tab


class ICurrency(ModelAdmin):
    search_fields = ('name', 'iso_code')
    list_display = ('name', 'iso_code', 'symbol', 'used_by')
    inlines = [tabular_factory(Country, fields=['name'], read_only=True)]

    def used_by(self, o):
        return ', '.join(['<a href="%s">%s</>' % (reverse('admin:geo_country_change', args=[c.pk]), c.name) for c in
                          Country.objects.filter(currency=o)])

    used_by.allow_tags = True


class AdministrativeAreaInline(TabularInline):
    model = AdministrativeArea

    def get_formset(self, request, obj=None, **kwargs):
        self.form = administrativeareatypeform_factory_for_country(obj)
        return super(AdministrativeAreaInline, self).get_formset(request, obj, **kwargs)


class ICountry(ModelAdmin):
    form = CountryForm
    search_fields = ('name', )
    list_display = ('name', 'continent', 'iso_code', 'iso_code3',
                    'currency', 'timezone', 'flag')
    list_filter = ('continent', 'region', )
    cell_filter = ('continent', 'region', 'currency')
    fieldsets = [(None, {'fields': (('name', 'fullname'),
                                    ('iso_code', 'iso_code3', 'iso_num'),
                                    ('region', 'continent', 'currency'),
                                    ('timezone', 'tld', 'phone_prefix'))})]
    inlines = (tabular_factory(Location, exclude=('description',)),
               AdministrativeAreaInline,
               tabular_factory(AdministrativeAreaType), )

    def flag(self, o):
        return flag(o)

    flag.allow_tags = True

    def capital(self, o):
        c = o.location_set.get_or_none(is_capital=True)
        if c:
            admin_url = reverse('admin:geo_location_change', args=[c.pk])
            return "<a href='%s'>%s</a>" % (admin_url, c.name)
        return c

    capital.allow_tags = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        context = {'nodes': obj.areas.all()}
        context.update(extra_context or {})
        return super(ICountry, self).change_view(request, object_id, form_url, context)


class ILocation(ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'country', 'area', 'is_administrative', 'is_capital')
    list_display_rel_links = cell_filter = ('country', 'area', 'is_administrative', 'is_capital')
    list_filter = ('is_administrative', 'is_capital')
    form = LocationForm


def rebuild_tree(modeladmin, request, queryset):
    modeladmin.model.objects.rebuild()


rebuild_tree.short_description = "Rebuild MPTT table structure"


class IArea(ModelAdmin):
    form = AreaForm
    search_fields = ('name', )
    list_display = ('name', 'parent', 'country', 'type', 'code')
    list_display_rel_links = cell_filter = ('country', 'type', 'code')
    list_filter = ('type', 'country')
    inlines = (tabular_factory(Location),)
    actions = [rebuild_tree, ]

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
    inlines = (tabular_factory(AdministrativeArea),)
    actions = [rebuild_tree, ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        context = {'nodes': obj.children.all()}
        context.update(extra_context or {})
        return super(IAreaType, self).change_view(request, object_id, form_url, context)

    def rebuild_tree(self, request, queryset):
        self.model.objects.rebuild()

    rebuild_tree.short_description = "Rebuild MPTT table structure"


reg = ((Country, ICountry), (Location, ILocation), (AdministrativeArea, IArea),
       (AdministrativeAreaType, IAreaType), (Currency, ICurrency), )

for model, model_admin in reg:
    site.register(model, model_admin)
