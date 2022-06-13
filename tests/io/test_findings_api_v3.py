'''
Test Explore -> Findings V3 API endpoints
'''
import pytest
from requests import Response

from tenable.io.v3.base.iterators.explore_iterator import CSVChunkIterator, SearchIterator


@pytest.mark.vcr()
def test_findings_v3_search_was(api):
    '''
    Test the search endpoint of web applications findings
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
