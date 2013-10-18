from functools import partial
import random
import string
from itertools import cycle
from django_dynamic_fixture import G
import uuidfield
from sample_data_utils.sample import text
from sample_data_utils.utils import sequence
#from django_any import any_field, any_model
#from django_any.contrib import any_model_with_defaults
from geo.models import Currency, Country, AdministrativeAreaType, AdministrativeArea, LocationType, Location


nextname = partial(sequence, cache={})

# Create two-character iso-codes
iso2_codes = []
for c1 in string.ascii_uppercase:
    for c2 in string.ascii_uppercase:
        iso2_codes.append('{}{}'.format(c1, c2))
random.shuffle(iso2_codes)
iso2_codes_iter = cycle(iso2_codes)

# Create three-character iso-codes
iso3_codes = []
for c1 in string.ascii_uppercase:
    for c2 in string.ascii_uppercase:
        for c3 in string.ascii_uppercase:
            iso3_codes.append('{}{}{}'.format(c1, c2, c3))
random.shuffle(iso3_codes)
iso3_codes_iter = cycle(iso3_codes)

# Create iso-number with three digits
iso_numbers = range(100, 999)
random.shuffle(iso_numbers)
iso_numbers_iter = cycle(iso_numbers)

#
#@any_field.register(uuidfield.UUIDField)
#def uuid_field(field, **kwargs):
#    return uuidfield.UUIDField()._create_uuid()


def subargs(kwargs, prefix):
    prefix = "%s__" % prefix
    ret = {key[len(prefix):]: kwargs.pop(key) for key in kwargs.keys() if key.startswith(prefix)}
    return ret


def currency_factory(**kwargs):
    return G(Currency, code=nextname('CUR').next())


def country_factory(**kwargs):
    iso_code = iso2_codes_iter.next()
    currency = G(Currency, code=nextname(iso_code))

    kwargs.setdefault('iso_code', iso_code)
    kwargs.setdefault('num_code', iso_numbers_iter.next())
    kwargs.setdefault('iso3_code', iso3_codes_iter.next())
    kwargs.setdefault('name', nextname('Country'))
    kwargs.setdefault('fullname', text(20))
    kwargs.setdefault('currency', currency)

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
