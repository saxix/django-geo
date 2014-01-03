# -*- coding: utf-8 -*-
from StringIO import StringIO
from contextlib import contextmanager
import os
import requests
import codecs
import sys
import unicodecsv as csv
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from geo.config import conf
from geo.exceptions import LoadingError
from geo.models import Country, Currency, AdministrativeArea, Location


def splitline(line, sep='\t', ignore='#'):
    if line.startswith(ignore):
        return None
    elif not line.strip():
        return None
    return line.split(sep)


@contextmanager
def open_cached(url, destination=None, rewrite=False):
    filename = destination or url.split('/')[-1]
    fielpath = os.path.join(conf.CACHE, filename)

    if rewrite or not os.path.exists(fielpath):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with codecs.open(fielpath, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)
    f = codecs.open(fielpath, 'r')
    yield f
    f.close()


def load_timezone(overwrite=False, stdout=None):
    from pytz import country_timezones
    # for c in country_timezones()
    stdout = stdout or StringIO()

    def _update(instance, key):
        try:
            instance.timezone = country_timezones[key][0]
            instance.save()
        except KeyError:
            pass

    filters1 = filters2 = filters3 = {}
    if overwrite:
        filters1 = {'timezone__isnull': True}
        filters2 = {'country__timezone__isnull': True}
        filters3 = {'country__timezone__    Pisnull': True}

    for country in Country.objects.filter(**filters1):
        _update(country, country.iso_code)
        stdout.write("Updated timezone for `%s` \n" % unicode(country))

    for aa in AdministrativeArea.objects.filter(**filters2):
        _update(aa, aa.country.iso_code)
        stdout.write("Updated timezone for `%s` \n" % unicode(aa))

    for location in Location.objects.filter(**filters3):
        _update(location, location.country.iso_code)
        stdout.write("Updated timezone for `%s` \n" % unicode(location))


def load_fullnames(stdout=None):
    stdout = stdout or StringIO()
    fielpath = os.path.join(conf.DATA, 'fullnames.csv')
    with codecs.open(fielpath, 'r') as h:
        f = csv.reader(h, encoding='utf-8', delimiter=',', doublequote='"')
        for parts in f:
            code, name, fullname = parts
            try:
                c = Country.objects.get(iso_num=code)
                c.name = name
                c.fullname = fullname
                c.save()
            except Country.DoesNotExist:
                print code, name, fullname


def load_currency_symbols(stdout=None):
    fielpath = os.path.join(conf.DATA, 'symbols.csv')

    with codecs.open(fielpath, 'r') as h:
        f = csv.reader(h, encoding='utf-8', delimiter=';', doublequote='"')
        for parts in f:
            code, symbol = parts
            try:
                c = Currency.objects.get(iso_code=code)
                c.symbol = symbol
                c.save()
            except Currency.DoesNotExist:
                print code


def load_country(rewrite=False, stdout=None):
    url = "http://download.geonames.org/export/dump/countryInfo.txt"
    stdout = stdout or StringIO()
    with open_cached(url) as f:
        r = csv.reader(f, encoding='utf-8', delimiter='\t', lineterminator='\n')
        for line in r:
            if line[0][0] == '#':
                continue
            if len(line) == 19:
                iso2, iso3, ison, fips, name, \
                capital, area, population, \
                continent, tld, \
                currencycode, currencyname, \
                phone, postal_code_format, \
                postal_code_regex, \
                languages, \
                geonameid, neighbours, \
                equivalentfipscode = line

                fields = {'iso_code3': iso3, 'iso_code': iso2,
                          'phone_prefix': phone, 'name': name,
                          'fullname': name, 'tld': tld,
                          'continent': continent.upper()}
                c, created = Country.objects.get_or_create(iso_num=ison,
                                                      defaults=fields)

                for field_name, value in fields.items():
                    setattr(c, field_name, value)

                try:
                    curr = Currency.objects.get(iso_code=currencycode)
                    c.currency = curr
                except Currency.DoesNotExist:
                    pass
                c.clean()
                c.save()
                stdout.write("%s\n" % unicode(c))
            else:
                raise LoadingError(line)

    load_fullnames()


def load_currency(rewrite=False, stdout=None):
    """
        ISO 4217 Currency Codes - Dataset - Frictionless Open Data
    """
    url = "http://www.currency-iso.org/dam/downloads/table_a1.xml"
    from lxml import etree

    stdout = stdout or StringIO()
    with open_cached(url) as f:
        root = etree.fromstring(f.read())
        for element in root.iter("CcyNtry"):
            code = element.find('Ccy')
            if code is not None:
                values = {'numeric_code': element.find('CcyNbr').text,
                          'name': element.find('CcyNm').text,
                          'symbol': ''}

                cur, created = Currency.objects.get_or_create(iso_code=code.text,
                                                              defaults=values)
                if not created:
                    for field_name, value in values.items():
                        setattr(cur, field_name, value)

                try:
                    cur.decimals = int(element.find('CcyMnrUnts').text)
                except ValueError:
                    pass
                cur.save()
                stdout.write('%s\n' % unicode(cur))

    load_currency_symbols()

