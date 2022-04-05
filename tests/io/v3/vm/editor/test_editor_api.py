'''
Test Editor APIs
'''
from pathlib import Path

import requests
import responses

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tests.io.v3.vm.editor.objects import (CONFIGURATION_DETAILS,
                                           CONFIGURATION_ID, ETYPE, FAMILY_ID,
                                           FILE_ID, OBJECT_ID, PLUGIN_DETAILS,
                                           PLUGIN_ID, POLICY_ID, RESP_EXPECTED,
                                           TEMPALTE_SEARCH_FILTER,
                                           TEMPALTE_SEARCH_SORT, TEMPLATE,
                                           TEMPLATE_DETAILS, TEMPLATE_ID,
                                           TEMPLATE_SEARCH_FIELDS)

EDITOR_BASE_URL = 'https://cloud.tenable.com/api/v3/editor'


@responses.activate
def test_obj_details(api):
    '''
    Test editor obj_details
    '''
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/{CONFIGURATION_ID}',
        json=CONFIGURATION_DETAILS
    )
    resp = api.v3.vm.editor.obj_details(ETYPE, CONFIGURATION_ID)
    assert resp == CONFIGURATION_DETAILS


@responses.activate
def test_search_templates(api):
    '''
    Test editor search_templates
    '''
    response = {
        'templates': [TEMPLATE],
        'pagination': {'total': 1, 'next': 'nextToken'}
    }

    api_payload = {
        'fields': TEMPLATE_SEARCH_FIELDS,
        'filter': TEMPALTE_SEARCH_FILTER,
        'limit': 2,
        'sort': [{'title': 'desc'}],
    }

    responses.add(
        responses.POST,
        f'{EDITOR_BASE_URL}/{ETYPE}/templates/search',
        json=response,
        match=[responses.matchers.json_params_matcher(api_payload)]
    )
    resp = api.v3.vm.editor.search_templates(
        etype=ETYPE,
        fields=TEMPLATE_SEARCH_FIELDS,
        filter=TEMPALTE_SEARCH_FILTER,
        sort=TEMPALTE_SEARCH_SORT,
        limit=2
    )
    assert isinstance(resp, SearchIterator)

    for template in resp:
        assert template == response['templates'][0]

    resp = api.v3.vm.editor.search_templates(
        etype=ETYPE,
        fields=TEMPLATE_SEARCH_FIELDS,
        filter=TEMPALTE_SEARCH_FILTER,
        sort=TEMPALTE_SEARCH_SORT,
        limit=2,
        return_csv=True
    )
    assert isinstance(resp, CSVChunkIterator)

    resp = api.v3.vm.editor.search_templates(
        etype=ETYPE,
        fields=TEMPLATE_SEARCH_FIELDS,
        filter=TEMPALTE_SEARCH_FILTER,
        sort=TEMPALTE_SEARCH_SORT,
        limit=2,
        return_resp=True
    )
    assert isinstance(resp, requests.Response)


@responses.activate
def test_template_details(api):
    '''
    Test editor template_details
    '''
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/templates/{TEMPLATE_ID}',
        json=TEMPLATE_DETAILS
    )
    resp = api.v3.vm.editor.template_details(ETYPE, TEMPLATE_ID)
    assert resp == TEMPLATE_DETAILS


@responses.activate
def test_plugin_description(api):
    '''
    Test editor plugin_description
    '''
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/policy/{POLICY_ID}/families/{FAMILY_ID}/plugins'
        f'/{PLUGIN_ID}',
        json=PLUGIN_DETAILS
    )
    resp = api.v3.vm.editor.plugin_description(POLICY_ID, FAMILY_ID, PLUGIN_ID)
    assert resp == PLUGIN_DETAILS['plugindescription']


@responses.activate
def test_audits(api):
    '''
    Test editor audits
    '''
    sample_report = Path(__file__).parent / Path('audit.txt')

    with open(sample_report, 'rb') as report:
        file_contents = report.read()

    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/{OBJECT_ID}/audits/{FILE_ID}',
        body=file_contents
    )

    received_report = Path(__file__).parent / Path('downloaded_audit.txt')
    with open(received_report, 'wb') as report:
        api.v3.vm.editor.audits(ETYPE, OBJECT_ID, FILE_ID, report)

    with open(received_report, 'rb') as report:
        assert report.read() == file_contents

    received_report.unlink()


@responses.activate
def test_details(api):
    '''
    Test editor details
    '''
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/{CONFIGURATION_ID}',
        json=CONFIGURATION_DETAILS
    )
    resp = api.v3.vm.editor.details(ETYPE, CONFIGURATION_ID)

    assert resp == RESP_EXPECTED
