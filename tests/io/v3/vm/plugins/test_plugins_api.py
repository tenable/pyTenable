'''
test plugins
'''
import re

import requests
import responses

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tests.io.v3.vm.plugins.objects import (FAMILIES, FAMILY_FIELDS,
                                            FAMILY_FILTER, PLUGIN,
                                            PLUGIN_FIELDS, PLUGIN_FILTER,
                                            PLUGIN_ID, PLUGINS_IN_FAMILY,
                                            PLUGINS_IN_FAMILY_ID, PLUGINS_LIST)

BASE_URL = 'https://cloud.tenable.com/api/v3/plugins'


@responses.activate
def test_search_families(api):
    '''
    Test Plugin search families API
    '''
    response = {
        'families': FAMILIES,
        'pagination': {'total': len(FAMILIES), 'next': 'nextToken'}
    }

    api_payload = {
        'fields': FAMILY_FIELDS,
        'filter': FAMILY_FILTER,
        'limit': 2,
        'sort': [{'id': 'desc'}],
    }

    responses.add(
        responses.POST,
        f'{BASE_URL}/families/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )
    resp = api.v3.vm.plugins.search_families(
        fields=FAMILY_FIELDS,
        filter=FAMILY_FILTER,
        sort=[('id', 'desc')],
        limit=2
    )
    assert isinstance(resp, SearchIterator)

    for ind, family in enumerate(resp):
        assert family == FAMILIES[ind]

    resp = api.v3.vm.plugins.search_families(
        fields=FAMILY_FIELDS,
        filter=FAMILY_FILTER,
        sort=[('id', 'desc')],
        limit=2,
        return_csv=True
    )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.vm.plugins.search_families(
        fields=FAMILY_FIELDS,
        filter=FAMILY_FILTER,
        sort=[('id', 'desc')],
        limit=2,
        return_resp=True
    )
    assert isinstance(resp, requests.Response)


@responses.activate
def test_search(api):
    '''
    Test Plugin search families API
    '''
    response = {
        'plugins': PLUGINS_LIST['plugins'],
        'pagination': {
            'total': len(PLUGINS_LIST['plugins']),
            'next': 'nextToken'
        }
    }

    api_payload = {
        'fields': PLUGIN_FIELDS,
        'filter': PLUGIN_FILTER,
        'limit': 2,
        'sort': [{'name': 'desc'}],
    }

    responses.add(
        responses.POST,
        f'{BASE_URL}/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )
    resp = api.v3.vm.plugins.search(
        fields=PLUGIN_FIELDS,
        filter=PLUGIN_FILTER,
        sort=[('name', 'desc')],
        limit=2
    )
    assert isinstance(resp, SearchIterator)

    for ind, family in enumerate(resp):
        assert family == PLUGINS_LIST['plugins'][ind]

    resp = api.v3.vm.plugins.search(
        fields=PLUGIN_FIELDS,
        filter=PLUGIN_FILTER,
        sort=[('name', 'desc')],
        limit=2,
        return_csv=True
    )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.vm.plugins.search(
        fields=PLUGIN_FIELDS,
        filter=PLUGIN_FILTER,
        sort=[('name', 'desc')],
        limit=2,
        return_resp=True
    )
    assert isinstance(resp, requests.Response)


@responses.activate
def test_family_details(api):
    '''
    Test Plugins family_details API
    '''
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/families/{PLUGINS_IN_FAMILY_ID}'),
        json=PLUGINS_IN_FAMILY
    )
    family_details_response = api.v3.vm.plugins.family_details(
        PLUGINS_IN_FAMILY_ID
    )
    assert family_details_response == PLUGINS_IN_FAMILY


@responses.activate
def test_plugin_details(api):
    '''
    Test case for plugin_details api
    '''
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/plugin/{PLUGIN_ID}'),
        json=PLUGIN
    )
    plugin_detail_response = api.v3.vm.plugins.plugin_details(PLUGIN_ID)
    assert plugin_detail_response == PLUGIN
