from tenable.errors import *
from .fixtures import *


def get_vulns(sc, **kw):
    kw['pages'] = 2
    kw['limit'] = 50
    vulns = sc.analysis.vulns(**kw)
    return vulns


def test_vulns_cceipdetail_tool(sc):
    vulns = get_vulns(sc, tool='cceipdetail')
    for v in vulns:
        assert isinstance(v, dict)

def test_vulns_cveipdetail_tool(sc):
    vulns = get_vulns(sc, tool='cveipdetail')
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

def test_vulns_iavmipdetail_tool(sc):
    vulns = get_vulns(sc, tool='iavmipdetail')
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

def test_vulns_iplist_tool(sc):
    vulns = get_vulns(sc, tool='iplist')
    assert isinstance(vulns, dict)
    for i in vulns:
        check(vulns, i, str)

def test_vulns_listmailclients_tool(sc):
    vulns = get_vulns(sc, tool='listmailclients')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

def test_vulns_listservices_tool(sc):
    vulns = get_vulns(sc, tool='listservices')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

def test_vulns_listos_tool(sc):
    vulns = get_vulns(sc, tool='listos')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

def test_vulns_listsoftware_tool(sc):
    vulns = get_vulns(sc, tool='listsoftware')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

def test_vulns_listsshservers_tool(sc):
    vulns = get_vulns(sc, tool='listsshservers')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

def test_vulns_listvuln_tool(sc):
    vulns = get_vulns(sc, tool='listvuln')
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

def test_vulns_listwebclients_tool(sc):
    vulns = get_vulns(sc, tool='listwebclients')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

def test_vulns_listwebservers_tool(sc):
    vulns = get_vulns(sc, tool='listwebservers')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'detectionMethod', str)
        check(v, 'name', str)

@pytest.mark.xfail(raises=ServerError)
def test_vulns_popcount_tool(sc):
    vulns = get_vulns(sc, tool='popcount')
    for v in vulns:
        assert isinstance(v, dict)

def test_vulns_sumasset_tool(sc):
    vulns = get_vulns(sc, tool='sumasset')
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

def test_vulns_sumcce_tool(sc):
    vulns = get_vulns(sc, tool='sumcce')
    for v in vulns:
        assert isinstance(v, dict)

def test_vulns_sumclassa_tool(sc):
    vulns = get_vulns(sc, tool='sumclassa')
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

def test_vulns_sumclassb_tool(sc):
    vulns = get_vulns(sc, tool='sumclassb')
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

def test_vulns_sumclassc_tool(sc):
    vulns = get_vulns(sc, tool='sumclassc')
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

def test_vulns_sumcve_tool(sc):
    vulns = get_vulns(sc, tool='sumcve')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'cveID', str)
        check(v, 'total', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'hostTotal', str)

def test_vulns_sumdnsname_tool(sc):
    vulns = get_vulns(sc, tool='sumdnsname')
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

def test_vulns_sumfamily_tool(sc):
    vulns = get_vulns(sc, tool='sumfamily')
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

def test_vulns_sumiavm_tool(sc):
    vulns = get_vulns(sc, tool='sumiavm')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'iavmID', str)
        check(v, 'total', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'hostTotal', str)

def test_vulns_sumid_tool(sc):
    vulns = get_vulns(sc, tool='sumid')
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

def test_vulns_sumip_tool(sc):
    vulns = get_vulns(sc, tool='sumip')
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

def test_vulns_summsbulletin_tool(sc):
    vulns = get_vulns(sc, tool='summsbulletin')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'msbulletinID', str)
        check(v, 'total', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)
        check(v, 'hostTotal', str)

def test_vulns_sumport_tool(sc):
    vulns = get_vulns(sc, tool='sumport')
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

def test_vulns_sumprotocol_tool(sc):
    vulns = get_vulns(sc, tool='sumprotocol')
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

def test_vulns_sumremediation_tool(sc):
    vulns = get_vulns(sc, tool='sumremediation')
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

def test_vulns_sumseverity_tool(sc):
    vulns = get_vulns(sc, tool='sumseverity')
    for v in vulns:
        assert isinstance(v, dict)
        check(v, 'count', str)
        check(v, 'severity', dict)
        check(v['severity'], 'description', str)
        check(v['severity'], 'id', str)
        check(v['severity'], 'name', str)

def test_vulns_sumuserresponsibility_tool(sc):
    vulns = get_vulns(sc, tool='sumuserresponsibility')
    for v in vulns:
        assert isinstance(v, dict)

def test_vulns_sumuserresponsibility_tool(sc):
    vulns = get_vulns(sc, tool='sumuserresponsibility')
    for v in vulns:
        assert isinstance(v, dict)

def test_vulns_trend_tool(sc):
    vulns = get_vulns(sc, tool='trend')
    for v in vulns:
        assert isinstance(v, dict)

def test_vulns_vulndetails_tool(sc):
    vulns = get_vulns(sc, tool='vulndetails')
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

def test_vulns_vulnipdetail_tool(sc):
    vulns = get_vulns(sc, tool='vulnipdetail')
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

def test_vulns_vulnipsummary_tool(sc):
    vulns = get_vulns(sc, tool='vulnipsummary')
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

def test_console_logs(sc):
    logs = sc.analysis.console(limit=50, pages=2)
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

