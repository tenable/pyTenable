'''
test vulns
'''
import re
import pytest
import responses
from box import Box
from tests.ot.conftest import ot as fixture_ot

def load_responses(responses):
    '''
    A centralized location for these larger responses to be used in this testing
    module
    '''
    responses.add(
        method='GET',
        url='https://localhost:443/v1/vulnerabilities',
        json=[
            {'comment': '',
             'cpeTree': None,
             'cvss': {'accessComplexity': 'LOW',
                      'accessVector': 'NETWORK',
                      'authentication': 'NONE',
                      'availabilityImpact': 'COMPLETE',
                      'confidentialityImpact': 'COMPLETE',
                      'integrityImpact': 'COMPLETE',
                      'score': 10},
             'descriptions': [{'cveId': 'CVE-2020-9633',
                               'language': 'en',
                               'value': 'Adobe Flash Player Desktop Runtime 32.0.0.371 and '
                                        'earlier, Adobe Flash Player for Google Chrome '
                                        '32.0.0.371 and earlier, and Adobe Flash Player '
                                        'for Microsoft Edge and Internet Explorer '
                                        '32.0.0.330 and earlier have an use after free '
                                        'vulnerability. Successful exploitation could lead '
                                        'to arbitrary code execution.'}],
             'id': 'CVE-2020-9633',
             'lastModifiedDate': '2020-07-06T14:15:00Z',
             'publishedDate': '2020-06-12T14:15:00Z',
             'references': [{'cveId': 'CVE-2020-9633',
                             'name': 'https://helpx.adobe.com/security/products/flash-player/apsb20-30.html',
                             'source': 'CONFIRM',
                             'url': 'https://helpx.adobe.com/security/products/flash-player/apsb20-30.html'},
                            {'cveId': 'CVE-2020-9633',
                             'name': 'GLSA-202006-09',
                             'source': 'GENTOO',
                             'url': 'https://security.gentoo.org/glsa/202006-09'}],
             'tvi': {'cveId': 'CVE-2020-9633',
                     'cvssV3Score': 5.9,
                     'exploitCodeMaturity': 'UnprovenExploitCodeMaturity',
                     'productCoverage': 'LowProductCoverage',
                     'threatIntensity': 'VeryLowThreatIntensity',
                     'threatRecency': 'From120To365DaysThreatRecency',
                     'threatSources': ['NoRecordedEventsThreatSource'],
                     'vprScore': 5.9,
                     'vulnerabilityAge': 'From60To180DaysVulnerabilityAge'}},
        ]
    )
    responses.add(
        method='POST',
        url=re.compile('https://localhost:443/v1/vulnerabilities/[^/]+/assets'),
        json=[{
            'id': '8fe5cdb1-723e-4996-9d3c-7787445bc38a',
            'name': 'CP-487F0A',
            'firstSeen': '2020-04-15T20:27:50.750495Z',
            'lastSeen': '2020-04-20T14:40:13.533982Z',
            'addresses': ['192.168.101.154'],
            'directAddresses': ['192.168.101.154'],
            'type': 'PlcType',
            'purdueLevel': 'Level1',
            'vendor': 'Beckhoff',
            'runStatus': 'Unknown',
            'runStatusTime': '0001-01-01T00:00:00Z',
            'os': 'Windows 7 Service Pack 1',
            'family': 'C-Series',
            'firmwareVersion': '3.1.4024',
            'risk': 69.03533650200879,
            'criticality': 'HighCriticality',
            'hidden': False,
            'site': 'e4f7997b-8470-483c-a4b2-8fddcae22df3'
        }]
    )
    responses.add(
        method='GET',
        url=re.compile('https://localhost:443/v1/assets/[^/]+/connections'),
        json=[{
            'asset': '8fe5cdb1-723e-4996-9d3c-7787445bc38a',
            'networkInterface': 'd7f06b04-5733-44ac-9e84-096f6fdb181b',
            'local': True,
            'direct': True,
            'connector': {
                'parts': [
                    {'connectionType': 'Direct'}
                ]
            }
        }]
    )
    responses.add(
        method='GET',
        url=re.compile('https://localhost:443/v1/networkinterfaces/.*'),
        json={
            'id': 'd7f06b04-5733-44ac-9e84-096f6fdb181b',
            'ips': ['192.168.101.154'],
            'dnsNames': None,
            'lastSeen': '2020-07-09T00:10:51.125735Z',
            'firstSeen': '2020-07-09T00:01:22.618953Z',
            'family': 'Unknown'
        }
    )


@responses.activate
def test_vuln_asset_intermixer(fixture_ot):
    '''
    Tests the intermixer iterator
    '''
    load_responses(responses)
    vulns = fixture_ot.vulns.extract()

    # assert the iterator returns itself.
    assert vulns == vulns.__iter__()

    # as __next__() calls next(), we will use the internal method to clear the
    # testing requirements.
    vuln = vulns.__next__()

    assert vuln.asset.id == '8fe5cdb1-723e-4996-9d3c-7787445bc38a'
    assert vuln.asset.connections
    assert vuln.asset.connections[0].networkInterface.id == 'd7f06b04-5733-44ac-9e84-096f6fdb181b'
    assert vuln.cvss.score == 10

    # Validate that merge_cache should always return the same asset cache.
    data = vulns._merge_cache(Box({'id': '8fe5cdb1-723e-4996-9d3c-7787445bc38a'}))
    assert vuln.asset.id == data.asset.id
    assert vuln.id == data.id

    # test that the stop iterator works as expected.
    with pytest.raises(StopIteration):
        vulns.next()


@responses.activate
def test_list(fixture_ot):
    '''
    Tests the list method
    '''
    load_responses(responses)
    vulns = fixture_ot.vulns.list()

    for vuln in vulns:
        assert vuln.id == 'CVE-2020-9633'
        assert vuln.cvss.score == 10


@responses.activate
def test_assets_list(fixture_ot):
    '''
    test to list the assets
    '''
    responses.add(
        method='GET',
        url='https://localhost:443/v1/vulnerabilities/assets',
        json=[
            {
                'cveId': 'CVE-2017-14463',
                'assetCount': 1
            }, {
                'cveId': 'CVE-2017-14472',
                'assetCount': 1
            }
        ]
    )
    counts = fixture_ot.vulns.assets_list()
    for count in counts:
        assert count.cveId
        assert count.assetCount
