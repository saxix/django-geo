================
django-geo
================

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

 Three levels

.. code-block:: python

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
    city, __ = LocationType.objects.get_or_create(description='CITY')
    roma, __  = Location.objects.get_or_create(country=italy,
                                                name ='Roma',
                                                type=city,
                                                area=roma_comune)

Two levels

 .. code-block:: python

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
    city, __ = LocationType.objects.get_or_create(description='CITY')
    hudson, __  = Location.objects.get_or_create(country=us,
                                                 name ='Hudson',
                                                 type=city,
                                                 area=columbia,
                                                 is_administrative=True)


Links
~~~~~

+--------------------+----------------+--------------+----------------+
| Stable             | |master-build| | |master-cov| | |master-req|   |
+--------------------+----------------+--------------+----------------+
| Development        | |dev-build|    | |dev-cov|    | |dev-req|      |
+--------------------+----------------+--------------+----------------+
| Project home page: |https://github.com/saxix/django-geo             |
+--------------------+---------------+--------------------------------+
| Issue tracker:     |https://github.com/saxix/django-geo/issues?sort |
+--------------------+---------------+--------------------------------+
| Download:          |http://pypi.python.org/pypi/django-geo/         |
+--------------------+---------------+--------------------------------+
| Documentation:     |https://django-geo.readthedocs.org/en/latest/   |
+--------------------+---------------+--------------+-----------------+

.. |master-build| image:: https://secure.travis-ci.org/saxix/django-geo.png?branch=master
                    :target: http://travis-ci.org/saxix/django-geo/

.. |master-cov| image:: https://coveralls.io/repos/saxix/django-geo/badge.png?branch=master
                    :target: https://coveralls.io/r/saxix/django-geo

.. |master-req| image:: https://requires.io/github/saxix/django-geo/requirements.png?branch=master
                    :target: https://requires.io/github/saxix/django-geo/requirements/?branch=master
                    :alt: Requirements Status


.. |dev-build| image:: https://secure.travis-ci.org/saxix/django-geo.png?branch=develop
                    :target: http://travis-ci.org/saxix/django-geo/

.. |dev-cov| image:: https://coveralls.io/repos/saxix/django-geo/badge.png?branch=develop
                :target: https://coveralls.io/r/saxix/django-geo

.. |dev-req| image:: https://requires.io/github/saxix/django-geo/requirements.png?branch=develop
                :target: https://requires.io/github/saxix/django-geo/requirements/?branch=develop
                :alt: Requirements Status

