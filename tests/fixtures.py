from functools import partial
import random
import string
from itertools import cycle
from django_dynamic_fixture import G
from geo.models import Currency, Country, AdministrativeAreaType, AdministrativeArea, LocationType, Location
from sample_data_utils.geo import iso2, isonum, countries
from sample_data_utils.text import text
from sample_data_utils.utils import unique, sequence

nextname = partial(sequence, cache={})

# iso2_codes = unique(country)
# iso_number = unique(isonum)

def subargs(kwargs, prefix):
    prefix = "%s__" % prefix
    ret = {key[len(prefix):]: kwargs.pop(key) for key in kwargs.keys() if key.startswith(prefix)}
    return ret


def currency_factory(**kwargs):
    return G(Currency, code=nextname('CUR').next())


def country_factory(**kwargs):
    names = nextname('Country')
    kwargs.setdefault('iso_code', lambda x: unique(iso2))
    kwargs.setdefault('num_code', lambda x: unique(isonum))
    kwargs.setdefault('iso3_code', lambda x: unique(isonum))
    kwargs.setdefault('name', lambda x: next(names))
    kwargs.setdefault('fullname', lambda x: text(20))

    country = G(Country, **kwargs)
    return country


def area_tree_factory(country):
    parent = area_factory(country, name=nextname('RegionArea'), type__name=nextname('Region'))
    area = area_factory(parent=parent, name=nextname('SubRegionArea'), type__name=nextname('SubRegion'))
    location = location_factory(area=area)
    return parent, area, location


def area_type_factory(country, **kwargs):
    kwargs.setdefault('name', nextname('AdministrativeAreaType'))
    kwargs.setdefault('parent', None)
    return AdministrativeAreaType.objects.get_or_create(country=country, **kwargs)[0]


def area_factory(country=None, **kwargs):
    if 'parent' in kwargs:
        country = kwargs['parent'].country
        type_kwargs = subargs(kwargs, 'type')
        type_kwargs['country'] = country
        type_kwargs['parent'] = kwargs['parent'].type
        kwargs['type'] = area_type_factory(**type_kwargs)
    else:
        type_kwargs = subargs(kwargs, 'type')
        type_kwargs['country'] = country
        kwargs['type'] = area_type_factory(**type_kwargs)

    kwargs.setdefault('parent', None)
    kwargs.setdefault('name', nextname('AdministrativeArea'))

    return AdministrativeArea.objects.get_or_create(country=country, **kwargs)[0]


def location_type_factory(**kwargs):
    return G(LocationType, **kwargs)


def location_factory(**kwargs):
    if 'area' in kwargs:
        kwargs['country'] = kwargs['area'].country
    else:
        if not 'country' in kwargs:
            kwargs['country'] = country_factory(**subargs(kwargs, 'country'))
        area_kwargs = subargs(kwargs, 'area')
        area_kwargs['country'] = kwargs['country']
        kwargs['area'] = area_factory(**area_kwargs)
    if 'type' not in kwargs:
        kwargs['type'] = location_type_factory(**subargs(kwargs, 'type'))

    kwargs.setdefault('name', nextname('Location'))
    location = G(Location, **kwargs)
    return location
