from django.contrib.auth.models import User
from django_dynamic_fixture import G
import pytest
from django.core.urlresolvers import reverse
import django_webtest
from .fixtures import superuser, hierachy
from geo.models import Country, AdministrativeAreaType, AdministrativeArea
from tests.fixtures import country_factory, area_tree_factory


@pytest.fixture(scope='function')
def app(request):
    wtm = django_webtest.WebTestMixin()
    wtm._patch_settings()
    wtm._setup_auth()
    request.addfinalizer(wtm._unpatch_settings)
    return django_webtest.DjangoTestApp()


@pytest.mark.django_db(transaction=False)
def test_country_update(app, superuser):
    url = reverse('admin:geo_country_changelist')
    country_factory(n=10)

    res = app.get(url, user=superuser.username)
    res = res.click('^Country-1$')
    res = res.form.submit().follow()


@pytest.mark.django_db(transaction=True)
def test_areatype_update(app, hierachy, superuser):
    italy, regione, provincia, comune = hierachy
    url = reverse('admin:geo_administrativeareatype_changelist')

    res = app.get(url, user=superuser.username)
    res = res.click('^Regione$')
    res = res.form.submit().follow()


@pytest.mark.django_db(transaction=True)
def test_area_update(app, hierachy, superuser):
    italy, regione, provincia, comune = hierachy
    G(AdministrativeArea, type=regione, name='Lazio', country=italy)
    url = reverse('admin:geo_administrativearea_changelist')

    res = app.get(url, user=superuser.username)
    res = res.click('^Lazio$')
    res = res.form.submit().follow()
