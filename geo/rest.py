import logging

from datetime import datetime
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import cache, exceptions
from django.core.urlresolvers import reverse
from geo.models import Country, Currency
from pytz import timezone
from rest_framework import serializers, pagination

#
# Serializers
#

class BaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        exclude = ('last_modified_user', 'security_hash')


class CountrySerializer(BaseSerializer):
    class Meta:
        model = Country


class CountryLookupSerializer(BaseSerializer):
    class Meta:
        model = Country
        fields = ('name', 'id')


class CurrencySerializer(BaseSerializer):
    class Meta:
        model = Currency


#
# Views
#
class AbstractListView(ListAPIView):
    permission_classes = (AllowAny, )
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    #permission_classes = (permissions.IsAuthenticated, IsOwner)
    renderer_classes = (UnicodeJSONRenderer, JSONPRenderer, BrowsableAPIRenderer, YAMLRenderer, XMLRenderer)
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100


class CountryListView(AbstractListView):
    search_fields = ['name', 'fullname', ]
    serializer_class = CountrySerializer
    pagination_serializer_class = CustomPaginationSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('iso_code', 'iso3_code', 'num_code', 'name')

    def get_queryset(self):
        return Country.objects.all().order_by('name')

