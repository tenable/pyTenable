import pytest
import responses

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
    Test was plugins search method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.was.plugins.search()
