"""
test file for testing various scenarios in analysis
"""

import pytest
import responses

from tenable.errors import UnexpectedValueError
from tenable.sc.analysis import AnalysisResultsIterator
from ..checker import check


def test_analysis_constructor_type_error(tsc):
    """
    test analysis constructor for type error
    """
    with pytest.raises(TypeError):
        getattr(tsc.analysis, '_analysis')(
            tool=1, type='type', sort_field='field', sort_direction=1
        )

    with pytest.raises(TypeError):
        getattr(tsc.analysis, '_analysis')(
            tool=1,
            type='type',
            sort_field='field',
            sort_direction='ASC',
            offset=0,
            limit='limit',
        )


def test_analysis_constructor_success(tsc):
    """
    test analysis constructor for success
    """
    analysis = getattr(tsc.analysis, '_analysis')(
        tool=1,
        type='type',
        sort_field='field',
        sort_direction='ASC',
        offset=0,
        payload={'sourceType': 'individual'},
    )
    assert isinstance(analysis, AnalysisResultsIterator)


def test_analysis_asset_expansion_simple(tsc):
    """
    test analysis asset expansion simple for success
    """
    resp = getattr(tsc.analysis, '_combo_expansion')(('or', 1, 2))
    assert resp == {
        'operator': 'union',
        'operand1': {'id': '1'},
        'operand2': {'id': '2'},
    }


def test_analysis_asset_expansion_complex(tsc):
    """
    test analysis asset expansion complex for success
    """
    resp = getattr(tsc.analysis, '_combo_expansion')(
        ('or', ('and', 1, 2), ('not', ('or', 3, 4)))
    )
    assert resp == {
        'operator': 'union',
        'operand1': {
            'operator': 'intersection',
            'operand1': {'id': '1'},
            'operand2': {'id': '2'},
        },
        'operand2': {
            'operator': 'complement',
            'operand1': {
                'operator': 'union',
                'operand1': {'id': '3'},
                'operand2': {'id': '4'},
            },
        },
    }


def test_analysis_query_constructor_simple(tsc):
    """
    test analysis query constructor simple for success
    """
    resp = getattr(tsc.analysis, '_query_constructor')(
        ('filter1', 'operator1', 'value1'),
        ('filter2', 'operator2', 'value2'),
        tool='tool_test',
        type='type_test',
    )
    assert resp == {
        'tool': 'tool_test',
        'query': {
            'tool': 'tool_test',
            'type': 'type_test',
            'filters': [
                {
                    'filterName': 'filter1',
                    'operator': 'operator1',
                    'value': 'value1',
                },
                {'filterName': 'filter2', 'operator': 'operator2', 'value': 'value2'},
            ],
        },
    }


def test_analysis_query_constructor_replace(tsc):
    """
    test analysis query constructor replace for success
    """
    resp = getattr(tsc.analysis, '_query_constructor')(
        ('filter1', 'operator1', 'badvalue'),
        ('filter1', 'operator1', 'value1'),
        ('filter2', 'operator2', 'value2'),
        tool='tool_test',
        type='type_test',
    )
    assert resp == {
        'tool': 'tool_test',
        'query': {
            'tool': 'tool_test',
            'type': 'type_test',
            'filters': [
                {
                    'filterName': 'filter1',
                    'operator': 'operator1',
                    'value': 'value1',
                },
                {'filterName': 'filter2', 'operator': 'operator2', 'value': 'value2'},
            ],
        },
    }


def test_analysis_query_constructor_remove(tsc):
    """
    test analysis query constructor remove for success
    """
    resp = getattr(tsc.analysis, '_query_constructor')(
        ('filter3', 'operator1', 'badvalue'),
        ('filter1', 'operator1', 'value1'),
        ('filter2', 'operator2', 'value2'),
        ('filter3', None, None),
        tool='tool_test',
        type='type_test',
    )
    assert resp == {
        'tool': 'tool_test',
        'query': {
            'tool': 'tool_test',
            'type': 'type_test',
            'filters': [
                {
                    'filterName': 'filter1',
                    'operator': 'operator1',
                    'value': 'value1',
                },
                {'filterName': 'filter2', 'operator': 'operator2', 'value': 'value2'},
            ],
        },
    }


def test_analysis_query_constructor_asset(tsc):
    """
    test analysis query constructor asset for success
    """
    resp = getattr(tsc.analysis, '_query_constructor')(
        ('asset', '~', ('or', 1, 2)), tool='tool', type='type'
    )
    assert resp == {
        'tool': 'tool',
        'query': {
            'tool': 'tool',
            'type': 'type',
            'filters': [
                {
                    'filterName': 'asset',
                    'operator': '~',
                    'value': {
                        'operator': 'union',
                        'operand1': {'id': '1'},
                        'operand2': {'id': '2'},
                    },
                }
            ],
        },
    }


def test_analysis_vulns(tsc):
    """
    test analysis vulnerabilities for success
    """
    vulns = tsc.analysis.vulns(source='cumulative', scan_id=1)
    assert isinstance(vulns, AnalysisResultsIterator)


def test_analysis_scan(tsc):
    """
    test analysis scan for success
    """
    scan = tsc.analysis.scan(1)
    assert isinstance(scan, AnalysisResultsIterator)


def test_analysis_events(tsc):
    """
    test analysis events for success
    """
    event = tsc.analysis.events(source='archive', silo_id='silo_id')
    assert isinstance(event, AnalysisResultsIterator)


def test_analysis_events_unexpected_value_error(tsc):
    """
    test analysis events for unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.analysis.events(source='archive')


@responses.activate
def test_analysis_vulns_cceipdetail_tool(tsc):
    """
    test analysis vulnerabilities cceip detail tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '0',
                'returnedRecords': 0,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629',
                'results': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080186,
        },
    )
    vulns = tsc.analysis.vulns(tool='cceipdetail', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@responses.activate
def test_analysis_vulns_cveipdetail_tool(tsc):
    """
    test analysis vulnerabilities cveip detail tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '689',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '689',
                'results': [
                    {
                        'cveID': 'CVE-1999-0524',
                        'total': '22',
                        'hosts': [
                            {
                                'repositoryID': '1',
                                'iplist': [
                                    {
                                        'ip': '192.168.100.1',
                                        'uuid': '',
                                        'macAddress': '',
                                        'netbiosName': '',
                                        'dnsName': 'pfsense.home.cugnet.net',
                                    },
                                    {
                                        'ip': '192.168.100.5',
                                        'uuid': '',
                                        'macAddress': '',
                                        'netbiosName': '',
                                        'dnsName': 'switch.home.cugnet.net',
                                    },
                                ],
                            }
                        ],
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080186,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '689',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '689',
                'results': [
                    {
                        'cveID': 'CVE-2014-3566',
                        'total': '3',
                        'hosts': [
                            {
                                'repositoryID': '1',
                                'iplist': [
                                    {
                                        'ip': '192.168.100.5',
                                        'uuid': '',
                                        'macAddress': '',
                                        'netbiosName': '',
                                        'dnsName': 'switch.home.cugnet.net',
                                    },
                                    {
                                        'ip': '192.168.100.10',
                                        'uuid': '',
                                        'macAddress': '',
                                        'netbiosName': '',
                                        'dnsName': 'wap.home.cugnet.net',
                                    },
                                ],
                            }
                        ],
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080188,
        },
    )
    vulns = tsc.analysis.vulns(tool='cveipdetail', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'cveID', str)
        check(vuln, 'total', str)
        check(vuln, 'hosts', list)
        host = vuln['hosts'][0]
        check(host, 'iplist', list)
        check(host, 'repositoryID', str)
        for ip_address in host['iplist']:
            check(ip_address, 'ip', str)
            check(ip_address, 'netbiosName', str)
            check(ip_address, 'dnsName', str)
            check(ip_address, 'uuid', str)
            check(ip_address, 'macAddress', str)


@responses.activate
def test_analysis_vulns_iavmipdetail_tool(tsc):
    """
    test analysis vulnerabilities iavmip detail tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '15',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '15',
                'results': [
                    {
                        'iavmID': '2017-A-0165',
                        'total': '2',
                        'hosts': [
                            {
                                'repositoryID': '1',
                                'iplist': [
                                    {
                                        'ip': '192.168.101.130',
                                        'uuid': 'eb6c151b-166f-44ee-8e40-4db763d3a43d',
                                        'macAddress': '00:0c:29:99:4f:e9',
                                        'netbiosName': 'UNKNOWN\\torrents.home.cugnet.net',
                                        'dnsName': 'torrents.home.cugnet.net',
                                    }
                                ],
                            }
                        ],
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080190,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '15',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '15',
                'results': [
                    {
                        'iavmID': '2018-A-0019',
                        'total': '2',
                        'hosts': [
                            {
                                'repositoryID': '1',
                                'iplist': [
                                    {
                                        'ip': '192.168.101.130',
                                        'uuid': 'eb6c151b-166f-44ee-8e40-4db763d3a43d',
                                        'macAddress': '00:0c:29:99:4f:e9',
                                        'netbiosName': 'UNKNOWN\\torrents.home.cugnet.net',
                                        'dnsName': 'torrents.home.cugnet.net',
                                    }
                                ],
                            }
                        ],
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080192,
        },
    )
    vulns = tsc.analysis.vulns(tool='iavmipdetail', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'iavmID', str)
        check(vuln, 'total', str)
        check(vuln, 'hosts', list)
        host = vuln['hosts'][0]
        check(host, 'iplist', list)
        check(host, 'repositoryID', str)
        for ip_address in host['iplist']:
            check(ip_address, 'ip', str)
            check(ip_address, 'netbiosName', str)
            check(ip_address, 'dnsName', str)
            check(ip_address, 'uuid', str)
            check(ip_address, 'macAddress', str)


@responses.activate
def test_analysis_vulns_iplist_tool(tsc):
    """test to get the iplist"""
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                '0': '192.168.100.1',
                '1': '192.168.100.3-192.168.100.5',
                '2': '192.168.100.10',
                '3': '192.168.100.114',
                '4': '192.168.101.1',
                '5': '192.168.101.30',
                '6': '192.168.101.115',
                '7': '192.168.101.117',
                '8': '192.168.101.130',
                '9': '192.168.101.133',
                '10': '192.168.101.140',
                '11': '192.168.101.146',
                '12': '192.168.101.177-192.168.101.179',
                '13': '192.168.101.189',
                '14': '192.168.101.191',
                '15': '192.168.102.1',
                '16': '192.168.104.106',
                '17': '192.168.104.109',
                '18': '192.168.104.114-192.168.104.115',
                '19': '192.168.104.123-192.168.104.124',
                '20': '192.168.104.126-192.168.104.127',
                'results': None,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080193,
        },
    )
    vulns = getattr(tsc.analysis, 'vulns')(tool='iplist', pages=2, limit=5)
    assert isinstance(vulns, dict)
    for vuln in vulns:
        check(vulns, vuln, str)


@responses.activate
def test_analysis_vulns_listmailclients_tool(tsc):
    """
    test analysis vulnerabilities list mail clients tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '0',
                'returnedRecords': 0,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '0',
                'results': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080194,
        },
    )
    vulns = tsc.analysis.vulns(tool='listmailclients', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_listservices_tool(tsc):
    """
    test analysis vulnerabilities list services tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '47',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '158',
                'results': [
                    {
                        'count': '23',
                        'detectionMethod': 'Active',
                        'name': 'A web server is running on this port.',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080194,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '47',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '158',
                'results': [
                    {
                        'count': '6',
                        'detectionMethod': 'Active',
                        'name': 'Process ID   : 1088\n  Executable   : /usr/bin/transmission-daemon\n  Command line : /usr/bin/transmission-daemon -f --log-error',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080195,
        },
    )
    vulns = tsc.analysis.vulns(tool='listservices', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_listos_tool(tsc):
    """
    test analysis vulnerabilities list os tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '18',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '29',
                'results': [
                    {
                        'count': '3',
                        'detectionMethod': 'Active',
                        'name': 'FreeBSD 11.1-RELEASE-p10 (amd64)',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080195,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '18',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '29',
                'results': [
                    {
                        'count': '2',
                        'detectionMethod': 'Active',
                        'name': 'Linux Kernel 3.10.0-862.3.3.el7.x86_64 on CentOS Linux release 7.6.1810 (Core)',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080195,
        },
    )
    vulns = tsc.analysis.vulns(tool='listos', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_listsoftware_tool(tsc):
    """
    test analysis vulnerabilities list software tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '1286',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '5323',
                'results': [
                    {
                        'count': '13',
                        'detectionMethod': 'Active',
                        'name': 'aic94xx-firmware-30-6.el7|(none)',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080196,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '1286',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '5323',
                'results': [
                    {
                        'count': '13',
                        'detectionMethod': 'Active',
                        'name': 'centos-logos-70.0.6-3.el7.centos|(none)',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080196,
        },
    )
    vulns = tsc.analysis.vulns(tool='listsoftware', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_listsshservers_tool(tsc):
    """
    test analysis vulnerabilities list ssh servers tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '5',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '14',
                'results': [
                    {
                        'count': '10',
                        'detectionMethod': 'Active',
                        'name': 'SSH-2.0-OpenSSH_7.4',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080197,
        },
    )
    vulns = tsc.analysis.vulns(tool='listsshservers', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_listvuln_tool(tsc):
    """
    test analysis vulnerabilities list vulnerability tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '1629',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '-1',
                'results': [
                    {
                        'pluginID': '10107',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'ip': '192.168.100.1',
                        'uuid': '',
                        'port': '80',
                        'protocol': 'TCP',
                        'name': 'HTTP Server Type and Version',
                        'dnsName': 'pfsense.home.cugnet.net',
                        'macAddress': '',
                        'netbiosName': '',
                        'uniqueness': 'repositoryID,ip,dnsName',
                        'family': {'id': '11', 'name': 'Web Servers', 'type': 'active'},
                        'repository': {
                            'id': '1',
                            'name': 'Default',
                            'description': '',
                            'dataFormat': 'IPv4',
                        },
                        'pluginInfo': '10107 (80/6) HTTP Server Type and Version',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080197,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '1629',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '-1',
                'results': [
                    {
                        'pluginID': '10863',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'ip': '192.168.100.1',
                        'uuid': '',
                        'port': '443',
                        'protocol': 'TCP',
                        'name': 'SSL Certificate Information',
                        'dnsName': 'pfsense.home.cugnet.net',
                        'macAddress': '',
                        'netbiosName': '',
                        'uniqueness': 'repositoryID,ip,dnsName',
                        'family': {'id': '30', 'name': 'General', 'type': 'active'},
                        'repository': {
                            'id': '1',
                            'name': 'Default',
                            'description': '',
                            'dataFormat': 'IPv4',
                        },
                        'pluginInfo': '10863 (443/6) SSL Certificate Information',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080198,
        },
    )
    vulns = tsc.analysis.vulns(tool='listvuln', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'macAddress', str)
        check(vuln, 'uniqueness', str)
        check(vuln, 'protocol', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'family', dict)
        check(vuln['family'], 'type', str)
        check(vuln['family'], 'id', str)
        check(vuln['family'], 'name', str)
        check(vuln, 'pluginInfo', str)
        check(vuln, 'ip', str)
        check(vuln, 'netbiosName', str)
        check(vuln, 'name', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'dataFormat', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'dnsName', str)
        check(vuln, 'port', str)
        check(vuln, 'uuid', str)


@responses.activate
def test_analysis_vulns_listwebclients_tool(tsc):
    """
    test analysis vulnerabilities list web clients tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '0',
                'returnedRecords': 0,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '0',
                'results': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080198,
        },
    )
    vulns = tsc.analysis.vulns(tool='listwebclients', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_listwebservers_tool(tsc):
    """
    test analysis vulnerabilities list web servers tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '14',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '26',
                'results': [
                    {'count': '9', 'detectionMethod': 'Active', 'name': 'nginx'}
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080199,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '14',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '26',
                'results': [
                    {'count': '1', 'detectionMethod': 'Active', 'name': 'Apache'}
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080199,
        },
    )
    vulns = tsc.analysis.vulns(tool='listwebservers', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_sumasset_tool(tsc):
    """
    test analysis vulnerabilities sum asset tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '34',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '5600:69:584:686:122:4139:10780',
                'results': [
                    {
                        'score': '0',
                        'total': '0',
                        'severityInfo': '0',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                        'asset': {
                            'id': '1',
                            'name': 'Systems Discovered Passively',
                            'description': 'This asset uses passive plugins for OS detection and hop detection to identify hosts on the network.',
                            'type': 'dynamic',
                            'status': '0',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080200,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '34',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '5600:69:584:686:122:4139:10780',
                'results': [
                    {
                        'score': '0',
                        'total': '0',
                        'severityInfo': '0',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                        'asset': {
                            'id': '11',
                            'name': 'Sniffed Hosts Not in DNS',
                            'description': "Leverage PVS plugin 12 (Host TTL discovered) and Nessus plugin 12503 (Host Fully Qualified Domain Name (FQDN) Resolution) to find hosts that don't have a resolvable FQDN in DNS.",
                            'type': 'dynamic',
                            'status': '0',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080200,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumasset', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'total', str)
        check(vuln, 'score', str)
        check(vuln, 'asset', dict)
        check(vuln['asset'], 'status', str)
        check(vuln['asset'], 'description', str)
        check(vuln['asset'], 'type', str)
        check(vuln['asset'], 'id', str)
        check(vuln['asset'], 'name', str)


@responses.activate
def test_analysis_vulns_sumcce_tool(tsc):
    """
    test analysis vulnerabilities sum cce tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '0',
                'returnedRecords': 0,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:0:0:0:0:0:0:0',
                'results': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080201,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumcce', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@responses.activate
def test_analysis_vulns_sumclassa_tool(tsc):
    """
    test analysis vulnerabilities sum class-a tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '2',
                'returnedRecords': 2,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'ip': '192.0.0.0/8',
                        'score': '1528',
                        'total': '475',
                        'severityInfo': '305',
                        'severityLow': '8',
                        'severityMedium': '70',
                        'severityHigh': '79',
                        'severityCritical': '13',
                        'repository': {
                            'id': '2',
                            'name': 'Agents',
                            'description': '',
                            'dataFormat': 'agent',
                        },
                    }
                ]
                * 2,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080202,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumclassa', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'total', str)
        check(vuln, 'score', str)
        check(vuln, 'ip', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'dataFormat', str)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)


@responses.activate
def test_analysis_vulns_sumclassb_tool(tsc):
    """
    test analysis vulnerabilities sum class-b tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '2',
                'returnedRecords': 2,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'ip': '192.168.0.0/16',
                        'score': '1528',
                        'total': '475',
                        'severityInfo': '305',
                        'severityLow': '8',
                        'severityMedium': '70',
                        'severityHigh': '79',
                        'severityCritical': '13',
                        'repository': {
                            'id': '2',
                            'name': 'Agents',
                            'description': '',
                            'dataFormat': 'agent',
                        },
                    }
                ]
                * 2,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080203,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumclassb', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'total', str)
        check(vuln, 'score', str)
        check(vuln, 'ip', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'dataFormat', str)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)


@responses.activate
def test_analysis_vulns_sumclassc_tool(tsc):
    """
    test analysis vulnerabilities sum class-c tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '7',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'ip': '192.168.100.0/24',
                        'score': '617',
                        'total': '179',
                        'severityInfo': '144',
                        'severityLow': '0',
                        'severityMedium': '9',
                        'severityHigh': '15',
                        'severityCritical': '11',
                        'repository': {
                            'id': '2',
                            'name': 'Agents',
                            'description': '',
                            'dataFormat': 'agent',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080203,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '7',
                'returnedRecords': 2,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'ip': '192.168.102.0/24',
                        'score': '49',
                        'total': '38',
                        'severityInfo': '34',
                        'severityLow': '0',
                        'severityMedium': '3',
                        'severityHigh': '0',
                        'severityCritical': '1',
                        'repository': {
                            'id': '1',
                            'name': 'Default',
                            'description': '',
                            'dataFormat': 'IPv4',
                        },
                    }
                ]
                * 2,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080204,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumclassc', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'total', str)
        check(vuln, 'score', str)
        check(vuln, 'ip', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'dataFormat', str)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)


@responses.activate
def test_analysis_vulns_sumcve_tool(tsc):
    """
    test analysis vulnerabilities sum cve detail tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '689',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1356:0:0:0:0:0:0:1330',
                'results': [
                    {
                        'cveID': 'CVE-1999-0524',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'total': '22',
                        'hostTotal': '22',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080204,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '689',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1356:0:0:0:0:0:0:1330',
                'results': [
                    {
                        'cveID': 'CVE-2016-2183',
                        'severity': {
                            'id': '3',
                            'name': 'High',
                            'description': 'High Severity',
                        },
                        'total': '5',
                        'hostTotal': '5',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080206,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumcve', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'cveID', str)
        check(vuln, 'total', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'hostTotal', str)


@responses.activate
def test_analysis_vulns_sumdnsname_tool(tsc):
    """
    test analysis vulnerabilities sum dns name tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '24',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1467:17:146:172:31:1101:2687',
                'results': [
                    {
                        'dnsName': 'freelancer',
                        'score': '617',
                        'total': '179',
                        'severityInfo': '144',
                        'severityLow': '0',
                        'severityMedium': '9',
                        'severityHigh': '15',
                        'severityCritical': '11',
                        'repository': {
                            'id': '2',
                            'name': 'Agents',
                            'description': '',
                            'dataFormat': 'agent',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080208,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '24',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1467:17:146:172:31:1101:2687',
                'results': [
                    {
                        'dnsName': 'herfio.home.cugnet.net',
                        'score': '257',
                        'total': '77',
                        'severityInfo': '33',
                        'severityLow': '4',
                        'severityMedium': '21',
                        'severityHigh': '19',
                        'severityCritical': '0',
                        'repository': {
                            'id': '2',
                            'name': 'Agents',
                            'description': '',
                            'dataFormat': 'agent',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080209,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumdnsname', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'dnsName', str)
        check(vuln, 'score', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'dataFormat', str)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)


@responses.activate
def test_analysis_vulns_sumfamily_tool(tsc):
    """
    test analysis vulnerabilities sum family tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '16',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'score': '0',
                        'total': '1',
                        'severityInfo': '1',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                        'family': {'id': '19', 'name': 'FTP', 'type': 'active'},
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080209,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '16',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'score': '0',
                        'total': '7',
                        'severityInfo': '7',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                        'family': {'id': '6', 'name': 'CGI abuses', 'type': 'active'},
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080210,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumfamily', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'family', dict)
        check(vuln['family'], 'type', str)
        check(vuln['family'], 'id', str)
        check(vuln['family'], 'name', str)
        check(vuln, 'score', str)
        check(vuln, 'total', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)


@responses.activate
def test_analysis_vulns_sumiavm_tool(tsc):
    """
    test analysis vulnerabilities sum iavm tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '15',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '42:0:0:0:0:0:0:28',
                'results': [
                    {
                        'iavmID': '2018-A-0020',
                        'severity': {
                            'id': '3',
                            'name': 'High',
                            'description': 'High Severity',
                        },
                        'total': '12',
                        'hostTotal': '2',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080211,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '15',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '42:0:0:0:0:0:0:28',
                'results': [
                    {
                        'iavmID': '2017-A-0165',
                        'severity': {
                            'id': '2',
                            'name': 'Medium',
                            'description': 'Medium Severity',
                        },
                        'total': '2',
                        'hostTotal': '2',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080213,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumiavm', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'iavmID', str)
        check(vuln, 'total', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'hostTotal', str)


@responses.activate
def test_analysis_vulns_sumid_tool(tsc):
    """
    test analysis vulnerabilities sum id tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '358',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780:1287',
                'results': [
                    {
                        'pluginID': '10092',
                        'total': '1',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'name': 'FTP Server Detection',
                        'hostTotal': '1',
                        'family': {
                            'id': '24',
                            'name': 'Service detection',
                            'type': 'active',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080215,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '358',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780:1287',
                'results': [
                    {
                        'pluginID': '10267',
                        'total': '14',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'name': 'SSH Server Type and Version Information',
                        'hostTotal': '14',
                        'family': {
                            'id': '24',
                            'name': 'Service detection',
                            'type': 'active',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080215,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumid', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'family', dict)
        check(vuln['family'], 'type', str)
        check(vuln['family'], 'id', str)
        check(vuln['family'], 'name', str)
        check(vuln, 'hostTotal', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'total', str)
        check(vuln, 'name', str)


@responses.activate
def test_analysis_vulns_sumip_tool(tsc):
    """
    test analysis vulnerabilities sum ip tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '33',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'ip': '192.168.100.1',
                        'uuid': '',
                        'score': '49',
                        'total': '43',
                        'severityInfo': '39',
                        'severityLow': '0',
                        'severityMedium': '3',
                        'severityHigh': '0',
                        'severityCritical': '1',
                        'macAddress': '',
                        'policyName': '3ae050e2-486c-5c1a-a6a5-45305557cec3-621/Full Safe Scan',
                        'pluginSet': '201812150336',
                        'netbiosName': '',
                        'dnsName': 'pfsense.home.cugnet.net',
                        'osCPE': 'cpe:/o:freebsd:freebsd:11.1',
                        'biosGUID': '',
                        'tpmID': '',
                        'mcafeeGUID': '',
                        'lastAuthRun': '',
                        'lastUnauthRun': '1545071370',
                        'uniqueness': 'repositoryID,ip,dnsName',
                        'repository': {
                            'id': '1',
                            'name': 'Default',
                            'description': '',
                            'dataFormat': 'IPv4',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080216,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '33',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'ip': '192.168.100.114',
                        'uuid': 'c2d9e0b8-d88e-46ed-b7f4-86062e3ab42b',
                        'score': '617',
                        'total': '179',
                        'severityInfo': '144',
                        'severityLow': '0',
                        'severityMedium': '9',
                        'severityHigh': '15',
                        'severityCritical': '11',
                        'macAddress': '62:45:b4:ed:2f:1c',
                        'policyName': 'Basic Agent Scan',
                        'pluginSet': '201812150336',
                        'netbiosName': 'UNKNOWN\\FREELANCER',
                        'dnsName': 'freelancer',
                        'osCPE': 'cpe:/o:microsoft:windows_10:::x64-home',
                        'biosGUID': '03D40274-0435-058C-D006-4F0700080009',
                        'tpmID': '',
                        'mcafeeGUID': '',
                        'lastAuthRun': '1545066276',
                        'lastUnauthRun': '',
                        'uniqueness': 'repositoryID,uuid',
                        'repository': {
                            'id': '2',
                            'name': 'Agents',
                            'description': '',
                            'dataFormat': 'agent',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080216,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumip', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'macAddress', str)
        check(vuln, 'lastAuthRun', str)
        check(vuln, 'ip', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'total', str)
        check(vuln, 'mcafeeGUID', str)
        check(vuln, 'policyName', str)
        check(vuln, 'uuid', str)
        check(vuln, 'osCPE', str)
        check(vuln, 'uniqueness', str)
        check(vuln, 'score', str)
        check(vuln, 'dnsName', str)
        check(vuln, 'lastUnauthRun', str)
        check(vuln, 'biosGUID', str)
        check(vuln, 'tpmID', str)
        check(vuln, 'pluginSet', str)
        check(vuln, 'netbiosName', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'dataFormat', str)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)


@responses.activate
def test_analysis_vulns_summsbulletin_tool(tsc):
    """
    test analysis vulnerabilities sum ms bulletin tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '30',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '31:0:0:0:0:0:0:30',
                'results': [
                    {
                        'msbulletinID': 'MS18-4471324',
                        'severity': {
                            'id': '4',
                            'name': 'Critical',
                            'description': 'Critical Severity',
                        },
                        'total': '2',
                        'hostTotal': '1',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080217,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '30',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '31:0:0:0:0:0:0:30',
                'results': [
                    {
                        'msbulletinID': 'MS18-4346087',
                        'severity': {
                            'id': '2',
                            'name': 'Medium',
                            'description': 'Medium Severity',
                        },
                        'total': '1',
                        'hostTotal': '1',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080218,
        },
    )
    vulns = tsc.analysis.vulns(tool='summsbulletin', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'msbulletinID', str)
        check(vuln, 'total', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'hostTotal', str)


@responses.activate
def test_analysis_vulns_sumport_tool(tsc):
    """
    test analysis vulnerabilities sum port tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '103',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'port': '0',
                        'score': '1999',
                        'total': '781',
                        'severityInfo': '503',
                        'severityLow': '17',
                        'severityMedium': '124',
                        'severityHigh': '129',
                        'severityCritical': '8',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080220,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '103',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'port': '53',
                        'score': '3',
                        'total': '14',
                        'severityInfo': '13',
                        'severityLow': '0',
                        'severityMedium': '1',
                        'severityHigh': '0',
                        'severityCritical': '0',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080221,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumport', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'port', str)
        check(vuln, 'score', str)
        check(vuln, 'total', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)


@responses.activate
def test_analysis_vulns_sumprotocol_tool(tsc):
    """
    test analysis vulnerabilities sum protocol tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '3',
                'returnedRecords': 3,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256:2780',
                'results': [
                    {
                        'protocol': 'ICMP(1)',
                        'score': '0',
                        'total': '22',
                        'severityInfo': '22',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                    }
                ]
                * 3,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080221,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumprotocol', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'protocol', str)
        check(vuln, 'score', str)
        check(vuln, 'total', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)


@responses.activate
def test_analysis_vulns_sumremediation_tool(tsc):
    """
    test analysis vulnerabilities sum remediation tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '56',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:0:0:0:0:0:2780:33',
                'results': [
                    {
                        'pluginID': '87892',
                        'cpe': '',
                        'solution': 'Apply MS16-005: Security Update for Windows Kernel-Mode Drivers to Address Remote Code Execution (3124584)',
                        'remediationList': '87892,87890,87881,87878,87877,87264,87262,87261,87257,87254,87253,86828,86826,86825,86822,86820,86819,86818,86373,86367,86366,85845',
                        'total': '1',
                        'totalPctg': '0.06%',
                        'score': '10',
                        'scorePctg': '0.36%',
                        'hostTotal': '1',
                        'msbulletinTotal': '1',
                        'cveTotal': '30',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080222,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '56',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629:0:0:0:0:0:2780:33',
                'results': [
                    {
                        'pluginID': '97305',
                        'cpe': 'p-cpe:/a:centos:centos:openssl-devel,p-cpe:/a:centos:centos:openssl-static,p-cpe:/a:centos:centos:openssl-perl,p-cpe:/a:centos:centos:openssl,p-cpe:/a:centos:centos:openssl-libs',
                        'solution': 'Update the affected openssl packages.',
                        'remediationList': '97305,93777,91171,89059,87781,87357,84199,83994,81997,80867,78516,77187,74334,73387,71865,65061,59294,58852,58502,57731',
                        'total': '2',
                        'totalPctg': '0.12%',
                        'score': '6',
                        'scorePctg': '0.22%',
                        'hostTotal': '2',
                        'msbulletinTotal': '0',
                        'cveTotal': '4',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080226,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumremediation', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'hostTotal', str)
        check(vuln, 'scorePctg', str)
        check(vuln, 'totalPctg', str)
        check(vuln, 'msbulletinTotal', str)
        check(vuln, 'remediationList', str)
        check(vuln, 'cpe', str)
        check(vuln, 'cveTotal', str)
        check(vuln, 'solution', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'score', str)
        check(vuln, 'total', str)


@responses.activate
def test_analysis_vulns_sumseverity_tool(tsc):
    """
    test analysis vulnerabilities sum severity tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '5',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629:19:146:176:32:1256',
                'results': [
                    {
                        'severity': {
                            'id': '4',
                            'name': 'Critical',
                            'description': 'Critical Severity',
                        },
                        'count': '19',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080229,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumseverity', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)


@responses.activate
def test_analysis_vulns_sum_user_responsibility_tool(tsc):
    """
    test analysis vulnerabilities sum user responsibility tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '0',
                'returnedRecords': 0,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '0:0:0:0:0:0:0',
                'results': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080230,
        },
    )
    vulns = tsc.analysis.vulns(tool='sumuserresponsibility', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'score', str)
        check(vuln, 'total', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'userList', list)
        for user in vuln['userList']:
            check(user, 'firstname', str)
            check(user, 'id', str)
            check(user, 'lastname', str)
            check(user, 'status', str)
            check(user, 'username', str)


@responses.activate
def test_analysis_vulns_trend_tool(tsc):
    """
    test analysis vulnerabilities trend tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': -1,
                'returnedRecords': -1,
                'startOffset': '0',
                'endOffset': '-1',
                'matchingDataElementCount': '0:0:0:0:0:0',
                'results': [
                    {
                        'date': -86400,
                        'score': '0',
                        'total': 0,
                        'severityInfo': '0',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                        'dbSource': 'unavailable',
                        'lastresults': '2^5^0^5^0:0:0:0:0:0^0^0@unavailable\nseverity\ncount\n4\n0\n3\n0\n2\n0\n1\n0\n0\n0',
                    }
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080231,
        },
    )
    vulns = tsc.analysis.vulns(tool='trend', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@responses.activate
def test_analysis_vulns_vulndetails_tool(tsc):
    """
    test analysis vulnerabilities 'vulnerability details' tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '1629',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '-1',
                'results': [
                    {
                        'pluginID': '10107',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'hasBeenMitigated': '0',
                        'acceptRisk': '0',
                        'recastRisk': '0',
                        'ip': '192.168.100.1',
                        'uuid': '',
                        'port': '80',
                        'protocol': 'TCP',
                        'pluginName': 'HTTP Server Type and Version',
                        'firstSeen': '1545074182',
                        'lastSeen': '1545074182',
                        'exploitAvailable': 'No',
                        'exploitEase': '',
                        'exploitFrameworks': '',
                        'synopsis': 'A web server is running on the remote host.',
                        'description': 'This plugin attempts to determine the type and the version of the   remote web server.',
                        'solution': 'n/a',
                        'seeAlso': '',
                        'riskFactor': 'None',
                        'stigSeverity': '',
                        'baseScore': '',
                        'temporalScore': '',
                        'cvssVector': '',
                        'cvssV3BaseScore': '',
                        'cvssV3TemporalScore': '',
                        'cvssV3Vector': '',
                        'cpe': '',
                        'vulnPubDate': '-1',
                        'patchPubDate': '-1',
                        'pluginPubDate': '947005200',
                        'pluginModDate': '1544806800',
                        'checkType': 'remote',
                        'version': '1.133',
                        'cve': '',
                        'bid': '',
                        'xref': '',
                        'pluginText': '<plugin_output>The remote web server type is :\n\nnginx</plugin_output>',
                        'dnsName': 'pfsense.home.cugnet.net',
                        'macAddress': '',
                        'netbiosName': '',
                        'uniqueness': 'repositoryID,ip,dnsName',
                        'family': {'id': '11', 'name': 'Web Servers', 'type': 'active'},
                        'repository': {
                            'id': '1',
                            'name': 'Default',
                            'description': '',
                            'dataFormat': 'IPv4',
                        },
                        'pluginInfo': '10107 (80/6) HTTP Server Type and Version',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080231,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '1629',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '-1',
                'results': [
                    {
                        'pluginID': '10863',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'hasBeenMitigated': '0',
                        'acceptRisk': '0',
                        'recastRisk': '0',
                        'ip': '192.168.100.1',
                        'uuid': '',
                        'port': '443',
                        'protocol': 'TCP',
                        'pluginName': 'SSL Certificate Information',
                        'firstSeen': '1545074182',
                        'lastSeen': '1545074182',
                        'exploitAvailable': 'No',
                        'exploitEase': '',
                        'exploitFrameworks': '',
                        'synopsis': 'This plugin displays the SSL certificate.',
                        'description': 'This plugin connects to every SSL-related port and attempts to extract and dump the X.509 certificate.',
                        'solution': 'n/a',
                        'seeAlso': '',
                        'riskFactor': 'None',
                        'stigSeverity': '',
                        'baseScore': '',
                        'temporalScore': '',
                        'cvssVector': '',
                        'cvssV3BaseScore': '',
                        'cvssV3TemporalScore': '',
                        'cvssV3Vector': '',
                        'cpe': '',
                        'vulnPubDate': '-1',
                        'patchPubDate': '-1',
                        'pluginPubDate': '1211212800',
                        'pluginModDate': '1451494800',
                        'checkType': 'remote',
                        'version': 'Revision: 1.16',
                        'cve': '',
                        'bid': '',
                        'xref': '',
                        'pluginText': '<plugin_output>Subject Name: \n\nCountry: US\nState/Province: State\nLocality: Locality\nOrganization: pfSense webConfigurato',
                        'dnsName': 'pfsense.home.cugnet.net',
                        'macAddress': '',
                        'netbiosName': '',
                        'uniqueness': 'repositoryID,ip,dnsName',
                        'family': {'id': '30', 'name': 'General', 'type': 'active'},
                        'repository': {
                            'id': '1',
                            'name': 'Default',
                            'description': '',
                            'dataFormat': 'IPv4',
                        },
                        'pluginInfo': '10863 (443/6) SSL Certificate Information',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080232,
        },
    )
    vulns = tsc.analysis.vulns(tool='vulndetails', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'acceptRisk', str)
        check(vuln, 'baseScore', str)
        check(vuln, 'bid', str)
        check(vuln, 'checkType', str)
        check(vuln, 'cpe', str)
        check(vuln, 'cve', str)
        check(vuln, 'cvssV3BaseScore', str)
        check(vuln, 'cvssV3TemporalScore', str)
        check(vuln, 'cvssV3Vector', str)
        check(vuln, 'cvssVector', str)
        check(vuln, 'description', str)
        check(vuln, 'dnsName', str)
        check(vuln, 'exploitAvailable', str)
        check(vuln, 'exploitEase', str)
        check(vuln, 'exploitFrameworks', str)
        check(vuln, 'family', dict)
        check(vuln['family'], 'type', str)
        check(vuln['family'], 'id', str)
        check(vuln['family'], 'name', str)
        check(vuln, 'firstSeen', str)
        check(vuln, 'hasBeenMitigated', str)
        check(vuln, 'ip', str)
        check(vuln, 'lastSeen', str)
        check(vuln, 'macAddress', str)
        check(vuln, 'netbiosName', str)
        check(vuln, 'patchPubDate', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'pluginInfo', str)
        check(vuln, 'pluginModDate', str)
        check(vuln, 'pluginName', str)
        check(vuln, 'pluginPubDate', str)
        check(vuln, 'pluginText', str)
        check(vuln, 'port', str)
        check(vuln, 'protocol', str)
        check(vuln, 'recastRisk', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'dataFormat', str)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)
        check(vuln, 'riskFactor', str)
        check(vuln, 'seeAlso', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'solution', str)
        check(vuln, 'stigSeverity', str)
        check(vuln, 'synopsis', str)
        check(vuln, 'temporalScore', str)
        check(vuln, 'uniqueness', str)
        check(vuln, 'uuid', str)
        check(vuln, 'version', str)
        check(vuln, 'vulnPubDate', str)
        check(vuln, 'xref', str)


@responses.activate
def test_analysis_vulns_vulnipdetail_tool(tsc):
    """
    test analysis vulnerabilities 'vulnerability ip detail' tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '358',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629',
                'results': [
                    {
                        'pluginID': '10092',
                        'total': '1',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'name': 'FTP Server Detection',
                        'pluginDescription': 'It is possible to obtain the banner of the remote FTP server by connecting to a remote port.',
                        'hosts': [
                            {
                                'iplist': [
                                    {
                                        'ip': '192.168.101.30',
                                        'uuid': '',
                                        'macAddress': '00:11:32:63:a1:cf',
                                        'netbiosName': 'WORKGROUP\\DISKSTATION',
                                        'dnsName': 'diskstation.home.cugnet.net',
                                    }
                                ],
                                'repository': {
                                    'id': '1',
                                    'name': 'Default',
                                    'description': '',
                                    'dataFormat': 'IPv4',
                                },
                            }
                        ],
                        'family': {
                            'id': '24',
                            'name': 'Service detection',
                            'type': 'active',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080232,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '358',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629',
                'results': [
                    {
                        'pluginID': '10267',
                        'total': '14',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'name': 'SSH Server Type and Version Information',
                        'pluginDescription': 'It is possible to obtain information about the remote SSH server by sending an empty authentication request.',
                        'hosts': [
                            {
                                'iplist': [
                                    {
                                        'ip': '192.168.100.5',
                                        'uuid': '',
                                        'macAddress': '',
                                        'netbiosName': '',
                                        'dnsName': 'switch.home.cugnet.net',
                                    },
                                    {
                                        'ip': '192.168.100.10',
                                        'uuid': '',
                                        'macAddress': '',
                                        'netbiosName': '',
                                        'dnsName': 'wap.home.cugnet.net',
                                    },
                                ],
                                'repository': {
                                    'id': '1',
                                    'name': 'Default',
                                    'description': '',
                                    'dataFormat': 'IPv4',
                                },
                            }
                        ],
                        'family': {
                            'id': '24',
                            'name': 'Service detection',
                            'type': 'active',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080233,
        },
    )
    vulns = tsc.analysis.vulns(tool='vulnipdetail', pages=2, limit=5)
    for vuln in vulns:
        check(vuln, 'family', dict)
        check(vuln['family'], 'type', str)
        check(vuln['family'], 'id', str)
        check(vuln['family'], 'name', str)
        check(vuln, 'hosts', list)
        host = vuln['hosts'][0]
        check(host, 'iplist', list)
        check(host, 'repository', dict)
        check(host['repository'], 'dataFormat', str)
        check(host['repository'], 'description', str)
        check(host['repository'], 'id', str)
        check(host['repository'], 'name', str)
        for ip_address in host['iplist']:
            check(ip_address, 'ip', str)
            check(ip_address, 'netbiosName', str)
            check(ip_address, 'dnsName', str)
            check(ip_address, 'uuid', str)
            check(ip_address, 'macAddress', str)
        check(vuln, 'name', str)
        check(vuln, 'pluginDescription', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'total', str)


@responses.activate
def test_analysis_vulns_vulnipsummary_tool(tsc):
    """
    test analysis vulnerabilities 'vulnerability ip summary' tool for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '358',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '1629',
                'results': [
                    {
                        'pluginID': '10092',
                        'total': '1',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'name': 'FTP Server Detection',
                        'pluginDescription': 'It is possible to obtain the banner of the remote FTP server by connecting to a remote port.',
                        'repositoryID': '1',
                        'hosts': [
                            {
                                'iplist': '192.168.101.30',
                                'uuidIPsList': '',
                                'repository': {
                                    'id': '1',
                                    'name': 'Default',
                                    'description': '',
                                    'dataFormat': 'IPv4',
                                },
                            }
                        ],
                        'family': {
                            'id': '24',
                            'name': 'Service detection',
                            'type': 'active',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080233,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '358',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '1629',
                'results': [
                    {
                        'pluginID': '10267',
                        'total': '14',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'name': 'SSH Server Type and Version Information',
                        'pluginDescription': 'It is possible to obtain information about the remote SSH server by sending an empty authentication request.',
                        'repositoryID': '1',
                        'hosts': [
                            {
                                'iplist': '192.168.100.5,192.168.100.10,192.168.101.30,192.168.101.115,192.168.101.117,192.168.101.130,192.168.101.133,192.168.101.140,192.168.101.146,192.168.101.177-192.168.101.179,192.168.101.189,192.168.101.191',
                                'uuidIPsList': '',
                                'repository': {
                                    'id': '1',
                                    'name': 'Default',
                                    'description': '',
                                    'dataFormat': 'IPv4',
                                },
                            }
                        ],
                        'family': {
                            'id': '24',
                            'name': 'Service detection',
                            'type': 'active',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080234,
        },
    )
    vulns = tsc.analysis.vulns(tool='vulnipsummary', pages=2, limit=5)
    for vuln in vulns:
        check(vuln, 'family', dict)
        check(vuln['family'], 'type', str)
        check(vuln['family'], 'id', str)
        check(vuln['family'], 'name', str)
        check(vuln, 'hosts', list)
        host = vuln['hosts'][0]
        check(host, 'iplist', str)
        check(host, 'repository', dict)
        check(host['repository'], 'dataFormat', str)
        check(host['repository'], 'description', str)
        check(host['repository'], 'id', str)
        check(host['repository'], 'name', str)
        check(vuln, 'name', str)
        check(vuln, 'pluginDescription', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'total', str)


@responses.activate
def test_analysis_console_logs(tsc):
    """
    test analysis console logs for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'skip': {'201812': 'false'},
                'results': [
                    {
                        'rawLog': "Mon, 17 Dec 2018 15:56:25 -0500|api|auth|INFO|Successful login for 'api' from 192.168.106.100 (authentication type: tns).\n",
                        'organization': {
                            'id': '1',
                            'name': 'HomeNet',
                            'description': '',
                        },
                        'message': "Successful login for 'api' from 192.168.106.100 (authentication type: tns).",
                        'severity': {
                            'id': '0',
                            'name': 'INFO',
                            'description': 'Information',
                        },
                        'module': 'auth',
                        'initiator': {
                            'id': '2',
                            'username': 'api',
                            'firstname': 'api',
                            'lastname': 'user',
                        },
                        'date': 'Mon, 17 Dec 2018 15:56:25 -0500',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080235,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'skip': {'201812': 'false'},
                'results': [
                    {
                        'rawLog': "Mon, 17 Dec 2018 14:52:06 -0500|api|auth|INFO|Successful login for 'api' from 192.168.106.100 (authentication type: tns).\n",
                        'organization': {
                            'id': '1',
                            'name': 'HomeNet',
                            'description': '',
                        },
                        'message': "Successful login for 'api' from 192.168.106.100 (authentication type: tns).",
                        'severity': {
                            'id': '0',
                            'name': 'INFO',
                            'description': 'Information',
                        },
                        'module': 'auth',
                        'initiator': {
                            'id': '2',
                            'username': 'api',
                            'firstname': 'api',
                            'lastname': 'user',
                        },
                        'date': 'Mon, 17 Dec 2018 14:52:06 -0500',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080235,
        },
    )
    logs = tsc.analysis.console(pages=2, limit=5)
    for log in logs:
        assert isinstance(log, dict)
        check(log, 'initiator', dict)
        check(log['initiator'], 'username', str)
        check(log['initiator'], 'firstname', str)
        check(log['initiator'], 'lastname', str)
        try:
            check(log['initiator'], 'id', int)
        except AssertionError:
            check(log['initiator'], 'id', str)
        check(log, 'severity', dict)
        check(log['severity'], 'description', str)
        check(log['severity'], 'id', str)
        check(log['severity'], 'name', str)
        check(log, 'rawLog', str)
        check(log, 'module', str)
        check(log, 'date', 'datetime')
        check(log, 'organization', dict)
        check(log['organization'], 'description', str)
        check(log['organization'], 'id', str)
        check(log['organization'], 'name', str)
        check(log, 'message', str)


@responses.activate
def test_analysis_mobile_listvuln(tsc):
    """
    test analysis mobile list vulnerability for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '244',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '-1 ',
                'results': [
                    {
                        'pluginID': '60035',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'identifier': 'iPad/roL89WeF21YvMYPryaT8KileVoCFnintNfh515lk',
                        'pluginName': 'MDM Mobile Device Reporting',
                        'repository': {
                            'id': '3',
                            'name': 'GoodMDM',
                            'description': '',
                            'dataFormat': 'mobile',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080236,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '244',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '-1 ',
                'results': [
                    {
                        'pluginID': '65633',
                        'severity': {
                            'id': '3',
                            'name': 'High',
                            'description': 'High Severity',
                        },
                        'identifier': 'iPhone/M1DUzuSKEg',
                        'pluginName': 'Apple iOS < 6.1.3 Multiple Vulnerabilities',
                        'repository': {
                            'id': '3',
                            'name': 'GoodMDM',
                            'description': '',
                            'dataFormat': 'mobile',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080236,
        },
    )
    vulns = tsc.analysis.mobile(tool='listvuln', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'identifier', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'pluginName', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)


@responses.activate
def test_analysis_mobile_sumdeviceid(tsc):
    """
    test analysis mobile sum device id for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '95',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '244:16:126:7:0:95:1921 ',
                'results': [
                    {
                        'identifier': 'Android/androidc0xnDVRnSop',
                        'model': 'Android',
                        'serial': 'androidchbUSsOako4',
                        'total': '1',
                        'score': '0',
                        'severityInfo': '1',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                        'repository': {
                            'id': '3',
                            'name': 'GoodMDM',
                            'description': '',
                            'dataFormat': 'mobile',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080237,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '95',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '244:16:126:7:0:95:1921 ',
                'results': [
                    {
                        'identifier': 'Android/androidc9QnzCvPvLb',
                        'model': 'Android',
                        'serial': 'androidcn6rTRa6Aup',
                        'total': '1',
                        'score': '0',
                        'severityInfo': '1',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                        'repository': {
                            'id': '3',
                            'name': 'GoodMDM',
                            'description': '',
                            'dataFormat': 'mobile',
                        },
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080237,
        },
    )
    vulns = tsc.analysis.mobile(tool='sumdeviceid', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'identifier', str)
        check(vuln, 'model', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)
        check(vuln, 'score', str)
        check(vuln, 'serial', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'total', str)


@responses.activate
def test_analysis_mobile_summdmuser(tsc):
    """
    test analysis mobile sum mdm user for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '68',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '68:0:0:0:0:68:0 ',
                'results': [
                    {
                        'user': 'John Doe',
                        'total': '1',
                        'score': '0',
                        'severityInfo': '1',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080238,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '68',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '68:0:0:0:0:68:0 ',
                'results': [
                    {
                        'user': 'SOMECORP.COM/Jane11 Doe11',
                        'total': '1',
                        'score': '0',
                        'severityInfo': '1',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080239,
        },
    )
    vulns = tsc.analysis.mobile(tool='summdmuser', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'score', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'total', str)
        check(vuln, 'user', str)


@responses.activate
def test_analysis_mobile_summodel(tsc):
    """
    test analysis mobile sum model for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '5',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '244:16:126:7:0:95:1921:95 ',
                'results': [
                    {
                        'model': 'Android',
                        'total': '43',
                        'deviceCount': '43',
                        'score': '0',
                        'severityInfo': '43',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '0',
                        'severityCritical': '0',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080239,
        },
    )
    vulns = tsc.analysis.mobile(tool='summodel', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'deviceCount', str)
        check(vuln, 'model', str)
        check(vuln, 'score', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'total', str)


@responses.activate
def test_analysis_mobile_sumoscpe(tsc):
    """
    test analysis mobile sum oscpe for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '2',
                'returnedRecords': 2,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '176:16:126:7:0:27:1921:27 ',
                'results': [
                    {
                        'osCPE': 'cpe:/o:apple:ios',
                        'total': '162',
                        'deviceCount': '20',
                        'score': '1900',
                        'severityInfo': '20',
                        'severityLow': '0',
                        'severityMedium': '0',
                        'severityHigh': '126',
                        'severityCritical': '16',
                    }
                ]
                * 2,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080240,
        },
    )
    vulns = tsc.analysis.mobile(tool='sumoscpe', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'deviceCount', str)
        check(vuln, 'osCPE', str)
        check(vuln, 'score', str)
        check(vuln, 'severityCritical', str)
        check(vuln, 'severityHigh', str)
        check(vuln, 'severityInfo', str)
        check(vuln, 'severityLow', str)
        check(vuln, 'severityMedium', str)
        check(vuln, 'total', str)


@responses.activate
def test_analysis_mobile_sumpluginid(tsc):
    """
    test analysis mobile sum plugin id for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '10',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '244:16:126:7:0:95:1921 ',
                'results': [
                    {
                        'pluginID': '60025',
                        'name': 'Apple iOS < 5.0.1 Multiple Vulnerabilities',
                        'severity': {
                            'id': '3',
                            'name': 'High',
                            'description': 'High Severity',
                        },
                        'total': '16',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080241,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '10',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '244:16:126:7:0:95:1921 ',
                'results': [
                    {
                        'pluginID': '62242',
                        'name': 'Apple iOS < 6.0 Multiple Vulnerabilities',
                        'severity': {
                            'id': '3',
                            'name': 'High',
                            'description': 'High Severity',
                        },
                        'total': '19',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080241,
        },
    )
    vulns = tsc.analysis.mobile(tool='sumpluginid', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'name', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'total', str)


@responses.activate
def test_analysis_mobile_vulndetails(tsc):
    """
    test analysis mobile vulnerability details for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '244',
                'returnedRecords': 5,
                'startOffset': '0',
                'endOffset': '5',
                'matchingDataElementCount': '-1 ',
                'results': [
                    {
                        'pluginID': '60035',
                        'severity': {
                            'id': '0',
                            'name': 'Info',
                            'description': 'Informative',
                        },
                        'identifier': 'iPad/roL89WeF21YvMYPryaT8KileVoCFnintNfh515lk',
                        'model': 'iPad',
                        'serial': 'BnvalFZVrSMQTLbOmmTWgi9Qdi2jMgtdxGI6cEdC',
                        'deviceVersion': '6.1.3',
                        'port': '0',
                        'protocol': 'tcp',
                        'pluginName': 'MDM Mobile Device Reporting',
                        'user': 'John Doe',
                        'mdmType': '',
                        'osCPE': '',
                        'lastSeen': '-1',
                        'pluginOutput': 'Serial Number : BnvalFZVrSMQTLbOmmTWgi9Qdi2jMgtdxGI6cEdC\\nDevice : iPad 4th generation (WiFi)\\nModel : iPad\\nVersion : 6.1.3\\nTimestamp : No Timestamp (Good MDM)\\nUser : John Doe\\nManaged By :\\n    Good MDM',
                        'exploitAvailable': 'No',
                        'exploitEase': '',
                        'exploitFrameworks': '',
                        'synopsis': 'Gathers mobile device information from MDMs and reports settings.',
                        'description': 'This plugin gathers the information provided from mobile device management systems around the network and reports the devices, information, and where they are managed.',
                        'solution': 'n/a',
                        'seeAlso': '',
                        'riskFactor': 'None',
                        'stigSeverity': '',
                        'baseScore': '0.0',
                        'temporalScore': '0.0',
                        'cvssVector': '',
                        'cvssV3BaseScore': '0.0',
                        'cvssV3TemporalScore': '0.0',
                        'cvssV3Vector': '',
                        'cpe': '',
                        'vulnPubDate': '-1',
                        'patchPubDate': '-1',
                        'pluginPubDate': '1338480000',
                        'pluginModDate': '1544806800',
                        'checkType': 'local',
                        'version': '1.52',
                        'cve': '',
                        'bid': '',
                        'xref': '',
                        'repository': {
                            'id': '3',
                            'name': 'GoodMDM',
                            'description': '',
                            'dataFormat': 'mobile',
                        },
                        'pluginInfo': '60035 (0/tcp) MDM Mobile Device Reporting',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080242,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': '244',
                'returnedRecords': 5,
                'startOffset': '5',
                'endOffset': '10',
                'matchingDataElementCount': '-1 ',
                'results': [
                    {
                        'pluginID': '65633',
                        'severity': {
                            'id': '3',
                            'name': 'High',
                            'description': 'High Severity',
                        },
                        'identifier': 'iPhone/M1DUzuSKEg',
                        'model': 'iPhone',
                        'serial': 'XreYyuUVc9',
                        'deviceVersion': '4.4.8',
                        'port': '0',
                        'protocol': 'tcp',
                        'pluginName': 'Apple iOS < 6.1.3 Multiple Vulnerabilities',
                        'user': '',
                        'mdmType': '',
                        'osCPE': 'cpe:/o:apple:ios',
                        'lastSeen': '1365772591',
                        'pluginOutput': 'Apple iOS vulnerable version detected\\n  Model         :  iPhone\\n  Serial Number :  XreYyuUVc9\\n  Version       :  4.4.8\\n  Fixed Version :  6.1.3 ',
                        'exploitAvailable': 'No',
                        'exploitEase': 'No known exploits are available',
                        'exploitFrameworks': '',
                        'synopsis': 'Report iOS devices older than 6.1.3.',
                        'description': 'The mobile device is running a version of iOS that is older than version 6.1.3.  This version contains security-related ',
                        'solution': 'Apple has released a set of patches for iOS-based devices.',
                        'seeAlso': 'https://support.apple.com/en-us/HT202706\\nhttps://lists.apple.com/archives/security-announce/2013/Mar/msg00004.html',
                        'riskFactor': 'High',
                        'stigSeverity': '',
                        'baseScore': '9.3',
                        'temporalScore': '6.9',
                        'cvssVector': 'AV:N/AC:M/Au:N/C:C/I:C/A:C/E:U/RL:OF/RC:C',
                        'cvssV3BaseScore': '0.0',
                        'cvssV3TemporalScore': '0.0',
                        'cvssV3Vector': '',
                        'cpe': 'cpe:/o:apple:iphone_os',
                        'vulnPubDate': '1360947600',
                        'patchPubDate': '1363708800',
                        'pluginPubDate': '1363795200',
                        'pluginModDate': '1544806800',
                        'checkType': 'local',
                        'version': '1.49',
                        'cve': 'CVE-2013-0912,CVE-2013-0977,CVE-2013-0978,CVE-2013-0979,CVE-2013-0980,CVE-2013-0981',
                        'bid': '57967,57990,58586,58588,58589,58590',
                        'xref': '',
                        'repository': {
                            'id': '3',
                            'name': 'GoodMDM',
                            'description': '',
                            'dataFormat': 'mobile',
                        },
                        'pluginInfo': '65633 (0/tcp) Apple iOS < 6.1.3 Multiple Vulnerabilities',
                    }
                ]
                * 5,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080242,
        },
    )
    vulns = tsc.analysis.mobile(pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'baseScore', str)
        check(vuln, 'bid', str)
        check(vuln, 'checkType', str)
        check(vuln, 'cpe', str)
        check(vuln, 'cve', str)
        check(vuln, 'cvssVector', str)
        check(vuln, 'description', str)
        check(vuln, 'deviceVersion', str)
        check(vuln, 'exploitAvailable', str)
        check(vuln, 'exploitEase', str)
        check(vuln, 'exploitFrameworks', str)
        check(vuln, 'identifier', str)
        check(vuln, 'lastSeen', str)
        check(vuln, 'mdmType', str)
        check(vuln, 'model', str)
        check(vuln, 'osCPE', str)
        check(vuln, 'patchPubDate', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'pluginInfo', str)
        check(vuln, 'pluginModDate', str)
        check(vuln, 'pluginName', str)
        check(vuln, 'pluginOutput', str)
        check(vuln, 'pluginPubDate', str)
        check(vuln, 'port', str)
        check(vuln, 'protocol', str)
        check(vuln, 'repository', dict)
        check(vuln['repository'], 'description', str)
        check(vuln['repository'], 'id', str)
        check(vuln['repository'], 'name', str)
        check(vuln, 'riskFactor', str)
        check(vuln, 'seeAlso', str)
        check(vuln, 'serial', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'solution', str)
        check(vuln, 'stigSeverity', str)
        check(vuln, 'synopsis', str)
        check(vuln, 'temporalScore', str)
        check(vuln, 'user', str)
        check(vuln, 'version', str)
        check(vuln, 'vulnPubDate', str)
        check(vuln, 'xref', str)


@responses.activate
def test_analysis_events_listdata(tsc):
    """
    test analysis events list data for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 48141,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48141,
                'results': [
                    {
                        'time': '1545069201',
                        'event': 'PF-Blocked_Inbound_Connection',
                        'source ip': '185.255.31.78',
                        'destination ip': '24.15.184.174',
                        'protocol': '0',
                        'destination port': '13284',
                        'number of vulns': '0',
                        'sensor': 'Syslog',
                        'type': 'firewall',
                        'va/ids': '0',
                    }
                ]
                * 5,
                'startTime': 1544993843,
                'endTime': 1545080243,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080243,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 48141,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48141,
                'results': [
                    {
                        'time': '1545069201',
                        'event': 'Apache-Content_CSS_Request',
                        'source ip': '192.168.106.100',
                        'destination ip': '192.168.101.1',
                        'protocol': '0',
                        'destination port': '0',
                        'number of vulns': '0',
                        'sensor': 'Syslog',
                        'type': 'web-access',
                        'va/ids': '0',
                    }
                ]
                * 5,
                'startTime': 1544993844,
                'endTime': 1545080244,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080244,
        },
    )
    events = tsc.analysis.events(tool='listdata', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'destination ip', str)
        check(event, 'destination port', str)
        check(event, 'event', str)
        check(event, 'number of vulns', str)
        check(event, 'protocol', str)
        check(event, 'sensor', str)
        check(event, 'source ip', str)
        check(event, 'time', str)
        check(event, 'type', str)
        check(event, 'va/ids', str)


@responses.activate
def test_analysis_events_sumasset(tsc):
    """
    test analysis events sum asset for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 34,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 134116,
                'results': [
                    {
                        'count': '64187',
                        'asset': {
                            'id': '2',
                            'name': 'Systems that have been Scanned',
                            'description': 'This asset uses the Scan Summary plugin to detect if a host has been scanned by Nessus. The Scan Summary plugin contains the list of tests conducted during the most recent scan.',
                            'type': 'dynamic',
                            'status': '0',
                        },
                    }
                ]
                * 5,
                'startTime': 1544994095,
                'endTime': 1545080495,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080495,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 34,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 134152,
                'results': [
                    {
                        'count': '5613',
                        'asset': {
                            'id': '3',
                            'name': 'Windows Hosts',
                            'description': 'The operating system detected has Windows installed.\n\nThis will be helpful for those getting started with SecurityCenter.',
                            'type': 'dynamic',
                            'status': '0',
                        },
                    }
                ]
                * 5,
                'startTime': 1544994097,
                'endTime': 1545080497,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080497,
        },
    )
    events = tsc.analysis.events(tool='sumasset', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'asset', dict)
        check(event['asset'], 'description', str)
        check(event['asset'], 'id', str)
        check(event['asset'], 'name', str)
        check(event['asset'], 'status', str)
        check(event['asset'], 'type', str)
        try:
            check(event, 'count', str)
        except AssertionError:
            check(event, 'count', int)


@responses.activate
def test_analysis_events_sumclassa(tsc):
    """
    test analysis events sum class-a for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 114,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48181,
                'results': [{'class-a': '192.0.0.0/8', 'count': '81815'}] * 5,
                'startTime': 1544993848,
                'endTime': 1545080248,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080248,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 114,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48181,
                'results': [{'class-a': '17.0.0.0/8', 'count': '451'}] * 5,
                'startTime': 1544993850,
                'endTime': 1545080250,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080249,
        },
    )
    events = tsc.analysis.events(tool='sumclassa', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-a', str)
        check(event, 'count', str)


@responses.activate
def test_analysis_events_sumclassb(tsc):
    """
    test analysis events sum class-b for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 263,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48181,
                'results': [{'class-b': '192.168.0.0/16', 'count': '81663'}] * 5,
                'startTime': 1544993851,
                'endTime': 1545080251,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080251,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 263,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48181,
                'results': [{'class-b': '209.208.0.0/16', 'count': '380'}] * 5,
                'startTime': 1544993852,
                'endTime': 1545080252,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080252,
        },
    )
    events = tsc.analysis.events(tool='sumclassb', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-b', str)
        check(event, 'count', str)


@responses.activate
def test_analysis_events_sumclassc(tsc):
    """
    test analysis events sum class-c for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 425,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48181,
                'results': [{'class-c': '192.168.101.0/24', 'count': '63790'}] * 5,
                'startTime': 1544993853,
                'endTime': 1545080253,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080253,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 425,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48181,
                'results': [{'class-c': '224.0.0.0/24', 'count': '390'}] * 5,
                'startTime': 1544993855,
                'endTime': 1545080255,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080254,
        },
    )
    events = tsc.analysis.events(tool='sumclassc', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-c', str)
        check(event, 'count', str)


@responses.activate
def test_analysis_events_sumconns(tsc):
    """
    test analysis events sum conns for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 881,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48181,
                'results': [
                    {
                        'source ip': '192.168.101.179',
                        'destination ip': '192.168.101.1',
                        'count': '21431',
                    }
                ]
                * 5,
                'startTime': 1544993856,
                'endTime': 1545080256,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080256,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 881,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48208,
                'results': [
                    {
                        'source ip': '192.168.104.188',
                        'destination ip': '192.168.106.100',
                        'count': '851',
                    }
                ]
                * 5,
                'startTime': 1544993857,
                'endTime': 1545080257,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080257,
        },
    )
    events = tsc.analysis.events(tool='sumconns', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'destination ip', str)
        check(event, 'source ip', str)


@responses.activate
def test_analysis_events_sumdate(tsc):
    """
    test analysis events sum date for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 1,
                'returnedRecords': 1,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48208,
                'results': [
                    {
                        'date': 'Dec 17, 2018',
                        'time block start': '1545022800',
                        'time block stop': '1545109199',
                        'count': '48208',
                        '24-hour plot': '0,0,0,0,0,0,0,0,0,0,0,0,804,34828,6422,6154,0,0,0,0,0,0,0,0',
                    }
                ],
                'startTime': 1544993858,
                'endTime': 1545080258,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080258,
        },
    )
    events = tsc.analysis.events(tool='sumdate', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'date', str)
        check(event, 'time block start', str)
        check(event, 'time block stop', str)


@responses.activate
def test_analysis_events_sumdstip(tsc):
    """
    test analysis events sum ds tip for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 555,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48208,
                'results': [
                    {
                        'address': '192.168.101.1',
                        'count': '27047',
                        'lce': {
                            'id': '1',
                            'name': 'Internal LCE',
                            'description': '',
                            'status': '1',
                        },
                    }
                ]
                * 5,
                'startTime': 1544993859,
                'endTime': 1545080259,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080259,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 555,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48208,
                'results': [
                    {
                        'address': '192.168.106.1',
                        'count': '1240',
                        'lce': {
                            'id': '1',
                            'name': 'Internal LCE',
                            'description': '',
                            'status': '1',
                        },
                    }
                ]
                * 5,
                'startTime': 1544993861,
                'endTime': 1545080261,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080261,
        },
    )
    events = tsc.analysis.events(tool='sumdstip', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'address', str)
        check(event, 'count', str)
        check(event, 'lce', dict)
        check(event['lce'], 'description', str)
        check(event['lce'], 'id', str)
        check(event['lce'], 'name', str)
        check(event['lce'], 'status', str)


@responses.activate
def test_analysis_events_sumevent(tsc):
    """
    test analysis events sum event for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 76,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48208,
                'results': [
                    {
                        'event': 'Apache-405_PUT',
                        'description': 'The Apache web server encountered an invalid web put which returned an Apache error code in the 400 range.',
                        'file': 'web_apache.prm',
                        '24-hour plot': '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,0,0,0,0',
                        'count': '6',
                    }
                ]
                * 5,
                'startTime': 1544993862,
                'endTime': 1545080262,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080262,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 76,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48208,
                'results': [
                    {
                        'event': 'DHCP-Discover',
                        'description': 'A DHCP Discover was issued.',
                        'file': 'dhcp.prm',
                        '24-hour plot': '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,36,17,0,1,0,0',
                        'count': '54',
                    }
                ]
                * 5,
                'startTime': 1544993863,
                'endTime': 1545080263,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080263,
        },
    )
    events = tsc.analysis.events(tool='sumevent', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'description', str)
        check(event, 'event', str)
        check(event, 'file', str)


@responses.activate
def test_analysis_events_sumevent2(tsc):
    """
    test analysis events sum event for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 1,
                'returnedRecords': 1,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 5480,
                'results': [
                    {
                        'event': 'unnormalized',
                        'description': 'No description found.',
                        'file': 'File not found.',
                        '24-hour plot': '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,30,2524,2739,47,45,60,35',
                        'count': '5480',
                    }
                ],
                'startTime': 1544993864,
                'endTime': 1545080264,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080264,
        },
    )
    events = tsc.analysis.events(tool='sumevent2', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'description', str)
        check(event, 'event', str)
        check(event, 'file', str)


@responses.activate
def test_analysis_events_sumip(tsc):
    """
    test analysis events sum ip for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 781,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48208,
                'results': [
                    {
                        'address': '192.168.101.1',
                        'count': '33102',
                        'lce': {
                            'id': '1',
                            'name': 'Internal LCE',
                            'description': '',
                            'status': '1',
                        },
                    }
                ]
                * 5,
                'startTime': 1544993866,
                'endTime': 1545080266,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080266,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 781,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48234,
                'results': [
                    {
                        'address': '192.168.101.30',
                        'count': '5499',
                        'lce': {
                            'id': '1',
                            'name': 'Internal LCE',
                            'description': '',
                            'status': '1',
                        },
                    }
                ]
                * 5,
                'startTime': 1544993867,
                'endTime': 1545080267,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080267,
        },
    )
    events = tsc.analysis.events(tool='sumip', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'address', str)
        check(event, 'count', str)
        check(event, 'lce', dict)
        check(event['lce'], 'description', str)
        check(event['lce'], 'id', str)
        check(event['lce'], 'name', str)
        check(event['lce'], 'status', str)


@responses.activate
def test_analysis_events_sumport(tsc):
    """
    test analysis events sum port for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 6960,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48234,
                'results': [{'port': '0', 'count': '61292'}] * 5,
                'startTime': 1544993868,
                'endTime': 1545080268,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080268,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 6960,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48234,
                'results': [{'port': '53', 'count': '1230'}] * 5,
                'startTime': 1544993869,
                'endTime': 1545080269,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080269,
        },
    )
    events = tsc.analysis.events(tool='sumport', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'port', str)


@responses.activate
def test_analysis_events_sumprotocol(tsc):
    """
    test analysis events sum protocol for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 3,
                'returnedRecords': 3,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48234,
                'results': [{'protocol': 'Unknown(0)', 'count': '32241'}] * 3,
                'startTime': 1544993870,
                'endTime': 1545080270,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080270,
        },
    )
    events = tsc.analysis.events(tool='sumprotocol', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'protocol', str)


@responses.activate
def test_analysis_events_sumsrcip(tsc):
    """
    test analysis events sum src ip for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 268,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48234,
                'results': [
                    {
                        'address': '192.168.101.179',
                        'count': '21757',
                        'lce': {
                            'id': '1',
                            'name': 'Internal LCE',
                            'description': '',
                            'status': '1',
                        },
                    }
                ]
                * 5,
                'startTime': 1544993872,
                'endTime': 1545080272,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080272,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 268,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48234,
                'results': [
                    {
                        'address': '192.168.104.171',
                        'count': '921',
                        'lce': {
                            'id': '1',
                            'name': 'Internal LCE',
                            'description': '',
                            'status': '1',
                        },
                    }
                ]
                * 5,
                'startTime': 1544993873,
                'endTime': 1545080273,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080273,
        },
    )
    events = tsc.analysis.events(tool='sumsrcip', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'address', str)
        check(event, 'count', str)
        check(event, 'lce', dict)
        check(event['lce'], 'description', str)
        check(event['lce'], 'id', str)
        check(event['lce'], 'name', str)
        check(event['lce'], 'status', str)


@responses.activate
def test_analysis_events_sumtime(tsc):
    """
    test analysis events sum time for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 100,
                'returnedRecords': 100,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 0,
                'results': [
                    {
                        'time block start': '1544993874',
                        'time block stop': '1544994737',
                        'count': '0',
                    }
                ]
                * 100,
                'startTime': '1544993874',
                'endTime': 1545080274,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080274,
        },
    )
    events = tsc.analysis.events(tool='sumtime', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'time block start', str)
        check(event, 'time block stop', str)


@responses.activate
def test_analysis_events_sumtype(tsc):
    """
    test analysis events sum type for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 18,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48234,
                'results': [
                    {
                        'type': 'application',
                        '24-hour plot': '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,11,2,6,2,2',
                        'count': '32',
                    }
                ]
                * 5,
                'startTime': 1544993876,
                'endTime': 1545080276,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080275,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 18,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48234,
                'results': [
                    {
                        'type': 'firewall',
                        '24-hour plot': '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,483,1863,1528,1238,1299,1545,1294',
                        'count': '9250',
                    }
                ]
                * 5,
                'startTime': 1544993877,
                'endTime': 1545080277,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080277,
        },
    )
    events = tsc.analysis.events(tool='sumtype', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'type', str)


@responses.activate
def test_analysis_events_sumuser(tsc):
    """
    test analysis events sum user for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 4,
                'returnedRecords': 4,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48252,
                'results': [
                    {
                        'user': '(unknown)',
                        '24-hour plot': '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1472,17144,17024,2967,3179,3189,2953',
                        'count': '47928',
                    }
                ]
                * 4,
                'startTime': 1544993878,
                'endTime': 1545080278,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080278,
        },
    )
    events = tsc.analysis.events(tool='sumuser', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'user', str)


@responses.activate
def test_analysis_events_syslog(tsc):
    """
    test analysis events sys log for success
    """
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 48252,
                'returnedRecords': 5,
                'startOffset': 0,
                'endOffset': 5,
                'matchingDataElementCount': 48252,
                'results': [
                    {
                        'time': '1545069201',
                        'sensor': 'Syslog',
                        'type': 'firewall',
                        'message': '<134>Dec 17 11:53:19 filterlog: 9,,,1000000103,igb1,match,block,in,4,0x20,,237,29416,0,none,6,tcp,40,185.255.31.78,24.15.184.174,53590,13284,0,S,3403610530,,1024,,',
                    }
                ]
                * 5,
                'startTime': 1544993879,
                'endTime': 1545080279,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080279,
        },
    )
    responses.post(
        'https://nourl/rest/analysis',
        json={
            'type': 'regular',
            'response': {
                'totalRecords': 48252,
                'returnedRecords': 5,
                'startOffset': 5,
                'endOffset': 10,
                'matchingDataElementCount': 48252,
                'results': [
                    {
                        'time': '1545069201',
                        'sensor': 'Syslog',
                        'type': 'connection',
                        'message': '<134>Dec 17 11:53:18 filterlog: 136,,,1455312420,igb2.106,match,pass,in,4,0x0,,64,0,0,DF,6,tcp,64,192.168.106.100,192.168.101.179,54181,8834,0,S,1440727508,,65535,,mss;nop;wscale;nop;nop;TS;sackOK;eol',
                    }
                ]
                * 5,
                'startTime': 1544993880,
                'endTime': 1545080280,
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1545080280,
        },
    )
    events = tsc.analysis.events(tool='syslog', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'message', str)
        check(event, 'sensor', str)
        check(event, 'time', str)
        check(event, 'type', str)
