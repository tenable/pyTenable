from tenable.errors import *
from ..checker import check, single
import pytest

def test_analysis_asset_excpansion_simple(sc):
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



@pytest.mark.vcr()
def test_analysis_vulns_cceipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='cceipdetail', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)

@pytest.mark.vcr()
def test_analysis_vulns_cveipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='cveipdetail', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'cveID', str)
        check(v, 'total', str)
        check(v, 'hosts', list)
        i = v['hosts'][0]
        check(i, 'iplist', list)
        check(i, 'repositoryID', str)
        for j in i['iplist']:
            check(j, 'ip', str)
            check(j, 'netbiosName', str)
            check(j, 'dnsName', str)
            check(j, 'uuid', str)
            check(j, 'macAddress', str)

@pytest.mark.vcr()
def test_analysis_vulns_iavmipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='iavmipdetail', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'iavmID', str)
        check(v, 'total', str)
        check(v, 'hosts', list)
        i = v['hosts'][0]
        check(i, 'iplist', list)
        check(i, 'repositoryID', str)
        for j in i['iplist']:
            check(j, 'ip', str)
            check(j, 'netbiosName', str)
            check(j, 'dnsName', str)
            check(j, 'uuid', str)
            check(j, 'macAddress', str)

@pytest.mark.vcr()
def test_analysis_vulns_iplist_tool(sc):
    vulns = sc.analysis.vulns(tool='iplist', pages=2, limit=5)
    assert isinstance(vulns, dict)
    for i in vulns:
        check(vulns, i, str)

@pytest.mark.vcr()
def test_analysis_vulns_listmailclients_tool(sc):
    vulns = sc.analysis.vulns(tool='listmailclients', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_listservices_tool(sc):
    vulns = sc.analysis.vulns(tool='listservices', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_listos_tool(sc):
    vulns = sc.analysis.vulns(tool='listos', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_listsoftware_tool(sc):
    vulns = sc.analysis.vulns(tool='listsoftware', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_listsshservers_tool(sc):
    vulns = sc.analysis.vulns(tool='listsshservers', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_listvuln_tool(sc):
    vulns = sc.analysis.vulns(tool='listvuln', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'macAddress', str)
        check(v, 'uniqueness', str)
        check(v, 'protocol', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'family', dict)
        check(v['family'], 'type', str)
        check(v['family'], 'id', str)
        check(v['family'], 'name', str)
        check(v, 'pluginInfo', str)
        check(v, 'ip', str)
        check(v, 'netbiosName', str)
        check(v, 'name', str)
        check(v, 'repository', dict)
        check(v['repository'], 'description', str)
        check(v['repository'], 'dataFormat', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)
        check(v, 'pluginID', str)
        check(v, 'dnsName', str)
        check(v, 'port', str)
        check(v, 'uuid', str)

@pytest.mark.vcr()
def test_analysis_vulns_listwebclients_tool(sc):
    vulns = sc.analysis.vulns(tool='listwebclients', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_listwebservers_tool(sc):
    vulns = sc.analysis.vulns(tool='listwebservers', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumasset_tool(sc):
    vulns = sc.analysis.vulns(tool='sumasset', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)
        check(v, 'total', str)
        check(v, 'score', str)
        check(v, 'asset', dict)
        check(v['asset'], 'status', str)
        check(v['asset'], 'description', str)
        check(v['asset'], 'type', str)
        check(v['asset'], 'id', str)
        check(v['asset'], 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumcce_tool(sc):
    vulns = sc.analysis.vulns(tool='sumcce', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)

@pytest.mark.vcr()
def test_analysis_vulns_sumclassa_tool(sc):
    vulns = sc.analysis.vulns(tool='sumclassa', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)
        check(v, 'total', str)
        check(v, 'score', str)
        check(v, 'ip', str)
        check(v, 'repository', dict)
        check(v['repository'], 'dataFormat', str)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumclassb_tool(sc):
    vulns = sc.analysis.vulns(tool='sumclassb', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)
        check(v, 'total', str)
        check(v, 'score', str)
        check(v, 'ip', str)
        check(v, 'repository', dict)
        check(v['repository'], 'dataFormat', str)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumclassc_tool(sc):
    vulns = sc.analysis.vulns(tool='sumclassc', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)
        check(v, 'total', str)
        check(v, 'score', str)
        check(v, 'ip', str)
        check(v, 'repository', dict)
        check(v['repository'], 'dataFormat', str)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumcve_tool(sc):
    vulns = sc.analysis.vulns(tool='sumcve', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'cveID', str)
        check(v, 'total', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'hostTotal', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumdnsname_tool(sc):
    vulns = sc.analysis.vulns(tool='sumdnsname', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'dnsName', str)
        check(v, 'score', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)
        check(v, 'repository', dict)
        check(v['repository'], 'dataFormat', str)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumfamily_tool(sc):
    vulns = sc.analysis.vulns(tool='sumfamily', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'family', dict)
        check(v['family'], 'type', str)
        check(v['family'], 'id', str)
        check(v['family'], 'name', str)
        check(v, 'score', str)
        check(v, 'total', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumiavm_tool(sc):
    vulns = sc.analysis.vulns(tool='sumiavm', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'iavmID', str)
        check(v, 'total', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'hostTotal', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumid_tool(sc):
    vulns = sc.analysis.vulns(tool='sumid', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'family', dict)
        check(v['family'], 'type', str)
        check(v['family'], 'id', str)
        check(v['family'], 'name', str)
        check(v, 'hostTotal', str)
        check(v, 'pluginID', str)
        check(v, 'total', str)
        check(v, 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumip_tool(sc):
    vulns = sc.analysis.vulns(tool='sumip', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'macAddress', str)
        check(v, 'lastAuthRun', str)
        check(v, 'ip', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)
        check(v, 'total', str)
        check(v, 'mcafeeGUID', str)
        check(v, 'policyName', str)
        check(v, 'uuid', str)
        check(v, 'osCPE', str)
        check(v, 'uniqueness', str)
        check(v, 'score', str)
        check(v, 'dnsName', str)
        check(v, 'lastUnauthRun', str)
        check(v, 'biosGUID', str)
        check(v, 'tpmID', str)
        check(v, 'pluginSet', str)
        check(v, 'netbiosName', str)
        check(v, 'repository', dict)
        check(v['repository'], 'dataFormat', str)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_summsbulletin_tool(sc):
    vulns = sc.analysis.vulns(tool='summsbulletin', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'msbulletinID', str)
        check(v, 'total', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'hostTotal', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumport_tool(sc):
    vulns = sc.analysis.vulns(tool='sumport', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'port', str)
        check(v, 'score', str)
        check(v, 'total', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumprotocol_tool(sc):
    vulns = sc.analysis.vulns(tool='sumprotocol', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'protocol', str)
        check(v, 'score', str)
        check(v, 'total', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumremediation_tool(sc):
    vulns = sc.analysis.vulns(tool='sumremediation', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'hostTotal', str)
        check(v, 'scorePctg', str)
        check(v, 'totalPctg', str)
        check(v, 'msbulletinTotal', str)
        check(v, 'remediationList', str)
        check(v, 'cpe', str)
        check(v, 'cveTotal', str)
        check(v, 'solution', str)
        check(v, 'pluginID', str)
        check(v, 'score', str)
        check(v, 'total', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumseverity_tool(sc):
    vulns = sc.analysis.vulns(tool='sumseverity', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)

@pytest.mark.vcr()
def test_analysis_vulns_sumuserresponsibility_tool(sc):
    vulns = sc.analysis.vulns(tool='sumuserresponsibility', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)

@pytest.mark.vcr()
def test_analysis_vulns_sumuserresponsibility_tool(sc):
    vulns = sc.analysis.vulns(tool='sumuserresponsibility', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'score', str)
        check(v, 'total', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityMedium', str)
        check(v, 'severityLow', str)
        check(v, 'severityInfo', str)
        check(v, 'userList', list)
        for i in v['userList']:
            check(i, 'firstname', str)
            check(i, 'id', str)
            check(i, 'lastname', str)
            check(i, 'status', str)
            check(i, 'username', str)

@pytest.mark.vcr()
def test_analysis_vulns_trend_tool(sc):
    vulns = sc.analysis.vulns(tool='trend', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)

@pytest.mark.vcr()
def test_analysis_vulns_vulndetails_tool(sc):
    vulns = sc.analysis.vulns(tool='vulndetails', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'acceptRisk', str)
        check(v, 'baseScore', str)
        check(v, 'bid', str)
        check(v, 'checkType', str)
        check(v, 'cpe', str)
        check(v, 'cve', str)
        check(v, 'cvssV3BaseScore', str)
        check(v, 'cvssV3TemporalScore', str)
        check(v, 'cvssV3Vector', str)
        check(v, 'cvssVector', str)
        check(v, 'description', str)
        check(v, 'dnsName', str)
        check(v, 'exploitAvailable', str)
        check(v, 'exploitEase', str)
        check(v, 'exploitFrameworks', str)
        check(v, 'family', dict)
        check(v['family'], 'type', str)
        check(v['family'], 'id', str)
        check(v['family'], 'name', str)
        check(v, 'firstSeen', str)
        check(v, 'hasBeenMitigated', str)
        check(v, 'ip', str)
        check(v, 'lastSeen', str)
        check(v, 'macAddress', str)
        check(v, 'netbiosName', str)
        check(v, 'patchPubDate', str)
        check(v, 'pluginID', str)
        check(v, 'pluginInfo', str)
        check(v, 'pluginModDate', str)
        check(v, 'pluginName', str)
        check(v, 'pluginPubDate', str)
        check(v, 'pluginText', str)
        check(v, 'port', str)
        check(v, 'protocol', str)
        check(v, 'recastRisk', str)
        check(v, 'repository', dict)
        check(v['repository'], 'dataFormat', str)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)
        check(v, 'riskFactor', str)
        check(v, 'seeAlso', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'solution', str)
        check(v, 'stigSeverity', str)
        check(v, 'synopsis', str)
        check(v, 'temporalScore', str)
        check(v, 'uniqueness', str)
        check(v, 'uuid', str)
        check(v, 'version', str)
        check(v, 'vulnPubDate', str)
        check(v, 'xref', str)

@pytest.mark.vcr()
def test_analysis_vulns_vulnipdetail_tool(sc):
    vulns = sc.analysis.vulns(tool='vulnipdetail', pages=2, limit=5)
    for v in vulns:
        check(v, 'family', dict)
        check(v['family'], 'type', str)
        check(v['family'], 'id', str)
        check(v['family'], 'name', str)
        check(v, 'hosts', list)
        i = v['hosts'][0]
        check(i, 'iplist', list)
        check(i, 'repository', dict)
        check(i['repository'], 'dataFormat', str)
        check(i['repository'], 'description', str)
        check(i['repository'], 'id', str)
        check(i['repository'], 'name', str)
        for j in i['iplist']:
            check(j, 'ip', str)
            check(j, 'netbiosName', str)
            check(j, 'dnsName', str)
            check(j, 'uuid', str)
            check(j, 'macAddress', str)
        check(v, 'name', str)
        check(v, 'pluginDescription', str)
        check(v, 'pluginID', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'total', str)

@pytest.mark.vcr()
def test_analysis_vulns_vulnipsummary_tool(sc):
    vulns = sc.analysis.vulns(tool='vulnipsummary', pages=2, limit=5)
    for v in vulns:
        check(v, 'family', dict)
        check(v['family'], 'type', str)
        check(v['family'], 'id', str)
        check(v['family'], 'name', str)
        check(v, 'hosts', list)
        i = v['hosts'][0]
        check(i, 'iplist', str)
        check(i, 'repository', dict)
        check(i['repository'], 'dataFormat', str)
        check(i['repository'], 'description', str)
        check(i['repository'], 'id', str)
        check(i['repository'], 'name', str)
        check(v, 'name', str)
        check(v, 'pluginDescription', str)
        check(v, 'pluginID', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'total', str)

@pytest.mark.vcr()
def test_analysis_console_logs(sc):
    logs = sc.analysis.console(pages=2, limit=5)
    for i in logs:
        assert isinstance(i, dict)
        check(i, 'initiator', dict)
        check(i['initiator'], 'username', str)
        check(i['initiator'], 'firstname', str)
        check(i['initiator'], 'lastname', str)
        try:
            check(i['initiator'], 'id', int)
        except AssertionError:
            check(i['initiator'], 'id', str)
        check(i, 'severity', dict)
        check(i['severity'], 'description', str)
        check(i['severity'], 'id', str)
        check(i['severity'], 'name', str)
        check(i, 'rawLog', str)
        check(i, 'module', str)
        check(i, 'date', 'datetime')
        check(i, 'organization', dict)
        check(i['organization'], 'description', str)
        check(i['organization'], 'id', str)
        check(i['organization'], 'name', str)
        check(i, 'message', str)

@pytest.mark.vcr()
def test_analysis_mobile_listvuln(sc):
    vulns = sc.analysis.mobile(tool='listvuln', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'identifier', str)
        check(v, 'pluginID', str)
        check(v, 'pluginName', str)
        check(v, 'repository', dict)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)

@pytest.mark.vcr()
def test_analysis_mobile_sumdeviceid(sc):
    vulns = sc.analysis.mobile(tool='sumdeviceid', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'identifier', str)
        check(v, 'model', str)
        check(v, 'repository', dict)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)
        check(v, 'score', str)
        check(v, 'serial', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityInfo', str)
        check(v, 'severityLow', str)
        check(v, 'severityMedium', str)
        check(v, 'total', str)

@pytest.mark.vcr()
def test_analysis_mobile_summdmuser(sc):
    vulns = sc.analysis.mobile(tool='summdmuser', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'score', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityInfo', str)
        check(v, 'severityLow', str)
        check(v, 'severityMedium', str)
        check(v, 'total', str)
        check(v, 'user', str)

@pytest.mark.vcr()
def test_analysis_mobile_summodel(sc):
    vulns = sc.analysis.mobile(tool='summodel', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'deviceCount', str)
        check(v, 'model', str)
        check(v, 'score', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityInfo', str)
        check(v, 'severityLow', str)
        check(v, 'severityMedium', str)
        check(v, 'total', str)

@pytest.mark.vcr()
def test_analysis_mobile_sumoscpe(sc):
    vulns = sc.analysis.mobile(tool='sumoscpe', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'deviceCount', str)
        check(v, 'osCPE', str)
        check(v, 'score', str)
        check(v, 'severityCritical', str)
        check(v, 'severityHigh', str)
        check(v, 'severityInfo', str)
        check(v, 'severityLow', str)
        check(v, 'severityMedium', str)
        check(v, 'total', str)

@pytest.mark.vcr()
def test_analysis_mobile_sumpluginid(sc):
    vulns = sc.analysis.mobile(tool='sumpluginid', pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'name', str)
        check(v, 'pluginID', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'total', str)

@pytest.mark.vcr()
def test_analysis_mobile_vulndetails(sc):
    vulns = sc.analysis.mobile(pages=2, limit=5)
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'baseScore', str)
        check(v, 'bid', str)
        check(v, 'checkType', str)
        check(v, 'cpe', str)
        check(v, 'cve', str)
        check(v, 'cvssVector', str)
        check(v, 'description', str)
        check(v, 'deviceVersion', str)
        check(v, 'exploitAvailable', str)
        check(v, 'exploitEase', str)
        check(v, 'exploitFrameworks', str)
        check(v, 'identifier', str)
        check(v, 'lastSeen', str)
        check(v, 'mdmType', str)
        check(v, 'model', str)
        check(v, 'osCPE', str)
        check(v, 'patchPubDate', str)
        check(v, 'pluginID', str)
        check(v, 'pluginInfo', str)
        check(v, 'pluginModDate', str)
        check(v, 'pluginName', str)
        check(v, 'pluginOutput', str)
        check(v, 'pluginPubDate', str)
        check(v, 'port', str)
        check(v, 'protocol', str)
        check(v, 'repository', dict)
        check(v['repository'], 'description', str)
        check(v['repository'], 'id', str)
        check(v['repository'], 'name', str)
        check(v, 'riskFactor', str)
        check(v, 'seeAlso', str)
        check(v, 'serial', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'solution', str)
        check(v, 'stigSeverity', str)
        check(v, 'synopsis', str)
        check(v, 'temporalScore', str)
        check(v, 'user', str)
        check(v, 'version', str)
        check(v, 'vulnPubDate', str)
        check(v, 'xref', str)

@pytest.mark.vcr()
def test_analysis_events_listdata(sc):
    events = sc.analysis.events(tool='listdata', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'destination ip', str)
        check(e, 'destination port', str)
        check(e, 'event', str)
        check(e, 'number of vulns', str)
        check(e, 'protocol', str)
        check(e, 'sensor', str)
        check(e, 'source ip', str)
        check(e, 'time', str)
        check(e, 'type', str)
        check(e, 'va/ids', str)

@pytest.mark.vcr()
def test_analysis_events_sumasset(sc):
    events = sc.analysis.events(tool='sumasset', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'asset', dict)
        check(e['asset'], 'description', str)
        check(e['asset'], 'id', str)
        check(e['asset'], 'name', str)
        check(e['asset'], 'status', str)
        check(e['asset'], 'type', str)
        try:
            check(e, 'count', str)
        except AssertionError:
            check(e, 'count', int)

@pytest.mark.vcr()
def test_analysis_events_sumclassa(sc):
    events = sc.analysis.events(tool='sumclassa', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'class-a', str)
        check(e, 'count', str)

@pytest.mark.vcr()
def test_analysis_events_sumclassb(sc):
    events = sc.analysis.events(tool='sumclassb', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'class-b', str)
        check(e, 'count', str)

@pytest.mark.vcr()
def test_analysis_events_sumclassc(sc):
    events = sc.analysis.events(tool='sumclassc', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'class-c', str)
        check(e, 'count', str)

@pytest.mark.vcr()
def test_analysis_events_sumconns(sc):
    events = sc.analysis.events(tool='sumconns', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'count', str)
        check(e, 'destination ip', str)
        check(e, 'source ip', str)

@pytest.mark.vcr()
def test_analysis_events_sumdate(sc):
    events = sc.analysis.events(tool='sumdate', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, '24-hour plot', str)
        check(e, 'count', str)
        check(e, 'date', str)
        check(e, 'time block start', str)
        check(e, 'time block stop', str)

@pytest.mark.vcr()
def test_analysis_events_sumdstip(sc):
    events = sc.analysis.events(tool='sumdstip', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'address', str)
        check(e, 'count', str)
        check(e, 'lce', dict)
        check(e['lce'], 'description', str)
        check(e['lce'], 'id', str)
        check(e['lce'], 'name', str)
        check(e['lce'], 'status', str)

@pytest.mark.vcr()
def test_analysis_events_sumevent(sc):
    events = sc.analysis.events(tool='sumevent', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, '24-hour plot', str)
        check(e, 'count', str)
        check(e, 'description', str)
        check(e, 'event', str)
        check(e, 'file', str)

@pytest.mark.vcr()
def test_analysis_events_sumevent2(sc):
    events = sc.analysis.events(tool='sumevent2', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, '24-hour plot', str)
        check(e, 'count', str)
        check(e, 'description', str)
        check(e, 'event', str)
        check(e, 'file', str)

@pytest.mark.vcr()
def test_analysis_events_sumip(sc):
    events = sc.analysis.events(tool='sumip', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'address', str)
        check(e, 'count', str)
        check(e, 'lce', dict)
        check(e['lce'], 'description', str)
        check(e['lce'], 'id', str)
        check(e['lce'], 'name', str)
        check(e['lce'], 'status', str)

@pytest.mark.vcr()
def test_analysis_events_sumport(sc):
    events = sc.analysis.events(tool='sumport', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'count', str)
        check(e, 'port', str)

@pytest.mark.vcr()
def test_analysis_events_sumprotocol(sc):
    events = sc.analysis.events(tool='sumprotocol', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'count', str)
        check(e, 'protocol', str)

@pytest.mark.vcr()
def test_analysis_events_sumsrcip(sc):
    events = sc.analysis.events(tool='sumsrcip', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'address', str)
        check(e, 'count', str)
        check(e, 'lce', dict)
        check(e['lce'], 'description', str)
        check(e['lce'], 'id', str)
        check(e['lce'], 'name', str)
        check(e['lce'], 'status', str)

@pytest.mark.vcr()
def test_analysis_events_sumtime(sc):
    events = sc.analysis.events(tool='sumtime', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'count', str)
        check(e, 'time block start', str)
        check(e, 'time block stop', str)

@pytest.mark.vcr()
def test_analysis_events_sumtype(sc):
    events = sc.analysis.events(tool='sumtype', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, '24-hour plot', str)
        check(e, 'count', str)
        check(e, 'type', str)

@pytest.mark.vcr()
def test_analysis_events_sumuser(sc):
    events = sc.analysis.events(tool='sumuser', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, '24-hour plot', str)
        check(e, 'count', str)
        check(e, 'user', str)

@pytest.mark.vcr()
def test_analysis_events_syslog(sc):
    events = sc.analysis.events(tool='syslog', pages=2, limit=5)
    for e in events:
        assert isinstance(e, dict)
        check(e, 'message', str)
        check(e, 'sensor', str)
        check(e, 'time', str)
        check(e, 'type', str)
