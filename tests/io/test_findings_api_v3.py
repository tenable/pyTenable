'''
Test Explore -> Findings V3 API endpoints
'''
import pytest
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import CSVChunkIterator, SearchIterator


@pytest.mark.vcr()
def test_findings_v3_search_was(api):
    '''
    Test the search endpoint of web applications - findings
    '''

    fields = ['finding_id', 'severity', 'state', 'last_observed']
    sort = [("last_observed", "desc")]
    filter = ('and', ('severity', 'eq', [3]),
              ('state', 'eq', ['ACTIVE']))

    iterator = api.v3.explore.findings.search_webapp(
        fields=fields, filter=filter, sort=sort, limit=200,
    )
    assert isinstance(iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Web Applications Findings"

    iterator = api.v3.explore.findings.search_webapp(
        fields=fields, filter=filter, return_csv=True, sort=sort, limit=200,
    )
    assert isinstance(iterator, CSVChunkIterator), "CSV chunk iterator is not returned in response of " \
                                                   "Explore -> Web Applications Findings with return_csv flag enabled"

    resp = api.v3.explore.findings.search_webapp(
        fields=fields, filter=filter, return_resp=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response is not returned in response of " \
                                       "Explore -> Web Applications Findings with return_resp flag enabled"

    resp = api.v3.explore.findings.search_webapp(
        fields=fields, filter=filter, return_resp=True, return_csv=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response object (CSV format) is not returned in response of " \
                                       "Explore -> Web Applications Findings with return_resp & return_csv flag enabled"


@pytest.mark.vcr()
def test_findings_v3_search_cloud_resource(api):
    '''
    Test the search endpoint of cloud resource - findings

    '''

    fields = ['finding_id', 'last_found_time', 'risk_factor_num', 'asset.name', 'state']
    sort = [("state", "desc")]
    filter = ('and', ('risk_factor_num', 'eq', 3), ('state', 'eq', ['ACTIVE']))

    iterator = api.v3.explore.findings.search_cloud_resource(
        fields=fields, filter=filter, sort=sort, limit=200,
    )
    assert isinstance(iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Cloud Findings"

    iterator = api.v3.explore.findings.search_cloud_resource(
        fields=fields, filter=filter, return_csv=True, sort=sort, limit=200,
    )
    assert isinstance(iterator, CSVChunkIterator), "CSV chunk iterator is not returned in response of " \
                                                   "Explore -> Cloud Findings with return_csv flag enabled"

    resp = api.v3.explore.findings.search_cloud_resource(
        fields=fields, filter=filter, return_resp=True, return_csv=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response object (CSV format) is not returned in response of " \
                                       "Explore -> Cloud Findings with return_resp & return_csv flag enabled"

    resp = api.v3.explore.findings.search_cloud_resource(
        fields=fields, filter=filter, return_resp=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response is not returned in response of " \
                                       "Explore -> Cloud Findings with return_resp flag enabled"


@pytest.mark.vcr()
def test_findings_v3_search_host_audit(api):
    '''
    Test the search endpoint of host audit - findings
    '''
    fields = ["asset_id", "asset_name", "audit_name", "compliance_result", "plugin_id", 'state', 'last_observed']
    sort = [("state", "desc")]
    filter = ('and', ('asset_name', 'eq', ['ubuntu2004serv.target.tenablesecurity.com']),
              ('compliance_result', 'eq', ['WARNING']), ('state', 'eq', ['NEW']))

    iterator = api.v3.explore.findings.search_host_audit(
        fields=fields, filter=filter, sort=sort, limit=200,
    )
    assert isinstance(iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Host Audit Findings"

    iterator = api.v3.explore.findings.search_host_audit(
        fields=fields, filter=filter, return_csv=True, sort=sort, limit=200,
    )
    assert isinstance(iterator, CSVChunkIterator), "CSV chunk iterator is not returned in response of " \
                                                   "Explore -> Host Audit Findings with return_csv flag enabled"

    resp = api.v3.explore.findings.search_host_audit(
        fields=fields, filter=filter, return_resp=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response is not returned in response of " \
                                       "Explore -> Host Audit Findings with return_resp flag enabled"

    resp = api.v3.explore.findings.search_host_audit(
        fields=fields, filter=filter, return_resp=True, return_csv=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response object (CSV format) is not returned in response of " \
                                       "Explore -> Host Audit Findings with return_resp & return_csv flag enabled"


@pytest.mark.vcr()
def test_findings_v3_search_host(api):
    '''
    Test the search endpoint of host - findings
    '''
    fields = ['asset.name', 'asset.display_ipv4_address', 'severity', 'definition.family', 'last_seen']
    sort = [("severity", "desc")]
    filter = ('and', ('last_seen', 'gt', '-P80D'),
              ('severity', 'eq', [1, 2, 3, 4]), ('state', 'eq', ["ACTIVE", "RESURFACED", "NEW"]))

    iterator = api.v3.explore.findings.search_host(
        fields=fields, filter=filter, sort=sort, limit=200,
    )
    assert isinstance(iterator, SearchIterator), \
        "Iterator is not returned in response of Explore -> Host Findings"

    iterator = api.v3.explore.findings.search_host(
        fields=fields, filter=filter, return_csv=True, sort=sort, limit=200,
    )
    assert isinstance(iterator, CSVChunkIterator), "CSV chunk iterator is not returned in response of " \
                                                   "Explore -> Host Findings with return_csv flag enabled"

    resp = api.v3.explore.findings.search_host(
        fields=fields, filter=filter, return_resp=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response is not returned in response of " \
                                       "Explore -> Host Findings with return_resp flag enabled"

    resp = api.v3.explore.findings.search_host(
        fields=fields, filter=filter, return_resp=True, return_csv=True, sort=sort, limit=200
    )
    assert isinstance(resp, Response), "Response object (CSV format) is not returned in response of " \
                                       "Explore -> Host Findings with return_resp & return_csv flag enabled"
