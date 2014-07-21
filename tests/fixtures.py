from functools import partial
import random
import string
from itertools import cycle
from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest
from geo.hierarchy import italy
from geo.models import Currency, Country, AdministrativeAreaType, AdministrativeArea, LocationType, Location
from .util import text, unique
import itertools


name = lambda prefix, sequence: "{0}-{1}".format(prefix, next(sequence))
nextname = partial(name, sequence=itertools.count())

counter = itertools.count()


@pytest.fixture
def hierachy():
    Country.objects.all().delete()
    Currency.objects.all().delete()
    Country.objects.get_or_create(iso_code='IT', iso_code3='ITA', iso_num=380,
                                  name='Italy', fullname='Italy, Italian Republic')

    return italy()


@pytest.fixture
def superuser():
    try:
        return User.objects.get(is_superuser=True)
    except User.DoesNotExist:
        return User.objects.create_superuser('superuser', '', '123')


def subargs(kwargs, prefix):
    prefix = "%s__" % prefix
    ret = {key[len(prefix):]: kwargs.pop(key) for key in kwargs.keys() if key.startswith(prefix)}
    return ret


def currency_factory(**kwargs):
    return G(Currency,
             numeric_code=next(counter),
             code=nextname('CUR').next())


def country_factory(**kwargs):
    country_name = partial(name, sequence=itertools.count(start=0))

    kwargs.setdefault('iso_code', lambda x: "{:02}".format(next(counter))[:2])
    kwargs.setdefault('iso_code3', lambda x: "{:03}".format(next(counter))[:3])
    kwargs.setdefault('undp', lambda x: "{:03}".format(next(counter))[:3])
    kwargs.setdefault('nato3', lambda x: "{:03}".format(next(counter))[:3])
    kwargs.setdefault('iso_num', lambda x: "{:03}".format(next(counter))[:3])

    kwargs.setdefault('name_en', lambda x: country_name('Country'))
    kwargs.setdefault('currency', None)

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
