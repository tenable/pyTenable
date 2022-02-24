import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)

WAS_PLUGINS_BASE_URL = 'https://cloud.tenable.com/api/v3/was/plugins'
ID = 1
PLUGIN = {
    'id': ID,
    'name': 'Scan Information',
    'risk_factor': 'info',
    'cpe': None,
    'cvss_vector': None,
    'cvss_base_score': None,
    'cvss3_vector': None,
    'cvss3_base_score': None,
    'cvss_score_source': None,
    'solution': None,
    'synopsis': 'Scan Information',
    'description': 'Provides scan information and statistics of plugins run.',
    'exploit_available': None,
    'see_also': [],
    'vuln_published': None,
    'patch_published': None,
    'plugin_published': '2017-03-31T00:00:00Z',
    'plugin_modified': '2017-03-31T00:00:00Z',
    'created_at': '2019-05-15T13:53:29.059Z',
    'updated_at': '2021-11-23T11:50:07.130781Z',
    'family': 'General',
    'policy': [],
    'wasc': [],
    'owasp': [],
    'cves': [],
    'owasp_asvs': [],
    'nist': [],
    'hipaa': [],
    'pci_dss': [],
    'iso': [],
    'capec': [],
    'disa_stig': [],
    'cwe': [],
    'bids': []
}


@responses.activate
def test_details(api):
    '''
    Test was plugins plugin_details method
    '''
    responses.add(
        responses.GET,
        f'{WAS_PLUGINS_BASE_URL}/{ID}',
        json=PLUGIN
    )
    plugin = api.v3.was.plugins.details(ID)
    assert isinstance(plugin, dict)
    assert plugin == PLUGIN


@responses.activate
def test_search(api):
    '''
    Test the search method
    '''
    fields = [
        'name',
        'type',
        'id'
    ]
    sort = [('family', 'desc')]
    filters = ('name', 'eq', 'Scan Information')

    payload = {
        'fields': fields,
        'filter': {
            'property': 'name',
            'operator': 'eq',
            'value': 'Scan Information'
        }
    }

    api_response = {
        'plugins': [
            {
                'plugin_id': 98000,
                'name': 'Scan Information',
                'family': 'General',
                'policy': []
            }
        ],
        'pagination': {
            'total': 1
        }
    }
    responses.add(
        responses.POST,
        f'{WAS_PLUGINS_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.was.plugins.search(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.was.plugins.search(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.was.plugins.search(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)
