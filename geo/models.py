# -*- coding: utf-8 -*-
'''
Created on May 7, 2010

@author: sax
'''
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _
import logging
from mptt.models import MPTTModel, TreeForeignKey

logger = logging.getLogger("geo")


class Currency(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=5)

    class Meta:
        app_label = 'geo'
        get_latest_by = 'since'
        ordering = ['code', ]


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


class Country(models.Model):
    """ Model for the country of origin """
    ISO_code = models.CharField(max_length=2, unique=True, blank=False, null=False, db_index=True)
    ISO3_code = models.CharField(max_length=3, blank=True, null=True)
    num_code = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=100, db_index=True)
    fullname = models.CharField(max_length=100, db_index=True)

    region = models.IntegerField(choices=Regions, blank=True, null=True)
    continent = models.CharField(choices=CONTINENTS, max_length=2)
    currency = models.ForeignKey(Currency, blank=True, null=True)

    fullname.alphabetic_filter = True
    objects = CountryManager()

    class Meta:
        app_label = 'geo'
        verbose_name_plural = _('Countries')
        ordering = ['name']

    def __unicode__(self):
        return self.fullname

    def natural_key(self):
        return (self.ISO_code,)


class AdministrativeAreaType(MPTTModel):
    name = models.CharField(_('Name'), max_length=100, db_index=True)
    country = models.ForeignKey(Country)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

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

    def save(self, force_insert=False, force_update=False, using=None):
        super(AdministrativeAreaType, self).save(force_insert, force_update, using)

    def clean(self):
        if self.parent == self:
            raise ValidationError(_('`%s` cannot contains same type') % self.parent)
        super(AdministrativeAreaType, self).clean()


class AdministrativeArea(MPTTModel):
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    country = models.ForeignKey(Country)
    type = models.ForeignKey(AdministrativeAreaType)

    class Meta:
        verbose_name = _("Administrative Area")
        verbose_name_plural = _("Administrative Areas")
        app_label = 'geo'
        ordering = ['name']
        order_with_respect_to = 'country'

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.country.natural_key() + (self.name, )


class Location(models.Model):
    """ Geographical location ( city, place everything with a name and Lat/Lng"""
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

    #
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

    class Meta:
        verbose_name_plural = _('Locations')
        verbose_name = _('Location')
        app_label = 'geo'
        ordering = ("name",)
        order_with_respect_to = 'country'

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.country.natural_key() + (self.name, str(self.lat), str(self.lng))
