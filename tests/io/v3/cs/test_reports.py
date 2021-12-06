'''
Testing the Groups endpoints
'''
import responses

BASE_URL = 'https://cloud.tenable.com'
REPORTS_BASE_URL = f'{BASE_URL}/container-security/api/v3/reports'
REPOSITORY = 'centos'
IMAGE = '7'
TAG = 'latest'
SAMPLE_REPORT = {}


@responses.activate
def test_get_report(api):
    responses.add(
        responses.GET,
        f'{REPORTS_BASE_URL}/{REPOSITORY}/{IMAGE}/{TAG}',
        json=SAMPLE_REPORT
    )

    resp = api.v3.cs.reports.report(REPOSITORY, IMAGE, TAG)
    assert resp == SAMPLE_REPORT
