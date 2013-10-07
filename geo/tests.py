from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from geo.models import Country, AdministrativeArea, Location


class Test(TestCase):
    fixtures = ['geo_test.json']

    def test_validator_country_iso_code(self):
        c = Country(name='a', fullname='aa', iso_code='a', iso3_code='aaa', num_code='123', continent='AS')
        self.assertRaises(ValidationError, c.full_clean, )

    def test_validator_country_iso3_code(self):
        c = Country(name='a', fullname='aa', iso_code='aa', iso3_code='aa', num_code='123', continent='AS')
        self.assertRaises(ValidationError, c.full_clean, )

    def test_validator_country_num_code(self):
        c = Country(name='a', fullname='aa', iso_code='aa', iso3_code='aaa', num_code='aaa', continent='AS')
        self.assertRaises(ValidationError, c.full_clean, )

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

    def test_regione_in_country(self):
        """ a Type cannot contain the parent type
        """
        italy = Country.objects.get(iso_code='IT')
        lazio = italy.areas.get(name='Lazio')
        self.assertTrue(lazio in italy)

    def test_comune_in_regione(self):
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

    def test_same_name_for_location_in_diff_area(self):
        italy = Country.objects.get(iso_code='IT')
        fiumicino = italy.areas.get(name='Comune di Fiumicino')
        # No Roma location within Fiumicino council: just for testing.
        roma2 = Location(name="Roma", country=italy, area=fiumicino)
        roma2.save()
        all_roma = Location.objects.filter(name='Roma')
        self.assertTrue(len(all_roma), 2)
        self.assertTrue(roma2.area, fiumicino)

    def test_unique_together_location_within_same_area(self):
        italy = Country.objects.get(iso_code='IT')
        comune = italy.administrativeareatype_set.get(name='Comune')
        area_comune = AdministrativeArea(name='Area Comune', country=italy, type=comune)
        area_comune.save()
        location_1 = Location(name="Magliana", area=area_comune, country=italy)
        location_1.save()
        # duplicate location in the same area
        location_2 = Location(name="Magliana", area=area_comune, country=italy)
        self.assertRaises(IntegrityError, location_2.save)

    def test_no_area_of_same_name_and_type_within_a_country(self):
        italy = Country.objects.get(iso_code='IT')
        comune = italy.administrativeareatype_set.get(name='Comune')
        an_area = AdministrativeArea(name='Cool Area', country=italy, type=comune)
        an_area.save()
        # duplicate area (name and type) in the same country
        another_area = AdministrativeArea(name='Cool Area', country=italy, type=comune)
        self.assertRaises(IntegrityError, another_area.save)

    def test_natural_key_if_no_lat_lng(self):
        location_1 = Location.objects.get(name="Roma")
        location_2 = Location.objects.get_by_natural_key(location_1.natural_key())
        self.assertEquals(location_1.pk, location_2.pk)

    def test_natural_key_with_lat_lng(self):
        location_1 = Location.objects.get(name="Bracciano")
        location_2 = Location.objects.get_by_natural_key(location_1.natural_key())
        self.assertEquals(location_1.pk, location_2.pk)

    def test_administrativearea_natural_key(self):
        area = AdministrativeArea.objects.get(country__iso_code='IT', parent__name='Lazio')
        location_2 = AdministrativeArea.objects.get_by_natural_key(area.natural_key())
        self.assertEquals(area.pk, location_2.pk)
