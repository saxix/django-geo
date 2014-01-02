from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest
from django.core.urlresolvers import reverse
import django_webtest
from .base import superuser
from geo.models import Country
from tests.fixtures import country_factory


@pytest.fixture(scope='function')
def app(request):
    wtm = django_webtest.WebTestMixin()
    wtm._patch_settings()
    wtm._setup_auth()
    request.addfinalizer(wtm._unpatch_settings)
    return django_webtest.DjangoTestApp()

@pytest.mark.django_db(transaction=False)
def test_admin(app, superuser):
    url = reverse('admin:geo_country_changelist')
    country_factory(n=10)

    res = app.get(url, user=superuser.username)
    res = res.click('^Country-1$')

# class TestAdmin(django_webtest.WebTest):
#     def test_country(self):
#         superuser= User.objects.create_superuser('superuser','','123')
#         url = reverse('admin:geo_country_changelist')
#         res = self.app.get(url, user=superuser.username)
#         res.showbrowser()
