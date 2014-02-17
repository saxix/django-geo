# -*- coding: utf-8 -*-
from geo.config import conf
from django.core.urlresolvers import get_callable


def load_currency(stdout=None):
    func = get_callable(conf.LOAD_CURRENCY_FUNC)
    return func(stdout=stdout)


def load_country(stdout=None):
    func = get_callable(conf.LOAD_COUNTRY_FUNC)
    return func(stdout=stdout)
