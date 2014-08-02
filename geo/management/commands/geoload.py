# -*- coding: utf-8 -*-
from StringIO import StringIO
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.db import transaction, IntegrityError
from geo.loaders import load_timezone
from geo.models import Country, Currency, UNRegion
from geo.utils import load_currency, load_country


Regions = (('OMD', 'West Africa'),
           ('OMJ', 'Southern Africa'),
           ('OMP', 'Latin America & Caribbean'),
           ('OMB', 'Asia'),
           ('OMC', 'Middle East, North Africa, Eastern Europe and Central Asia'), ('OMN', 'Eastern & Central Africa'))


class Command(BaseCommand):
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='all'),
        make_option('-c', '--country', action='store_true', dest='country'),
        make_option('-p', '--capitals', action='store_true', dest='capital'),
        make_option('-z', '--timezone', action='store_true', dest='tz'),
        make_option('-m', '--currency', action='store_true', dest='currency'),
        make_option('-r', '--region', action='store_true', dest='region'),
        # make_option('-i', '--ignore-cache', action='store_true', dest='reset'),
    )

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        load_all = options.get('all')
        # reset = options.get('currency')
        if verbosity==0:
            stdout = StringIO()
        else:
            stdout  = self.stdout.write


        if load_all:
            region = tz = country = capital = currency = region = True
        else:
            country = options.get('country')
            region = options.get('region')
            capital = options.get('capital')
            tz = options.get('tz')
            currency = options.get('currency')

        if currency:
            stdout.write("Loading currencies...")
            load_currency(stdout)
        if region:
            for code, name in Regions:
                UNRegion.objects.get_or_create(name=name, code=code)
        if country:
            stdout.write("Loading countries...")
            load_country(stdout)
        if tz:
            stdout.write("Loading timezones...")
            load_timezone(stdout)
