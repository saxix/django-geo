# -*- coding: utf-8 -*-
from django.apps import AppConfig as AC
from timezone_field import TimeZoneField


class AppConfig(AC):

    name = 'geo'
    label = 'geo'
    verbose_name = 'Geo'

    def ready(self):
        from bitfield.models import BitField

        def deconstruct_factory(model, **field_kwargs):
            def _dd(self):
                name, path, args, kwargs = super(model, self).deconstruct()
                kwargs.update(field_kwargs)
                return name, path, args, kwargs
            return _dd

        BitField.deconstruct = deconstruct_factory(BitField, flags=[])
        TimeZoneField.deconstruct = deconstruct_factory(TimeZoneField, choices=None)
