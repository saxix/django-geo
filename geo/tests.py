from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from geo.models import Country, AdministrativeArea, Location


class Test(TestCase):
    fixtures = ['geo_test.json']

    def test_consistency1(self):
        """ a Type cannot contain the same type
        """
        italy = Country.objects.get(iso_code='IT')
        regione = italy.administrativeareatype_set.get(name='Regione')
        lazio = italy.areas.get(name='Lazio')
        self.assertRaises(ValidationError, AdministrativeArea.objects.create,
            name='Lombardia',
            parent=lazio,
            type=regione)

    def test_consistency2(self):
        """ a Type cannot contain the parent type
        """
        italy = Country.objects.get(iso_code='IT')
        comune = italy.areas.get(name='Comune di Roma')
        lazio = italy.areas.get(name='Lazio')
        lazio.parent = comune
        self.assertRaises(ValidationError, lazio.save)

    def test_country_inheritance(self):
        """ a Type cannot contain the parent type
        """
        roma_provincia = AdministrativeArea.objects.get(
            country__iso_code='IT', parent__name='Lazio')

        italy = Country.objects.get(iso_code='IT')
        comune = italy.administrativeareatype_set.get(name='Comune')
        new_comune, __ = AdministrativeArea.objects.get_or_create(name='Comune di Viterbo',
            type=comune, parent=roma_provincia)
        self.assertEqual(new_comune.country, roma_provincia.country)

    def test_in_country(self):
        """ a Type cannot contain the parent type
        """
        italy = Country.objects.get(iso_code='IT')
        lazio = italy.areas.get(name='Lazio')
        self.assertTrue(lazio in italy)

    def test_in_country(self):
        """ a Type cannot contain the parent type
        """
        italy = Country.objects.get(iso_code='IT')
        lazio = italy.areas.get(name='Lazio')
        comune = italy.areas.get(name='Comune di Roma')
        self.assertTrue(comune in lazio)

    def test_unique_together(self):
        italy = Country.objects.get(iso_code='IT')
        regione = italy.administrativeareatype_set.get(name='Regione')
        lazio2 = AdministrativeArea(name='Lazio', country=italy, type=regione)
        self.assertRaises(IntegrityError, lazio2.save)
