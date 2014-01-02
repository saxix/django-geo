from functools import partial
import random
import string
from itertools import cycle
from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest
from geo.hierarchy import italy
from geo.models import Currency, Country, AdministrativeAreaType, AdministrativeArea, LocationType, Location
from sample_data_utils.geo import iso2, iso3, isonum, get_codes
from sample_data_utils.text import text
from sample_data_utils.utils import unique, sequence

nextname = partial(sequence, cache={})
countries = iter(get_codes())

# iso2_codes = unique(country)
# iso_number = unique(isonum)


@pytest.fixture
def hierachy():
    G(Country, iso_code='IT', iso_code3='ITA', iso_num=380,
              name='Italy', fullname='Italy, Italian Republic')

    return italy()

@pytest.fixture
def superuser():
    try:
        return User.objects.get(is_superuser=True)
    except User.DoesNotExist:
         return User.objects.create_superuser('superuser','','123')

def subargs(kwargs, prefix):
    prefix = "%s__" % prefix
    ret = {key[len(prefix):]: kwargs.pop(key) for key in kwargs.keys() if key.startswith(prefix)}
    return ret


def currency_factory(**kwargs):
    return G(Currency, code=nextname('CUR').next())


def country_factory(**kwargs):
    names = nextname('Country')
    iso_2 = unique(iso2, 1, cache={})
    iso_3 = unique(iso3, 1, cache={})
    iso_n = unique(isonum, 1, cache={})

    kwargs.setdefault('iso_code', lambda x: iso_2())
    kwargs.setdefault('iso_code3', lambda x: iso_3())
    kwargs.setdefault('num_code', lambda x: '%03d' % iso_n())
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
