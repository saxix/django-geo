# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.forms.widgets import Input, TextInput
from mptt.forms import TreeNodeChoiceField
from geo.models import AdministrativeAreaType, AdministrativeArea, Country, Location


class IsoCode2Field(CharField):
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        max_length = 2
        super(IsoCode2Field, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        if value:
            value = value.strip().upper()
        return super(IsoCode2Field, self).clean(value)


class IsoCode3Field(CharField):
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        max_length = 3
        super(IsoCode3Field, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        if value:
            value = value.strip().upper()
        return super(IsoCode3Field, self).clean(value)


class IsoNumericField(CharField):
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        max_length = 3
        super(IsoNumericField, self).__init__(max_length, min_length, *args, **kwargs)

    def clean(self, value):
        try:
            if value:
                value = '%03d' % int(value.strip().upper())
        except Exception as e:
            raise ValidationError(e)
        return super(IsoNumericField, self).clean(value)


class CountryForm(forms.ModelForm):
    iso_code = IsoCode2Field()
    iso_code3 = IsoCode3Field()
    iso_num = IsoNumericField()

    class Meta:
        model = Country
        exclude = ('pk', )
        widgets = {
            'fullname': TextInput(attrs={'size': 100}),
            # 'iso_code': TextInput(attrs={'size': 2}),
            # 'iso_code3': TextInput(attrs={'size': 3}),
            # 'num_code': TextInput(attrs={'size': 5}),
            # 'tld': TextInput(attrs={'size': 5}),
        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = AdministrativeArea
        exclude = ('pk', )
        widgets = {'name': TextInput(attrs={'size': 100}),
                   'code': TextInput(attrs={'size': 3})}


class AdministrativeAreaForm(forms.ModelForm):
    for_country = None

    def __init__(self, *args, **kwargs):
        super(AdministrativeAreaForm, self).__init__(*args, **kwargs)
        for_country = kwargs.pop('for_country', self.for_country)
        if 'initial' in kwargs:
            self.fields['type'].queryset = AdministrativeAreaType.objects.filter(country=initial.country)
        elif for_country:
            self.fields['type'].queryset = AdministrativeAreaType.objects.filter(country=for_country)

    class Meta:
        model = AdministrativeArea
        exclude = ('pk', )
        widgets = {
            'code': TextInput(attrs={'size': 10}),
        }


class LocationForm(forms.ModelForm):
    area = TreeNodeChoiceField(AdministrativeArea.objects.all(), required=False)

    class Meta:
        model = Location
        fields = ('area', 'country', 'type', 'is_capital',
                  'is_administrative', 'name',
                  'loccode', 'description', 'lat', 'lng', 'acc', 'flags', 'status')
        widgets = {
            'code': TextInput(attrs={'size': 10}),

        }


def administrativeareaform_factory_for_country(country):
    """ returns a AdministrativeAreaForm type for a specific Country
        ie. only AdministrativeAreaType related to the Counry are allowed.
        used by the admin's inlines

    """
    if country is None:
        return AdministrativeAreaForm
    name = str('%sAdministrativeAreaForm' % country.iso_code)
    args = {'for_country': country}
    return type(name, (AdministrativeAreaForm,), args)
