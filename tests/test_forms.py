# -*- coding: utf-8 -*-
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django_dynamic_fixture import G
from geo.forms import administrativeareatypeform_factory_for_country
from geo.models import Country, AdministrativeArea
from .fixtures import hierachy


@pytest.mark.django_db
def test_administrativeareatypeform_factorye(hierachy):
    italy, regione, provincia, comune = hierachy
    Form = administrativeareatypeform_factory_for_country(italy)
    print 11111111, Form()
