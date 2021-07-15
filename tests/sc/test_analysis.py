'''
test file for testing various scenarios in analysis
'''
import pytest

from tenable.errors import UnexpectedValueError
from tenable.sc.analysis import AnalysisResultsIterator
from ..checker import check


def test_analysis_constructor_type_error(security_center):
    '''
    test analysis constructor for type error
    '''
    with pytest.raises(TypeError):
        getattr(security_center.analysis, '_analysis')(tool=1, type='type',
                                           sort_field='field',
                                           sort_direction=1)

    with pytest.raises(TypeError):
        getattr(security_center.analysis, '_analysis')(tool=1, type='type',
                                           sort_field='field',
                                           sort_direction='ASC',
                                           offset=0,
                                           limit='limit')


def test_analysis_constructor_success(security_center):
    '''
    test analysis constructor for success
    '''
    analysis = getattr(security_center.analysis, '_analysis')(tool=1, type='type',
                                                  sort_field='field',
                                                  sort_direction='ASC',
                                                  offset=0,
                                                  payload={'sourceType': 'individual'})
    assert isinstance(analysis, AnalysisResultsIterator)


def test_analysis_asset_expansion_simple(security_center):
    '''
    test analysis asset expansion simple for success
    '''
    resp = getattr(security_center.analysis, '_combo_expansion')(('or', 1, 2))
    assert resp == {
        'operator': 'union',
        'operand1': {'id': '1'},
        'operand2': {'id': '2'},
    }


def test_analysis_asset_expansion_complex(security_center):
    '''
    test analysis asset expansion complex for success
    '''
    resp = getattr(security_center.analysis, '_combo_expansion')(
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


def test_analysis_query_constructor_simple(security_center):
    '''
    test analysis query constructor simple for success
    '''
    resp = getattr(security_center.analysis, '_query_constructor')(
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


def test_analysis_query_constructor_replace(security_center):
    '''
    test analysis query constructor replace for success
    '''
    resp = getattr(security_center.analysis, '_query_constructor')(
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


def test_analysis_query_constructor_remove(security_center):
    '''
    test analysis query constructor remove for success
    '''
    resp = getattr(security_center.analysis, '_query_constructor')(
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


def test_analysis_query_constructor_asset(security_center):
    '''
    test analysis query constructor asset for success
    '''
    resp = getattr(security_center.analysis, '_query_constructor')(('asset', '~', ('or', 1, 2)),
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


def test_analysis_vulns(security_center):
    '''
    test analysis vulnerabilities for success
    '''
    vulns = security_center.analysis.vulns(source='cumulative', scan_id=1)
    assert isinstance(vulns, AnalysisResultsIterator)


def test_analysis_scan(security_center):
    '''
    test analysis scan for success
    '''
    scan = security_center.analysis.scan(1)
    assert isinstance(scan, AnalysisResultsIterator)


def test_analysis_events(security_center):
    '''
    test analysis events for success
    '''
    event = security_center.analysis.events(source='archive', silo_id='silo_id')
    assert isinstance(event, AnalysisResultsIterator)


def test_analysis_events_unexpected_value_error(security_center):
    '''
    test analysis events for unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.analysis.events(source='archive')


@pytest.mark.vcr()
def test_analysis_vulns_cceipdetail_tool(security_center):
    '''
    test analysis vulnerabilities cceip detail tool for success
    '''
    vulns = security_center.analysis.vulns(tool='cceipdetail', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@pytest.mark.vcr()
def test_analysis_vulns_cveipdetail_tool(security_center):
    '''
    test analysis vulnerabilities cveip detail tool for success
    '''
    vulns = security_center.analysis.vulns(tool='cveipdetail', pages=2, limit=5)
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
def test_analysis_vulns_iavmipdetail_tool(security_center):
    '''
    test analysis vulnerabilities iavmip detail tool for success
    '''
    vulns = security_center.analysis.vulns(tool='iavmipdetail', pages=2, limit=5)
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
def test_analysis_vulns_iplist_tool(security_center):
    '''test to get the iplist'''
    vulns = getattr(security_center.analysis, 'vulns')(tool='iplist', pages=2, limit=5)
    assert isinstance(vulns, dict)
    for vuln in vulns:
        check(vulns, vuln, str)


@pytest.mark.vcr()
def test_analysis_vulns_listmailclients_tool(security_center):
    '''
    test analysis vulnerabilities list mail clients tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listmailclients', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listservices_tool(security_center):
    '''
    test analysis vulnerabilities list services tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listservices', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listos_tool(security_center):
    '''
    test analysis vulnerabilities list os tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listos', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listsoftware_tool(security_center):
    '''
    test analysis vulnerabilities list software tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listsoftware', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listsshservers_tool(security_center):
    '''
    test analysis vulnerabilities list ssh servers tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listsshservers', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listvuln_tool(security_center):
    '''
    test analysis vulnerabilities list vulnerability tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listvuln', pages=2, limit=5)
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
def test_analysis_vulns_listwebclients_tool(security_center):
    '''
    test analysis vulnerabilities list web clients tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listwebclients', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_listwebservers_tool(security_center):
    '''
    test analysis vulnerabilities list web servers tool for success
    '''
    vulns = security_center.analysis.vulns(tool='listwebservers', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'detectionMethod', str)
        check(vuln, 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_sumasset_tool(security_center):
    '''
    test analysis vulnerabilities sum asset tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumasset', pages=2, limit=5)
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
def test_analysis_vulns_sumcce_tool(security_center):
    '''
    test analysis vulnerabilities sum cce tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumcce', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@pytest.mark.vcr()
def test_analysis_vulns_sumclassa_tool(security_center):
    '''
    test analysis vulnerabilities sum class-a tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumclassa', pages=2, limit=5)
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
def test_analysis_vulns_sumclassb_tool(security_center):
    '''
    test analysis vulnerabilities sum class-b tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumclassb', pages=2, limit=5)
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
def test_analysis_vulns_sumclassc_tool(security_center):
    '''
    test analysis vulnerabilities sum class-c tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumclassc', pages=2, limit=5)
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
def test_analysis_vulns_sumcve_tool(security_center):
    '''
    test analysis vulnerabilities sum cve detail tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumcve', pages=2, limit=5)
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
def test_analysis_vulns_sumdnsname_tool(security_center):
    '''
    test analysis vulnerabilities sum dns name tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumdnsname', pages=2, limit=5)
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
def test_analysis_vulns_sumfamily_tool(security_center):
    '''
    test analysis vulnerabilities sum family tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumfamily', pages=2, limit=5)
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
def test_analysis_vulns_sumiavm_tool(security_center):
    '''
    test analysis vulnerabilities sum iavm tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumiavm', pages=2, limit=5)
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
def test_analysis_vulns_sumid_tool(security_center):
    '''
    test analysis vulnerabilities sum id tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumid', pages=2, limit=5)
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
def test_analysis_vulns_sumip_tool(security_center):
    '''
    test analysis vulnerabilities sum ip tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumip', pages=2, limit=5)
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
def test_analysis_vulns_summsbulletin_tool(security_center):
    '''
    test analysis vulnerabilities sum ms bulletin tool for success
    '''
    vulns = security_center.analysis.vulns(tool='summsbulletin', pages=2, limit=5)
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
def test_analysis_vulns_sumport_tool(security_center):
    '''
    test analysis vulnerabilities sum port tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumport', pages=2, limit=5)
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
def test_analysis_vulns_sumprotocol_tool(security_center):
    '''
    test analysis vulnerabilities sum protocol tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumprotocol', pages=2, limit=5)
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
def test_analysis_vulns_sumremediation_tool(security_center):
    '''
    test analysis vulnerabilities sum remediation tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumremediation', pages=2, limit=5)
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
def test_analysis_vulns_sumseverity_tool(security_center):
    '''
    test analysis vulnerabilities sum severity tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumseverity', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)
        check(vuln, 'count', str)
        check(vuln, 'severity', dict)
        check(vuln['severity'], 'description', str)
        check(vuln['severity'], 'id', str)
        check(vuln['severity'], 'name', str)


@pytest.mark.vcr()
def test_analysis_vulns_sum_user_responsibility_tool(security_center):
    '''
    test analysis vulnerabilities sum user responsibility tool for success
    '''
    vulns = security_center.analysis.vulns(tool='sumuserresponsibility', pages=2, limit=5)
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
def test_analysis_vulns_trend_tool(security_center):
    '''
    test analysis vulnerabilities trend tool for success
    '''
    vulns = security_center.analysis.vulns(tool='trend', pages=2, limit=5)
    for vuln in vulns:
        assert isinstance(vuln, dict)


@pytest.mark.vcr()
def test_analysis_vulns_vulndetails_tool(security_center):
    '''
    test analysis vulnerabilities 'vulnerability details' tool for success
    '''
    vulns = security_center.analysis.vulns(tool='vulndetails', pages=2, limit=5)
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
def test_analysis_vulns_vulnipdetail_tool(security_center):
    '''
    test analysis vulnerabilities 'vulnerability ip detail' tool for success
    '''
    vulns = security_center.analysis.vulns(tool='vulnipdetail', pages=2, limit=5)
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
def test_analysis_vulns_vulnipsummary_tool(security_center):
    '''
    test analysis vulnerabilities 'vulnerability ip summary' tool for success
    '''
    vulns = security_center.analysis.vulns(tool='vulnipsummary', pages=2, limit=5)
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
def test_analysis_console_logs(security_center):
    '''
    test analysis console logs for success
    '''
    logs = security_center.analysis.console(pages=2, limit=5)
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
def test_analysis_mobile_listvuln(security_center):
    '''
    test analysis mobile list vulnerability for success
    '''
    vulns = security_center.analysis.mobile(tool='listvuln', pages=2, limit=5)
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
def test_analysis_mobile_sumdeviceid(security_center):
    '''
    test analysis mobile sum device id for success
    '''
    vulns = security_center.analysis.mobile(tool='sumdeviceid', pages=2, limit=5)
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
def test_analysis_mobile_summdmuser(security_center):
    '''
    test analysis mobile sum mdm user for success
    '''
    vulns = security_center.analysis.mobile(tool='summdmuser', pages=2, limit=5)
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
def test_analysis_mobile_summodel(security_center):
    '''
    test analysis mobile sum model for success
    '''
    vulns = security_center.analysis.mobile(tool='summodel', pages=2, limit=5)
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
def test_analysis_mobile_sumoscpe(security_center):
    '''
    test analysis mobile sum oscpe for success
    '''
    vulns = security_center.analysis.mobile(tool='sumoscpe', pages=2, limit=5)
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
def test_analysis_mobile_sumpluginid(security_center):
    '''
    test analysis mobile sum plugin id for success
    '''
    vulns = security_center.analysis.mobile(tool='sumpluginid', pages=2, limit=5)
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
def test_analysis_mobile_vulndetails(security_center):
    '''
    test analysis mobile vulnerability details for success
    '''
    vulns = security_center.analysis.mobile(pages=2, limit=5)
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
def test_analysis_events_listdata(security_center):
    '''
    test analysis events list data for success
    '''
    events = security_center.analysis.events(tool='listdata', pages=2, limit=5)
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
def test_analysis_events_sumasset(security_center):
    '''
    test analysis events sum asset for success
    '''
    events = security_center.analysis.events(tool='sumasset', pages=2, limit=5)
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
def test_analysis_events_sumclassa(security_center):
    '''
    test analysis events sum class-a for success
    '''
    events = security_center.analysis.events(tool='sumclassa', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-a', str)
        check(event, 'count', str)


@pytest.mark.vcr()
def test_analysis_events_sumclassb(security_center):
    '''
    test analysis events sum class-b for success
    '''
    events = security_center.analysis.events(tool='sumclassb', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-b', str)
        check(event, 'count', str)


@pytest.mark.vcr()
def test_analysis_events_sumclassc(security_center):
    '''
    test analysis events sum class-c for success
    '''
    events = security_center.analysis.events(tool='sumclassc', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'class-c', str)
        check(event, 'count', str)


@pytest.mark.vcr()
def test_analysis_events_sumconns(security_center):
    '''
    test analysis events sum conns for success
    '''
    events = security_center.analysis.events(tool='sumconns', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'destination ip', str)
        check(event, 'source ip', str)


@pytest.mark.vcr()
def test_analysis_events_sumdate(security_center):
    '''
    test analysis events sum date for success
    '''
    events = security_center.analysis.events(tool='sumdate', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'date', str)
        check(event, 'time block start', str)
        check(event, 'time block stop', str)


@pytest.mark.vcr()
def test_analysis_events_sumdstip(security_center):
    '''
    test analysis events sum ds tip for success
    '''
    events = security_center.analysis.events(tool='sumdstip', pages=2, limit=5)
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
def test_analysis_events_sumevent(security_center):
    '''
    test analysis events sum event for success
    '''
    events = security_center.analysis.events(tool='sumevent', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'description', str)
        check(event, 'event', str)
        check(event, 'file', str)


@pytest.mark.vcr()
def test_analysis_events_sumevent2(security_center):
    '''
    test analysis events sum event for success
    '''
    events = security_center.analysis.events(tool='sumevent2', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'description', str)
        check(event, 'event', str)
        check(event, 'file', str)


@pytest.mark.vcr()
def test_analysis_events_sumip(security_center):
    '''
    test analysis events sum ip for success
    '''
    events = security_center.analysis.events(tool='sumip', pages=2, limit=5)
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
def test_analysis_events_sumport(security_center):
    '''
    test analysis events sum port for success
    '''
    events = security_center.analysis.events(tool='sumport', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'port', str)


@pytest.mark.vcr()
def test_analysis_events_sumprotocol(security_center):
    '''
    test analysis events sum protocol for success
    '''
    events = security_center.analysis.events(tool='sumprotocol', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'protocol', str)


@pytest.mark.vcr()
def test_analysis_events_sumsrcip(security_center):
    '''
    test analysis events sum src ip for success
    '''
    events = security_center.analysis.events(tool='sumsrcip', pages=2, limit=5)
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
def test_analysis_events_sumtime(security_center):
    '''
    test analysis events sum time for success
    '''
    events = security_center.analysis.events(tool='sumtime', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'count', str)
        check(event, 'time block start', str)
        check(event, 'time block stop', str)


@pytest.mark.vcr()
def test_analysis_events_sumtype(security_center):
    '''
    test analysis events sum type for success
    '''
    events = security_center.analysis.events(tool='sumtype', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'type', str)


@pytest.mark.vcr()
def test_analysis_events_sumuser(security_center):
    '''
    test analysis events sum user for success
    '''
    events = security_center.analysis.events(tool='sumuser', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, '24-hour plot', str)
        check(event, 'count', str)
        check(event, 'user', str)


@pytest.mark.vcr()
def test_analysis_events_syslog(security_center):
    '''
    test analysis events sys log for success
    '''
    events = security_center.analysis.events(tool='syslog', pages=2, limit=5)
    for event in events:
        assert isinstance(event, dict)
        check(event, 'message', str)
        check(event, 'sensor', str)
        check(event, 'time', str)
        check(event, 'type', str)
