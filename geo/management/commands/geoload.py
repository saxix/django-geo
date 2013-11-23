# -*- coding: utf-8 -*-
import StringIO
import unicodecsv as csv
from functools import wraps
import os
import zipfile
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.db import transaction, IntegrityError
from geo.models import Country, Currency, CONTINENTS
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), 'DATADIR')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def cache(func):
    def _inner(filename):
        if os.path.exists(os.path.join(DATA_DIR, filename)):
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                content = f.read()
        else:
            content = func(filename)
            with open(os.path.join(DATA_DIR, filename), 'wb') as f:
                f.write(content)
        return content

    return _inner


def geoload(filename):
    url = 'http://download.geonames.org/export/dump/%s' % filename

    if os.path.exists(os.path.join(DATA_DIR, filename)):
        with open(os.path.join(DATA_DIR, filename), 'r') as f:
            content = f.read()
    else:
        r = requests.get(url)
        assert r.status_code == 200, r.status_code
        assert r.headers['content-type'] != 'text/html; charset=utf-8', r.headers['content-type']
        with open(os.path.join(DATA_DIR, filename), 'wb') as f:
            f.write(r.content)
        content = r.content

    name, ext = filename.rsplit('.', 1)
    if ext == 'zip':
        z = zipfile.ZipFile(StringIO.StringIO(content))
        return z.read(name + '.txt')

    return content


class Command(BaseCommand):
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='all'),
        make_option('-c', '--country', action='store_true', dest='country'),
        #make_option('-t', '--city', action='store_true', dest='city'),
        make_option('-z', '--timezone', action='store_true', dest='tz'),
        make_option('-m', '--currency', action='store_true', dest='currency'),
        make_option('-r', '--region', action='store_true', dest='region'),
        make_option('-i', '--ignore-cache', action='store_true', dest='reset'),
    )

    def _split(self, text, sep='\t', linesep='\n', ignore='#'):
        lines = []
        for line in text.split(linesep):
            if line.startswith(ignore):
                continue
            elif not line.strip():
                continue
            lines.append(line.split(sep))
        return lines

    def handle(self, *args, **options):
        load_all = options.get('all')
        reset = options.get('currency')
        if load_all:
            region = country = city = tz = currency = True
        else:
            country = options.get('country')
            region = options.get('region')
            city = options.get('city')
            tz = options.get('timezone')
            currency = options.get('currency')

        if region:
            self.regions()
        if country:
            self.countries()

    #def cities(self):
    #    data = geoload('cities15000.zip')

    def countries(self):
        data = geoload('countryInfo.txt')
        # data = geoload('allCountries.zip')
        # data = load('IT.zip')
        lines = self._split(data)
        with transaction.commit_on_success():
            for line in lines:
                if line:
                    try:
                        iso2, iso3, ison, fips, name, \
                        capital, area, population, \
                        continent, tld, \
                        currencycode, currencyname, \
                        phone, postal_code_format, \
                        postal_code_regex, \
                        languages, \
                        geonameid, neighbours, \
                        equivalentfipscode = line

                        c, __ = Country.objects.get_or_create(num_code=ison,
                                                              defaults={'iso3_code': iso3,
                                                                        'iso_code': iso2,
                                                                        'name': name,
                                                                        'fullname': name})
                        c.tld = tld
                        c.geonameid = geonameid or None
                        c.continent = continent.upper()

                        curr, __ = Currency.objects.get_or_create(code=currencycode,
                                                                    defaults={'name': currencyname})
                        c.currency = curr
                        c.clean()
                        c.save()
                    except Country.DoesNotExist:
                        print geonameid, line
                    except (ValueError, IntegrityError, ValidationError) as e:
                        print e, line
                        raise
                    except:
                        raise
