import xlrd
import logging
from django.core.management.base import BaseCommand
from optparse import make_option
from geo.models import Country, AdministrativeAreaType, AdministrativeArea, LocationType, Location
from django.db import transaction

log = logging.getLogger(__name__)


@transaction.commit_on_success()
def import_geo_xls(country, filename):
    """ imports all geographical data for one country and creates any missing records

        Example how structure maps to excel file:

        Country
            Type1
                Type1A
                Type1B
                    Type1B1
                    Type1B2
            Type2

        row0 on sheet "Type1-0": [Type1][Type1A][Location][Location Type]
        row0 on sheet "Type1-1": [Type1][Type1B][Type1B1][Location][Location Type]
        row0 on sheet "Type1-2": [Type1][Type1B][Type1B2][Location][Location Type]
        row0 on sheet "Type2-0": [Type2][Location][Location Type]

    """
    book = xlrd.open_workbook(filename)
    for sheet in book.sheets():
        assert sheet.cell(0, sheet.ncols-1).value == u'Location type'
        assert sheet.cell(0, sheet.ncols-2).value == u'Location'

        # read header and create any missing admin types
        row_adm_types = sheet.row_values(0, 0, sheet.ncols-2)
        adm_type_per_column = []
        for adm_type_name in row_adm_types:
            parent_adm_type = None if len(adm_type_per_column) == 0 else adm_type_per_column[-1]
            try:
                adm_type = AdministrativeAreaType.objects.get(country=country, name=adm_type_name,
                                                              parent=parent_adm_type)
            except AdministrativeAreaType.DoesNotExist:
                log.debug("create adm area type with name '{}' and parent type name '{}'"
                          "".format(adm_type_name, parent_adm_type))
                adm_type = AdministrativeAreaType(name=adm_type_name, country=country, parent=parent_adm_type)
                adm_type.save()
            else:
                log.debug("already exists adm area type with name '{}' and parent type name '{}'"
                          "".format(adm_type_name, parent_adm_type))

            adm_type_per_column.append(adm_type)

        # create any missing administrative areas
        for col_index, adm_type in enumerate(adm_type_per_column):
            adm_areas_of_type = set(sheet.col_values(col_index, 1, sheet.nrows))
            for adm_area_name in adm_areas_of_type:
                try:
                    adm_area = AdministrativeArea.objects.get(country=country, type=adm_type, name=adm_area_name)
                except AdministrativeArea.DoesNotExist:
                    log.debug("create adm area with type '{}' and name '{}'".format(adm_type, adm_area_name))
                    adm_area = AdministrativeArea(country=country, type=adm_type, name=adm_area_name)
                    adm_area.save()
                else:
                    log.debug("already exists adm area with type '{}' and name '{}'".format(adm_type, adm_area_name))

        # create any missing location types
        location_types = set(sheet.col_values(sheet.ncols-1, 1, sheet.nrows))
        for loc_type_name in location_types:
            try:
                loc_type = LocationType.objects.get(description=loc_type_name)
            except Location.DoesNotExist:
                log.debug("create location type with description '{}'".format(loc_type_name))
                loc_type = LocationType(description=loc_type_name)
                loc_type.save()
            else:
                log.debug("already exists location type with description '{}'".format(loc_type_name))

        # create locations (at this point, all referred objects exists)
        for row_index in xrange(1, sheet.nrows):
            if sheet.ncols >= 3:
                adm_type_name = sheet.cell(0, sheet.ncols-3).value
                adm_area_name = sheet.cell(row_index, sheet.ncols-3).value
                print "'{}' '{}'".format(adm_type_name, adm_area_name)
                adm_area = AdministrativeArea.objects.get(country=country, type__name=adm_type_name, name=adm_area_name)
            else:
                adm_area = None
            loc_type_description = sheet.cell(row_index, sheet.ncols-1).value
            try:
                location = Location.objects.get(country=country, area=adm_area, type__description=loc_type_description)
            except Location.DoesNotExist:
                log.debug("create location with nane '{}' under admin area '{}'".format(loc_type_name, adm_area.name))
                location = Location(country=country, area=adm_area)
                location.type = LocationType.objects.get(description=loc_type_description)
                location.save()
            else:
                log.debug("already exist location with nane '{}' under admin area '{}'"
                          "".format(loc_type_name, adm_area.name))


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country-iso3', dest='country_iso3', action='store',
                    help='Country for which the export will be made.'),
        make_option('--file', action='store', dest='filename', default=False,
                    help='Filename to be used (if not provided will be: "{country_name}_geo.xls".'),
    )
    help = "Output geo-location data in an excel file for a country, can be imported by import_xls"

    def handle(self, *app_labels, **options):
        try:
            country = Country.objects.get(iso3=options['country_iso3'])
        except Country.DoesNotExist:
            print "Country with iso3 code: '{}' does not exists".format(options['country_iso3'])
            return
        if options['filename'] is None:
            options['filename'] = '{0.name}_geo.xls'.format(country)
        import_geo_xls(country, options['filename'])
