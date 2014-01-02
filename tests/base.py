from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest
from geo.hierarchy import italy
from geo.models import Country


@pytest.fixture
def hierachy():
    G(Country, iso_code='IT', iso_code3='ITA', iso_num=380,
              name='Italy', fullname='Italy, Italian Republic')

    return italy()

@pytest.fixture
def superuser():
    try:
        return User.objects.get(is_superuser=True)
    except User.DoesNotExist:
         return User.objects.create_superuser('superuser','','123')
