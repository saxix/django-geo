# -*- coding: utf-8 -*-
'''
Created on May 7, 2010

@author: sax
'''
from uuidfield import UUIDField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.manager import Manager
from django.utils.translation import ugettext_lazy as _
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
        return unicode("%s (%s)" % (self.code, self.name))


CONTINENTS = (
    ('AF', _('Africa')),
    ('AS', _('Asia')),
    ('EU', _('Europe')),
    ('NA', _('North America')),
    ('SA', _('South America')),
    ('OC', _('Oceania')),
    ('AN', _('Antartica')))

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
    iso_code = models.CharField(max_length=2, unique=True, blank=False, null=False, db_index=True, default=None,
                                help_text='ISO 3166-1 alpha 2', validators=[MinLengthValidator(2)])
    iso3_code = models.CharField(max_length=3, unique=True, blank=False, null=False, db_index=True, default=None,
                                 help_text='ISO 3166-1 alpha 3', validators=[MinLengthValidator(3)])
    num_code = models.CharField(max_length=3, unique=True, blank=False, null=False, default=None,
                                help_text='ISO 3166-1 numeric', validators=[RegexValidator('\d\d\d')])

    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'))
    name = models.CharField(max_length=100, db_index=True, default=None)
    fullname = models.CharField(max_length=100, db_index=True, default=None)

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
        return unicode(self.fullname)

    def clean(self):
        super(Country, self).clean()
        self.iso_code = self.iso_code.upper()
        self.iso3_code = self.iso3_code.upper()

    def natural_key(self):
        return (self.iso_code,)

    def __contains__(self, item):
        if hasattr(item, 'country'):
            return item.country.iso_code == self.iso_code

    def cities(self):
        return self.location_set.cities()


class AdministrativeAreaTypeManager(TreeManager):
    use_for_related_fields = True

    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class AdministrativeAreaType(MPTTModel):
    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'))
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
        return (self.uuid,)

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
    """ Administrative areas that can contains other AdministrativeArea and/or Location

    """

    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'))
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
        return unicode(self.name)

    def natural_key(self):
        return (self.uuid, )

    natural_key.dependencies = ['geo.country']

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
    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'))
    description = models.CharField(unique=True, max_length=100)

    class Meta:
        verbose_name_plural = _('Location Types')
        verbose_name = _('Location Type')
        app_label = 'geo'

    def natural_key(self):
        return (self.uuid,)


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
    is_capital = models.BooleanField(default=False,
        help_text="True if is the capital of `country`")

    is_administrative = models.BooleanField(default=False,
        help_text="True if is administrative for `area`")

    uuid = UUIDField(auto=True, blank=False, version=1, help_text=_('unique id'))
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
        unique_together = (('area', 'name'), )

    def __unicode__(self):
        return unicode(self.name)

    def natural_key(self):
        return (self.uuid,)

    natural_key.dependencies = ['geo.country']

    def clean(self):
        if self.area and self.area.country != self.country:
            raise ValidationError('Selected area not in selected country')
        super(Location, self).clean()
