
def test_naturalkeys():
    pass

# class TestNaturalKeys(TransactionTestCase):
#
#     def test_dump_and_load(self):
#         import os
#         from geo.tests.fixtures import location_factory, currency_factory
#         from django.db import transaction
#         from django.core.management import call_command
#         import tempfile
#
#         tempfile = tempfile.mktemp('.json', 'geo')
#
#         location = location_factory()
#         currency = currency_factory()
#
#         with open(tempfile, 'w') as fixture_file:
#             call_command('dumpdata', use_natural_keys=True, stdout=fixture_file)
#
#         Currency.objects.all().delete()
#         Location.objects.all().delete()
#         Country.objects.all().delete()
#
#         self.assertEqual(Country.objects.all().count(), 0)
#         self.assertEqual(Location.objects.all().count(), 0)
#         self.assertEqual(Currency.objects.all().count(), 0)
#
#         try:
#             call_command('loaddata', tempfile, use_natural_keys=True, verbosity=0)
#         finally:
#             os.remove(tempfile)
#
#         self.assertEqual(Country.objects.all().count(), 1)
#         self.assertEqual(Location.objects.all().count(), 1)
#         self.assertEqual(Currency.objects.all().count(), 2)
#
