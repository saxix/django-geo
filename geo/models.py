# -*- coding: utf-8 -*-
'''
Created on May 7, 2010

@author: sax
'''
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _
import logging
from mptt.exceptions import InvalidMove
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

logger = logging.getLogger("geo")


class Currency(models.Model):
    code = models.CharField(max_length=5, unique=True, help_text="ISO 4217 code")
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        app_label = 'geo'
        ordering = ['code', ]

    def __unicode__(self):
        return u"%s (%s)" % (self.code, self.name)


CONTINENTS = (
    ('AF', _('Africa')),
    ('AS', _('Asia')),
    ('EU', _('Europe')),
    ('NA', _('North America')),
    ('SA', _('South America')),
    ('OC', _('Oceania')),
    ('AN', _('Antartica'))
    )

Regions = zip(range(1, 5), ('Africa', 'Americas', 'Asia', 'Middle East'))

class CountryManager(Manager):
    use_for_related_fields = True

    def _by_continent(self, c):
        return self.get_query_set().filter(continent=c)

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

    def get_by_natural_key(self, iso_code):
        return self.get(iso_code=iso_code)


class Country(models.Model):
    """ Model for the country of origin """
    iso_code = models.CharField(max_length=2, unique=True, blank=False, null=False, db_index=True,
        help_text='ISO 3166-1 alpha 2')
    iso3_code = models.CharField(max_length=3, blank=True, null=True, db_index=True, help_text='ISO 3166-1 alpha 3')
    num_code = models.CharField(max_length=3, blank=True, null=True, help_text='ISO 3166-1 numeric')
    name = models.CharField(max_length=100, db_index=True)
    fullname = models.CharField(max_length=100, db_index=True)

    region = models.IntegerField(choices=Regions, blank=True, null=True)
    continent = models.CharField(choices=CONTINENTS, max_length=2)
    currency = models.ForeignKey(Currency, blank=True, null=True)

    #    tld = models.CharField(max_length=6, blank=True, null=True, help_text='internet tld')
    #    tz = models.IntegerField(blank=True, null=True, help_text='time zone')

    fullname.alphabetic_filter = True
    objects = CountryManager()

    class Meta:
        app_label = 'geo'
        verbose_name_plural = _('Countries')
        ordering = ['name']

    def __unicode__(self):
        return self.fullname

    def natural_key(self):
        return (self.iso_code,)

    def __contains__(self, item):
        if hasattr(item, 'country'):
            return item.country == self

    def cities(self):
        return self.location_set.cities()


class AdministrativeAreaTypeManager(TreeManager):
    use_for_related_fields = True

    def get_by_natural_key(self, iso_code, name):
        return self.get(country__iso_code=iso_code, name=name)


class AdministrativeAreaType(MPTTModel):
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

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.country.natural_key() + (self.name, )

    natural_key.dependencies = ['geo.country']

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('`%s` cannot contains same type') % self.parent)
        super(AdministrativeAreaType, self).clean()

    def get_or_create(self, **kwargs):
        return AdministrativeArea.objects.get_or_create(country=self.country, type=self, **kwargs)


class AdministrativeAreaManager(TreeManager):
    use_for_related_fields = True

    def get_by_natural_key(self, iso_code, name):
        return self.get(country__iso_code=iso_code, name=name)

    def get_or_create(self, **kwargs):
        return super(AdministrativeAreaManager, self).get_or_create(**kwargs)


class AdministrativeArea(MPTTModel):
    """ Administrative areas that can contains other AdministrativeArea and/or Location

    """

    name = models.CharField(_('Name'), max_length=255, db_index=True)
    code = models.CharField(_('Code'), max_length=10, blank=True, null=True, db_index=True, help_text='ISO 3166-2 code')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='areas')
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
        return self.name

    def natural_key(self):
        return (self.country.iso_code, self.name )

    natural_key.dependencies = ['geo.country']

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('`%s` cannot contains self') % self)
        if self.parent and self.parent.type == self.type:
            raise ValidationError(_('`%s` cannot contains same type') % self.parent.type)
        if (self.pk and self.parent) and self in self.parent:
            raise ValidationError(_('`%s` cannot contains same type') % self.parent)

        super(AdministrativeArea, self).clean()

    def save(self, *args, **kwargs):
        if not self.country_id:
            self.country = self.parent.country
        self.clean()
        super(AdministrativeArea, self).save(*args, **kwargs)

    def __contains__(self, item):
        return True


class LocationManager(models.Manager):
    use_for_related_fields = True

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except ObjectDoesNotExist:
            return None

    def cities(self):
        return self.get_query_set().filter(type=Location.CITY)

    def get_by_natural_key(self, country_iso_code, name, lat, lng):
        if lat == 'None':
            lat = None
        if lng == 'None':
            lng = None

        return self.get(country__iso_code=country_iso_code, name=name, lat=lat, lng=lng)


class Location(models.Model):
    """ Administrative location ( city, place everything with a name and Lat/Lng that
    is not intetend to contains anything ( use Areas for that
    """
    NONE = 0
    COUNTRY = 10
    EXACT = 20

    ACCURACY = (
        (NONE, _('None')),
        (COUNTRY, _('Country')),
        (EXACT, _('Exact')),
        )

    CITY = 0
    OTHER = 1
    TYPE = ((CITY, _("City")),
            (OTHER, _("Other")),
        )

    country = models.ForeignKey(Country, db_index=True)
    area = models.ForeignKey(AdministrativeArea, db_index=True, blank=True, null=True)
    type = models.IntegerField(choices=TYPE, default=CITY)
    is_capital = models.BooleanField(default=False,
        help_text="True if is the capital of `country`")

    is_administrative = models.BooleanField(default=False,
        help_text="True if is administrative for `area`")

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
        ordering = ('name', 'country')
        order_with_respect_to = 'country'

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.country.natural_key() + (self.name, str(self.lat), str(self.lng))

    natural_key.dependencies = ['geo.country']

    def clean(self):
        if self.area and self.area.country != self.country:
            raise ValidationError('Selected area not in selected country')
        super(Location, self).clean()

