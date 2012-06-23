.. |mnt| replace:: Django Site Maintenance
.. _exapmples:

Examples
========

Two levels
----------

    Country / City

::

    italy = Country.objects.get(iso_code='IT')
    roma_city, __  = Location.objects.get_or_create(country=italy,
                                                name ='Roma',
                                                type=Location.CITY)


Three levels
------------

    Country / Regione / City

::

    italy = Country.objects.get(iso_code='IT')
    regione, __ = italy.administrativeareatype_set.get_or_create(name='Regione')


    lazio, __ = AdministrativeArea.objects.get_or_create(country=italy,
                                                             name ='Lazio',
                                                             type=regione)

    roma_city, __  = Location.objects.get_or_create(country=italy,
                                                name ='Roma',
                                                type=Location.CITY,
                                                area=lazio)

Four levels
-----------

 Represtent US administrative hierarchy:

 Structure:

    Country / State / County / Location

 Es.

    United States   / New York   / Columbia / Hudson

    United States   / New York   / Albany / Albany


::

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



Five levels
-----------

 Represtent Italy administrative hierarchy:

 Structure:

    Country / Regione / Provincia / Comune / Location

 Es.

    Italy   / Lazio   / Provincia di Roma / Comune di Roma / Roma

    Italy   / Lazio   / Provincia di Roma / Comune di Roma / Ostia

    Italy   / Lazio   / Provincia di Roma / Comune di Ciampino / Ostia



::

    italy = Country.objects.get(iso_code='IT')

    # create administrative structure for Italy
    regione, __ = italy.administrativeareatype_set.create(name='Regione')
    provincia,__ = italy.administrativeareatype_set.get_or_create(name='Provincia',
                                                                  parent=regione)

    comune, __= italy.administrativeareatype_set.get_or_create(name='Comune',
                                                               parent=provincia)


    # add local administrative instances
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
    roma_city, __  = Location.objects.get_or_create(country=italy,
                                                name ='Roma',
                                                type=Location.CITY,
                                                area=roma_comune)

