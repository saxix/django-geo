# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Input, TextInput
from geo.models import AdministrativeAreaType, AdministrativeArea, Country, Location

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        widgets = {
            'fullname': TextInput(attrs={'size': 100}),
            'iso_code': TextInput(attrs={'size': 2}),
            'iso3_code': TextInput(attrs={'size': 3}),
            'num_code': TextInput(attrs={'size': 5}),
#            'tld': TextInput(attrs={'size': 5}),
            }

class AreaForm(forms.ModelForm):
    class Meta:
        model = AdministrativeArea
        widgets = {
            'name': TextInput(attrs={'size': 100}),
            'code': TextInput(attrs={'size': 3}),
            }

class AdministrativeAreaTypeForm(forms.ModelForm):

    for_country = None
    def __init__(self, *args, **kwargs):
        super(AdministrativeAreaTypeForm, self).__init__(*args, **kwargs)
        for_country = kwargs.pop('for_country', self.for_country)
        if 'initial' in kwargs:
            self.fields['type'].queryset = AdministrativeAreaType.objects.filter(country=initial.country)
        elif for_country:
            self.fields['type'].queryset = AdministrativeAreaType.objects.filter(country=for_country)

    class Meta:
        model = AdministrativeArea
        widgets = {
            'code': TextInput(attrs={'size': 10}),
            }

def administrativeareatypeform_factory_for_country(country):
    """ returns a AdministrativeAreaForm type for a specific Country
        ie. only AdministrativeAreaType related to the Counry are allowed.
        used by the admin's inlines

    """
    if country is None:
        return AdministrativeAreaTypeForm
    name = str('%sAdministrativeAreaForm' % country.iso_code)
    args = {'for_country':country}
    return type(name, (AdministrativeAreaTypeForm,), args)
