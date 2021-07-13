import pytest
from tenable.sc.analysis import AnalysisResultsIterator
from ..checker import check
from tenable.errors import UnexpectedValueError


def test_analysis_constructor_type_error(sc):
    with pytest.raises(TypeError):
        sc.analysis._analysis(tool=1, type='type',
                              sort_field='field',
                              sort_direction=1)

    with pytest.raises(TypeError):
        sc.analysis._analysis(tool=1, type='type',
                              sort_field='field',
                              sort_direction='ASC',
                              offset=0,
                              limit='limit')


def test_analysis_constructor_success(sc):
    analysis = sc.analysis._analysis(tool=1, type='type',
                                     sort_field='field',
                                     sort_direction='ASC',
                                     offset=0,
                                     payload={'sourceType': 'individual'})
    assert isinstance(analysis, AnalysisResultsIterator)


def test_analysis_asset_expansion_simple(sc):
    resp = sc.analysis._combo_expansion(('or', 1, 2))
    assert resp == {
        'operator': 'union',
        'operand1': {'id': '1'},
        'operand2': {'id': '2'},
    }


def test_analysis_asset_expansion_complex(sc):
    resp = sc.analysis._combo_expansion(
        ('or', ('and', 1, 2), ('not', ('or', 3, 4))))
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
                'operand2': {'id': '4'}
            }
        }
    }


def test_analysis_query_constructor_simple(sc):
    resp = sc.analysis._query_constructor(
        ('filter1', 'operator1', 'value1'),
        ('filter2', 'operator2', 'value2'),
        tool='tool_test',
        type='type_test')
    assert resp == {
        'tool': 'tool_test',
        'query': {
            'tool': 'tool_test',
            'type': 'type_test',
            'filters': [{
                'filterName': 'filter1',
                'operator': 'operator1',
                'value': 'value1',
            }, {
                'filterName': 'filter2',
                'operator': 'operator2',
                'value': 'value2'
            }]
        }
    }


def test_analysis_query_constructor_replace(sc):
    resp = sc.analysis._query_constructor(
        ('filter1', 'operator1', 'badvalue'),
        ('filter1', 'operator1', 'value1'),
        ('filter2', 'operator2', 'value2'),
        tool='tool_test',
        type='type_test')
    assert resp == {
        'tool': 'tool_test',
        'query': {
            'tool': 'tool_test',
            'type': 'type_test',
            'filters': [{
                'filterName': 'filter1',
                'operator': 'operator1',
                'value': 'value1',
            }, {
                'filterName': 'filter2',
                'operator': 'operator2',
                'value': 'value2'
            }]
        }
    }


def test_analysis_query_constructor_remove(sc):
    resp = sc.analysis._query_constructor(
        ('filter3', 'operator1', 'badvalue'),
        ('filter1', 'operator1', 'value1'),
        ('filter2', 'operator2', 'value2'),
        ('filter3', None, None),
        tool='tool_test',
        type='type_test')
    assert resp == {
        'tool': 'tool_test',
        'query': {
            'tool': 'tool_test',
            'type': 'type_test',
            'filters': [{
                'filterName': 'filter1',
                'operator': 'operator1',
                'value': 'value1',
            }, {
                'filterName': 'filter2',
                'operator': 'operator2',
                'value': 'value2'
            }]
        }
    }


def test_analysis_query_constructor_asset(sc):
    resp = sc.analysis._query_constructor(('asset', '~', ('or', 1, 2)),
                                          tool='tool', type='type')
    assert resp == {
        'tool': 'tool',
        'query': {
            'tool': 'tool',
            'type': 'type',
            'filters': [{
                'filterName': 'asset',
                'operator': '~',
                'value': {
                    'operator': 'union',
                    'operand1': {'id': '1'},
                    'operand2': {'id': '2'},
                }
            }]
        }
    }


def test_analysis_vulns(sc):
    vulns = sc.analysis.vulns(source='cumulative', scan_id=1)
    assert isinstance(vulns, AnalysisResultsIterator)


def test_analysis_scan(sc):
    scan = sc.analysis.scan(1)
    assert isinstance(scan, AnalysisResultsIterator)


def test_analysis_events(sc):
    event = sc.analysis.events(source='archive', silo_id='silo_id')
    assert isinstance(event, AnalysisResultsIterator)


def test_analysis_events_unexpected_value_error(sc):
    with pytest.raises(UnexpectedValueError):
        sc.analysis.events(source='archive')


@pytest.mark.vcr()
def test_analysis_vulns_cceipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='cceipdetail', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@pytest.mark.vcr()
def test_analysis_vulns_cveipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='cveipdetail', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_iavmipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='iavmipdetail', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_iplist_tool(sc):
    vulns = sc.analysis.vulns(tool='iplist', pages=2, limit=5)
    assert isinstance(vulns, dict)
    for vuln in vulns:
        check(vulns, vuln, str)


@pytest.mark.vcr()
def test_analysis_vulns_listmailclients_tool(sc):
    vulns = sc.analysis.vulns(tool='listmailclients', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listservices_tool(sc):
    vulns = sc.analysis.vulns(tool='listservices', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listos_tool(sc):
    vulns = sc.analysis.vulns(tool='listos', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listsoftware_tool(sc):
    vulns = sc.analysis.vulns(tool='listsoftware', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listsshservers_tool(sc):
    vulns = sc.analysis.vulns(tool='listsshservers', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listvuln_tool(sc):
    vulns = sc.analysis.vulns(tool='listvuln', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_listwebclients_tool(sc):
    vulns = sc.analysis.vulns(tool='listwebclients', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listwebservers_tool(sc):
    vulns = sc.analysis.vulns(tool='listwebservers', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_sumasset_tool(sc):
    vulns = sc.analysis.vulns(tool='sumasset', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumcce_tool(sc):
    vulns = sc.analysis.vulns(tool='sumcce', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@pytest.mark.vcr()
def test_analysis_vulns_sumclassa_tool(sc):
    vulns = sc.analysis.vulns(tool='sumclassa', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumclassb_tool(sc):
    vulns = sc.analysis.vulns(tool='sumclassb', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumclassc_tool(sc):
    vulns = sc.analysis.vulns(tool='sumclassc', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumcve_tool(sc):
    vulns = sc.analysis.vulns(tool='sumcve', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'cveID', str)
        check(vuln, 'total', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'hostTotal', str)


@pytest.mark.vcr()
def test_analysis_vulns_sumdnsname_tool(sc):
    vulns = sc.analysis.vulns(tool='sumdnsname', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumfamily_tool(sc):
    vulns = sc.analysis.vulns(tool='sumfamily', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumiavm_tool(sc):
    vulns = sc.analysis.vulns(tool='sumiavm', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'iavmID', str)
        check(vuln, 'total', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'hostTotal', str)


@pytest.mark.vcr()
def test_analysis_vulns_sumid_tool(sc):
    vulns = sc.analysis.vulns(tool='sumid', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumip_tool(sc):
    vulns = sc.analysis.vulns(tool='sumip', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_summsbulletin_tool(sc):
    vulns = sc.analysis.vulns(tool='summsbulletin', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'msbulletinID', str)
        check(vuln, 'total', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'hostTotal', str)


@pytest.mark.vcr()
def test_analysis_vulns_sumport_tool(sc):
    vulns = sc.analysis.vulns(tool='sumport', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumprotocol_tool(sc):
    vulns = sc.analysis.vulns(tool='sumprotocol', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumremediation_tool(sc):
    vulns = sc.analysis.vulns(tool='sumremediation', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_sumseverity_tool(sc):
    vulns = sc.analysis.vulns(tool='sumseverity', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_sumuserresponsibility_tool(sc):
    vulns = sc.analysis.vulns(tool='sumuserresponsibility', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@pytest.mark.vcr()
def test_analysis_vulns_sumuserresponsibility_tool(sc):
    vulns = sc.analysis.vulns(tool='sumuserresponsibility', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_trend_tool(sc):
    vulns = sc.analysis.vulns(tool='trend', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@pytest.mark.vcr()
def test_analysis_vulns_vulndetails_tool(sc):
    vulns = sc.analysis.vulns(tool='vulndetails', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_vulnipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='vulnipdetail', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_vulns_vulnipsummary_tool(sc):
    vulns = sc.analysis.vulns(tool='vulnipsummary', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_console_logs(sc):
    logs = sc.analysis.console(pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_mobile_listvuln(sc):
    vulns = sc.analysis.mobile(tool='listvuln', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_mobile_sumdeviceid(sc):
    vulns = sc.analysis.mobile(tool='sumdeviceid', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_mobile_summdmuser(sc):
    vulns = sc.analysis.mobile(tool='summdmuser', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_mobile_summodel(sc):
    vulns = sc.analysis.mobile(tool='summodel', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_mobile_sumoscpe(sc):
    vulns = sc.analysis.mobile(tool='sumoscpe', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_mobile_sumpluginid(sc):
    vulns = sc.analysis.mobile(tool='sumpluginid', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'name', str)
        check(vuln, 'pluginID', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)
        check(vuln, 'total', str)


@pytest.mark.vcr()
def test_analysis_mobile_vulndetails(sc):
    vulns = sc.analysis.mobile(pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_events_listdata(sc):
    events = sc.analysis.events(tool='listdata', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_events_sumasset(sc):
    events = sc.analysis.events(tool='sumasset', pages=2, limit=5)
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


@pytest.mark.vcr()
def test_analysis_events_sumclassa(sc):
    events = sc.analysis.events(tool='sumclassa', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-a', str)
        check(event, 'count', str)


@pytest.mark.vcr()
def test_analysis_events_sumclassb(sc):
    events = sc.analysis.events(tool='sumclassb', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-b', str)
        check(event, 'count', str)


@pytest.mark.vcr()
def test_analysis_events_sumclassc(sc):
    events = sc.analysis.events(tool='sumclassc', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-c', str)
        check(event, 'count', str)


@pytest.mark.vcr()
def test_analysis_events_sumconns(sc):
    events = sc.analysis.events(tool='sumconns', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'destination ip', str)
        check(event, 'source ip', str)


@pytest.mark.vcr()
def test_analysis_events_sumdate(sc):
    events = sc.analysis.events(tool='sumdate', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'date', str)
        check(event, 'time block start', str)
        check(event, 'time block stop', str)


@pytest.mark.vcr()
def test_analysis_events_sumdstip(sc):
    events = sc.analysis.events(tool='sumdstip', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'address', str)
        check(event, 'count', str)
        check(event, 'lce', dict)
        check(event['lce'], 'description', str)
        check(event['lce'], 'id', str)
        check(event['lce'], 'name', str)
        check(event['lce'], 'status', str)


@pytest.mark.vcr()
def test_analysis_events_sumevent(sc):
    events = sc.analysis.events(tool='sumevent', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'description', str)
        check(event, 'event', str)
        check(event, 'file', str)


@pytest.mark.vcr()
def test_analysis_events_sumevent2(sc):
    events = sc.analysis.events(tool='sumevent2', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'description', str)
        check(event, 'event', str)
        check(event, 'file', str)


@pytest.mark.vcr()
def test_analysis_events_sumip(sc):
    events = sc.analysis.events(tool='sumip', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'address', str)
        check(event, 'count', str)
        check(event, 'lce', dict)
        check(event['lce'], 'description', str)
        check(event['lce'], 'id', str)
        check(event['lce'], 'name', str)
        check(event['lce'], 'status', str)


@pytest.mark.vcr()
def test_analysis_events_sumport(sc):
    events = sc.analysis.events(tool='sumport', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'port', str)


@pytest.mark.vcr()
def test_analysis_events_sumprotocol(sc):
    events = sc.analysis.events(tool='sumprotocol', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'protocol', str)


@pytest.mark.vcr()
def test_analysis_events_sumsrcip(sc):
    events = sc.analysis.events(tool='sumsrcip', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'address', str)
        check(event, 'count', str)
        check(event, 'lce', dict)
        check(event['lce'], 'description', str)
        check(event['lce'], 'id', str)
        check(event['lce'], 'name', str)
        check(event['lce'], 'status', str)


@pytest.mark.vcr()
def test_analysis_events_sumtime(sc):
    events = sc.analysis.events(tool='sumtime', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'time block start', str)
        check(event, 'time block stop', str)


@pytest.mark.vcr()
def test_analysis_events_sumtype(sc):
    events = sc.analysis.events(tool='sumtype', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'type', str)


@pytest.mark.vcr()
def test_analysis_events_sumuser(sc):
    events = sc.analysis.events(tool='sumuser', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'user', str)


@pytest.mark.vcr()
def test_analysis_events_syslog(sc):
    events = sc.analysis.events(tool='syslog', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'message', str)
        check(event, 'sensor', str)
        check(event, 'time', str)
        check(event, 'type', str)
