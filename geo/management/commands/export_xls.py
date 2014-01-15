import xlwt
import logging
from geo.models import Country, AdministrativeAreaType, Location, AdministrativeArea, LocationType
from optparse import make_option
from django.core.management.base import BaseCommand


log = logging.getLogger(__name__)


def paths_root_to_leaf(node):
    """ yield each possible path from node to root
    """
    for leaf in node.get_leafnodes(include_self=True):
        path_to_root = [leaf]
        ancestor = leaf.parent
        while ancestor is not None:
            path_to_root.append(ancestor)
            ancestor = ancestor.parent
        yield list(reversed(path_to_root))


def geo_data(leaf_area_type):
    """ yield for each location (adm-area1, .., adm-area-leaf, location, location type)
    where adm-area-leaf.type == leaf_area_type
    """
    leaf_adm_areas = AdministrativeArea.objects.filter(type=leaf_area_type).all()
    for leaf_adm_area in leaf_adm_areas:
        paths_to_root = list(paths_root_to_leaf(leaf_adm_area))
        assert len(paths_to_root) == 1
        adm_areas = paths_to_root[0]
        locations = Location.objects.filter(area=leaf_area_type)
        for location in locations:
            row = adm_areas
            row.append(location)
            row.append(location.type)
            yield row


def export_geo_xls(country, filename):
    """ exports all geographical data for one country

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
    adm_type_roots = AdministrativeAreaType.objects.filter(country=country, parent=None).all()
    book = xlwt.Workbook()
    for root in adm_type_roots:
        for structure_index, path in enumerate(paths_root_to_leaf(root)):
            sheet = book.add_sheet('{}-{}'.format(root.name, structure_index))
            # write header row with name of area-types
            for col_index, node in enumerate(path):
                sheet.write(0, col_index, node.name)
            sheet.write(0, col_index+1, "Location")
            sheet.write(0, col_index+2, "Location type")
            # write each location and on that row, its upper administrative areas and location type
            leaf_area_type = path[-1]
            for row_index, row in enumerate(geo_data(leaf_area_type)):
                for col_index, value in enumerate(row):
                    if isinstance(value, LocationType):
                        sheet.write(row_index+1, col_index, value.description)
                    else:
                        sheet.write(row_index+1, col_index, value.name)
    book.save(filename)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--country-iso3', dest='country_iso3', action='store',
                    help='Country for which the export will be made.'),
        make_option('-o', '--out', action='store', dest='filename', default=False,
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
        export_geo_xls(country, options['filename'])
