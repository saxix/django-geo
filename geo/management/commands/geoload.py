# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.db import transaction, IntegrityError
from geo.loaders import load_timezone
from geo.models import Country, Currency
from geo.utils import load_currency, load_country


class Command(BaseCommand):
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='all'),
        make_option('-c', '--country', action='store_true', dest='country'),
        make_option('-p', '--capitals', action='store_true', dest='capital'),
        make_option('-z', '--timezone', action='store_true', dest='tz'),
        make_option('-m', '--currency', action='store_true', dest='currency'),
        # make_option('-r', '--region', action='store_true', dest='region'),
        # make_option('-i', '--ignore-cache', action='store_true', dest='reset'),
    )

    def handle(self, *args, **options):
        load_all = options.get('all')
        reset = options.get('currency')
        if load_all:
            region = tz= country = capital = currency = True
        else:
            country = options.get('country')
            capital = options.get('capital')
            tz = options.get('tz')
            currency = options.get('currency')

        if currency:
            self.stdout.write("Loading currencies...")
            load_currency(self.stdout)
        if country:
            self.stdout.write("Loading countries...")
            load_country(self.stdout)
        if tz:
            self.stdout.write("Loading timezones...")
            load_timezone(self.stdout)
