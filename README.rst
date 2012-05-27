================
django-geo
================

.. image:: https://secure.travis-ci.org/saxix/django-geo/djangorecipe.png?branch=master
   :target: http://travis-ci.org/saxix/django-geo/

A Django application which manage administrative geographical data.
It use Modified Preorder Tree Traversal, provided by django-mptt `https://github.com/django-mptt/django-mptt/`

Geo is not intented to replace a GIS, but to manage all the cases where you have
administrative trees, with a strict/lazy hierarchy.

Models
======

* Country
* Area
* Location
* AdministrativeAreaType
* Currency

Examples
--------

 Three levels ::

    italy = Country.objects.get(iso_code='IT')
    regione, __ = italy.administrativeareatype_set.get_or_create(name='Regione')
    provincia,__ = italy.administrativeareatype_set.get_or_create(name='Provincia',
                                                                  parent=regione)
    comune, __= italy.administrativeareatype_set.get_or_create(name='Comune',
                                                               parent=provincia)
    lazio, __ = AdministrativeArea.objects.get_or_create(country=italy,
                                                         name ='Lazio',
                                                         type=regione)
    roma_provincia, __ = AdministrativeArea.objects.get_or_create(country=italy,
                                                                  name ='Provincia di Roma',
                                                                  type=provincia,
                                                                  parent=lazio)
    roma_comune, __ = AdministrativeArea.objects.get_or_create(country=italy,
                                                                name ='Comune di Roma',
                                                                type=comune,
                                                                parent=roma_provincia)
    roma, __  = Location.objects.get_or_create(country=italy,
                                                name ='Roma',
                                                type=Location.CITY,
                                                area=roma_comune)

 Two levels, ::

    us = Country.objects.get(iso_code='US')
    state, __ = italy.administrativeareatype_set.get_or_create(name='State')
    county,__ = italy.administrativeareatype_set.get_or_create(name='County',
                                                                parent=state)
    ny, __ = AdministrativeArea.objects.get_or_create(country=us,
                                                        name ='New York',
                                                        type=state)
    columbia, __ = AdministrativeArea.objects.get_or_create(country=us,
                                                            name ='Columbia',
                                                            type=county,
                                                            parent=ny)
    hudson, __  = Location.objects.get_or_create(country=us,
                                                 name ='Hudson',
                                                 type=Location.CITY,
                                                 area=columbia,
                                                 is_administrative=True)

