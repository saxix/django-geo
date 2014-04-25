# -*- coding: utf-8 -*-
import pytest
from geo.forms import administrativeareaform_factory_for_country
from geo.models import AdministrativeArea
from .fixtures import hierachy


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
