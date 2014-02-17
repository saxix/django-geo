# -*- coding: utf-8 -*-
import pytest
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django_dynamic_fixture import G
from geo.forms import administrativeareaform_factory_for_country
from geo.models import Country, AdministrativeArea, AdministrativeAreaType
from .fixtures import hierachy


# # @pytest.mark.django_db
# def test_administrativeareatypeform_factory):
#     Form = administrativeareatypeform_factory_for_country(Country())
#     instance  = AdministrativeAreaType()
#     form = Form(instance=instance)
#     assert not form.is_valid()

@pytest.mark.django_db
def test_administrativeareaform_factory(hierachy):
    italy, regione, provincia, comune = hierachy
    Form = administrativeareaform_factory_for_country(italy)
    instance = AdministrativeArea()
    form = Form({'name': 'Lazio',
                 'type': regione.pk,
                 'country': italy.pk},
                instance=instance)
    form.full_clean()
    assert form.is_valid()
