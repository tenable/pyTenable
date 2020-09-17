from tenable.ot.schemas.iterators import OTIterator
from tenable.ot.vulns import VulnAssetIntermixer
from box import Box
import pytest, responses, re


def load_responses(responses):
    '''
    A centralized location for these larger responses to be used in this testing
    module
    '''
    responses.add(
        method='GET',
        url='https://localhost:443/v1/vulnerabilities',
        json=[{
            'cve': {
                'CVE_data_meta': {
                    'ID': 'CVE-2020-9464'
                },
                'references': {
                    'reference_data': [
                        {
                            'url': 'https://cert.vde.com/en-us/advisories/vde-2020-005',
                            'name': 'https://cert.vde.com/en-us/advisories/vde-2020-005',
                            'refsource': 'MISC'
                        }
                    ]
                },
                'description': {
                    'description_data': [
                        {
                            'lang': 'en',
                            'value': 'description_data'
                        }
                    ]
                }
            },
            'impact': {
                'baseMetricV2': {
                    'cvssV2': {
                        'baseScore': 7.8,
                        'accessVector': 'NETWORK',
                        'accessComplexity': 'LOW',
                        'authentication': 'NONE',
                        'confidentialityImpact': 'NONE',
                        'integrityImpact': 'NONE',
                        'availabilityImpact': 'COMPLETE'
                    }
                }
            },
            'configurations': {
                'nodes': [
                    {
                        'operator': 'AND',
                        'children': [
                            {
                                'operator': 'OR',
                                'cpe_match': [
                                    {
                                        'vulnerable': True,
                                        'cpe23Uri': 'cpe:2.3:o:beckhoff:bk9000_firmware:*:*:*:*:*:*:*:*',
                                        'family': 'Beckhoff'
                                    }
                                ]
                            }, {
                                'operator': 'OR',
                                'cpe_match': [
                                    {
                                        'vulnerable': False,
                                        'cpe23Uri': 'cpe:2.3:h:beckhoff:bk9000:-:*:*:*:*:*:*:*',
                                        'family': 'Beckhoff'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            'publishedDate': '2020-03-12T14:15Z',
            'lastModifiedDate': '2020-03-16T16:43Z',
            'comment': ''
        }]
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
def test_vuln_asset_intermixer(ot):
    '''
    Tests the intermixer iterator
    '''
    load_responses(responses)
    vulns = ot.vulns.extract()

    # assert the iterator returns itself.
    assert vulns == vulns.__iter__()

    # as __next__() calls next(), we will use the internal method to clear the
    # testing requirements.
    v = vulns.__next__()

    assert v.asset.id == '8fe5cdb1-723e-4996-9d3c-7787445bc38a'
    assert v.asset.connections
    assert v.asset.connections[0].networkInterface.id == 'd7f06b04-5733-44ac-9e84-096f6fdb181b'
    assert v.impact.baseMetricV2.cvssV2.baseScore == 7.8

    # Validate that merge_cache should always return the same asset cache.
    w = vulns._merge_cache(Box({'id': '8fe5cdb1-723e-4996-9d3c-7787445bc38a'}))
    assert v.asset.id == w.asset.id
    assert v.cve.id == w.cve.id

    # test that the stop iterator works as expected.
    with pytest.raises(StopIteration):
        vulns.next()


@responses.activate
def test_list(ot):
    '''
    Tests the list method
    '''
    load_responses(responses)
    vulns = ot.vulns.list()

    for vuln in vulns:
        assert vuln.cve.CVE_data_meta.ID == 'CVE-2020-9464'
        assert vuln.impact.baseMetricV2.cvssV2.baseScore == 7.8


@responses.activate
def test_assets_list(ot):
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
    counts = ot.vulns.assets_list()
    for c in counts:
        assert c.cveId
        assert c.assetCount