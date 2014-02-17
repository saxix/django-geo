import pytest
import sys
from geo.utils import load_currency, load_country


@pytest.mark.django_db
def test_load_currency():
    load_currency()


@pytest.mark.django_db
def test_load_country():
    load_country()
