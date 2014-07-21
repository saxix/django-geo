from django_dynamic_fixture import G
import pytest
from geo.models import Country


@pytest.mark.django_db
def test_issue_2():
    G(Country, currency=None)
