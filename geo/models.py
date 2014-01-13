# -*- coding: utf-8 -*-
'''
Created on May 7, 2010

@author: sax
'''
import functools
import warnings
from timezone_field import TimeZoneField
from uuidfield import UUIDField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import ugettext_lazy as _
import logging
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

logger = logging.getLogger("geo")


class CurrencyManager(Manager):
    use_for_related_fields = True

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class Currency(models.Model):
    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'), default="")
    iso_code = models.CharField(max_length=5, db_index=True, unique=True, help_text="ISO 4217 code")
    numeric_code = models.CharField(max_length=5, unique=True, help_text="ISO 4217 code")
    decimals = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5, blank=True, null=True)
    objects = CurrencyManager()

    class Meta:
        app_label = 'geo'
        ordering = ['iso_code', ]
        verbose_name_plural = 'Currencies'

    def __unicode__(self):
        return unicode("%s (%s)" % (self.iso_code, self.name))

    def natural_key(self):
        return self.uuid.hex,


CONTINENTS = (
    ('AF', _('Africa')),
    ('AN', _('Antartica')),
    ('AS', _('Asia')),
    ('EU', _('Europe')),
    ('NA', _('North America')),
    ('OC', _('Oceania')),
    ('SA', _('South America')),
)

REGIONS = zip(range(1, 5), ('Africa', 'Americas', 'Asia', 'Middle East'))


class CountryManager(Manager):
    use_for_related_fields = True

    def _by_continent(self, continent):
        return self.get_query_set().filter(continent=continent)

    def asia(self):
        return self._by_continent('AS')

    def europa(self):
        return self._by_continent('EU')

    def north_america(self):
        return self._by_continent('NA')

    def south_america(self):
        return self._by_continent('SA')

    def oceania(self):
        return self._by_continent('OC')

    def antartica(self):
        return self._by_continent('AN')

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class deprecated_fieldname(object):
    def __init__(self, replace):
        self.new_field_name = replace
        self._message = "`{0.name}` is deprecated. Please use `{0.new_field_name}` instead"

    def __get__(self, instance, owner):
        warnings.warn(self._message.format(self), stacklevel=2)
        return getattr(instance, self.new_field_name)

    def __set__(self, instance, value):
        warnings.warn(self._message.format(self), stacklevel=2)
        setattr(instance, self.new_field_name, value)

    def contribute_to_class(self, cls, name, virtual_only=False):
        self.name = name
        setattr(cls, name, self)


class Country(models.Model):
    """ Model for the country of origin.
    """
    iso_code = models.CharField(max_length=2, unique=True, blank=False, null=False, db_index=True,
                                help_text='ISO 3166-1 alpha 2', validators=[MinLengthValidator(2)])
    iso_code3 = models.CharField(max_length=3, unique=True, blank=False, null=False, db_index=True,
                                 help_text='ISO 3166-1 alpha 3', validators=[MinLengthValidator(3)])
    iso_numeric = models.CharField(max_length=3, unique=True, blank=False, null=False,
                                   help_text='ISO 3166-1 numeric', validators=[RegexValidator('\d\d\d')])
    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'), default="")

    name = models.CharField(max_length=100, db_index=True)

    fullname = models.CharField(max_length=100, db_index=True)

    region = models.IntegerField(choices=REGIONS, blank=True, null=True, default=None)
    continent = models.CharField(choices=CONTINENTS, max_length=2)
    currency = models.ForeignKey(Currency, blank=True, null=True)

    tld = models.CharField(help_text='Internet tld', max_length=5, blank=True, null=True)
    phone_prefix = models.CharField(help_text='Phone prefix number', max_length=20, blank=True, null=True)

    timezone = TimeZoneField(blank=True, null=True, default=None)
    expired = models.DateField(blank=True, null=True, default=None)
    fullname.alphabetic_filter = True
    objects = CountryManager()

    num_code = deprecated_fieldname('iso_numeric')
    iso3_code = deprecated_fieldname('iso_code3')


    class Meta:
        app_label = 'geo'
        verbose_name_plural = _('Countries')
        ordering = ['name']

    def __unicode__(self):
        return u"%s (%s)" % (self.fullname, self.iso_code)

    def clean(self):
        super(Country, self).clean()
        self.iso_code = self.iso_code.upper()
        self.iso_code3 = self.iso_code3.upper()

    def natural_key(self):
        return (self.uuid.hex, )

    def __contains__(self, item):
        if hasattr(item, 'country'):
            return item.country.iso_code == self.iso_code

    def sub(self, type):
        return self.areas.filter(type__name=type)


class AdministrativeAreaTypeManager(TreeManager):
    use_for_related_fields = True

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class AdministrativeAreaType(MPTTModel):
    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'), default="")
    name = models.CharField(_('Name'), max_length=100, db_index=True)
    country = models.ForeignKey(Country)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    objects = AdministrativeAreaTypeManager()

    class Meta:
        verbose_name = _("Administrative Area Type")
        verbose_name_plural = _("Administrative Area Types")
        app_label = 'geo'
        ordering = ['name']
        order_with_respect_to = 'country'
        unique_together = (('country', 'name'),)

    def __unicode__(self):
        return unicode(self.name)

    def __contains__(self, item):
        if isinstance(item, AdministrativeAreaType) and item.is_child_node():
            return item.is_descendant_of(self)

    def natural_key(self):
        return (self.uuid.hex, )

    natural_key.dependencies = ['geo.country']

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('`%s` cannot contains same type') % self.parent)
        super(AdministrativeAreaType, self).clean()

    def get_or_create(self, **kwargs):
        return AdministrativeArea.objects.get_or_create(country=self.country, type=self, **kwargs)


class AdministrativeAreaManager(TreeManager):
    use_for_related_fields = True

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class AdministrativeArea(MPTTModel):
    """ Administrative areas that can contains other AdministrativeArea and/or Location.
    """

    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'), default="")
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    code = models.CharField(_('Code'), max_length=10, blank=True, null=True, db_index=True, help_text='ISO 3166-2 code')
    parent = TreeForeignKey('self', null=True, blank=True, default=None, related_name='areas')
    country = models.ForeignKey(Country, related_name='areas')
    type = models.ForeignKey(AdministrativeAreaType)
    objects = AdministrativeAreaManager()

    class Meta:
        verbose_name = _("Administrative Area")
        verbose_name_plural = _("Administrative Areas")
        unique_together = (('name', 'country', 'type'),)
        app_label = 'geo'
        ordering = ['name']
        order_with_respect_to = 'country'

    def __unicode__(self):
        return unicode(self.name)

    def __repr__(self):
        return "<%s: %s>" % (self.type.name, self.name)

    def natural_key(self):
        return (self.uuid.hex, )

    natural_key.dependencies = ['geo.administrativeareatype', 'geo.country']

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('`%s` cannot contains self') % self)
        if self.parent and self.parent.type == self.type:
            raise ValidationError(_('`%s` cannot contains same type') % self.parent.type)
        if (self.pk and self.parent) and self.parent in self:
            raise ValidationError(_('`%s` cannot contains `%s`') % (self, self.parent))
        super(AdministrativeArea, self).clean()

    def save(self, *args, **kwargs):
        if not self.country_id:
            self.country = self.parent.country
        self.clean()
        super(AdministrativeArea, self).save(*args, **kwargs)

    def __contains__(self, item):
        if isinstance(item, AdministrativeArea) and item.is_child_node():
            return item.is_descendant_of(self)
        elif isinstance(item, Location) and item.area:
            return item.area.is_descendant_of(self)


class LocationTypeManager(models.Manager):
    use_for_related_fields = True

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class LocationType(models.Model):
    """Type of the location (city, village, place, locality, neighbourhood, etc.)
    This is not intended to contain anything inside it.
    """
    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'), default="")
    description = models.CharField(unique=True, max_length=100)
    objects = LocationTypeManager()

    class Meta:
        verbose_name_plural = _('Location Types')
        verbose_name = _('Location Type')
        app_label = 'geo'

    def natural_key(self):
        return (self.uuid.hex, )


class LocationManager(models.Manager):
    use_for_related_fields = True

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class Location(models.Model):
    """Administrative location (city, place everything with a name and Lat/Lng that
    is not intended to contain anything; use Areas for that).
    """
    NONE = 0
    COUNTRY = 10
    EXACT = 20

    ACCURACY = (
        (NONE, _('None')),
        (COUNTRY, _('Country')),
        (EXACT, _('Exact')))

    country = models.ForeignKey(Country, db_index=True)
    area = models.ForeignKey(AdministrativeArea, db_index=True, blank=True, null=True)
    type = models.ForeignKey(LocationType, blank=True, null=True)

    is_capital = models.BooleanField(default=False, help_text="True if is the capital of `country`")
    is_administrative = models.BooleanField(default=False, help_text="True if is administrative for `area`")
    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'), default="")
    name = models.CharField(_('Name'), max_length=255, db_index=True)

    description = models.CharField(max_length=100, blank=True, null=True)
    lat = models.DecimalField(max_digits=18, decimal_places=12, blank=True, null=True)
    lng = models.DecimalField(max_digits=18, decimal_places=12, blank=True, null=True)
    acc = models.IntegerField(choices=ACCURACY, default=NONE, blank=True, null=True,
                              help_text="Define the level of accuracy of lat/lng infos")
    objects = LocationManager()

    class Meta:
        verbose_name_plural = _('Locations')
        verbose_name = _('Location')
        app_label = 'geo'
        ordering = ('name', 'country', )
        order_with_respect_to = 'country'
        unique_together = (('area', 'name'), )

    def __unicode__(self):
        return unicode(self.name)

    def natural_key(self):
        return (self.uuid.hex, )

    natural_key.dependencies = ['geo.administrativearea', 'geo.country', 'geo.locationtype']

    def clean(self):
        if self.area and self.area.country != self.country:
            raise ValidationError('Selected area not in selected country')
        super(Location, self).clean()
