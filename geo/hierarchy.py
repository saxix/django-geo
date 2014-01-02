# -*- coding: utf-8 -*-

from django.utils.translation import gettext as _
from geo.models import Country


def italy():
    italy = Country.objects.get(iso_code='IT')
    regione, __ = italy.administrativeareatype_set.get_or_create(name='Regione')
    provincia, __ = italy.administrativeareatype_set.get_or_create(name='Provincia',
                                                                   parent=regione)
    comune, __ = italy.administrativeareatype_set.get_or_create(name='Comune',
                                                                parent=provincia)
    return italy, regione, provincia, comune


def usa():
    usa = Country.objects.get(iso_code='US')
    state, __ = italy.administrativeareatype_set.get_or_create(name='State')
    county, __ = italy.administrativeareatype_set.get_or_create(name='County',
                                                                parent=state)
    township, __ = italy.administrativeareatype_set.get_or_create(name='Township',
                                                                  parent=county)
    return usa, state, county, township

