# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.db import transaction, IntegrityError
from geo.hierarchy import italy
from geo.loaders import load_timezone
from geo.models import Country, Currency
from geo.utils import load_currency, load_country


class Command(BaseCommand):
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='all'),
        make_option('--it', action='store_true', dest='it'),
        # make_option('-p', '--capitals', action='store_true', dest='capital'),
        # make_option('-z', '--timezone', action='store_true', dest='tz'),
        # make_option('-m', '--currency', action='store_true', dest='currency'),
        # make_option('-r', '--region', action='store_true', dest='region'),
        # make_option('-i', '--ignore-cache', action='store_true', dest='reset'),
    )

    def handle(self, *args, **options):
        load_all = options.get('all')
        all = options.get('all')

        if options.get('it') or all:
            italy()
