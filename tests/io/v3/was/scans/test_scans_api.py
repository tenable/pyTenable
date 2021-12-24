from pathlib import Path

import pytest
import responses

WAS_SCANS_BASE_URL = 'https://cloud.tenable.com/api/v3/was'
SAMPLE_SCAN_ID = 'cade336b-29fb-4188-b42a-04d8f95d7de6'
SAMPLE_CONFIG_ID = '36adf672-0b08-43b5-a15f-6b32044f6b1f'
SAMPLE_SCAN = {
    'id': SAMPLE_SCAN_ID,
    'user_id': 'a444d3ca-ea68-40a8-85cc-2e33b76106ab',
    'config_id': SAMPLE_CONFIG_ID,
    'asset_id': '638311e5-a0d3-41d4-8afa-156f3b074b14',
    'target': 'http://target1.pubtarg.tenablesecurity.com',
    'application_uri': 'http://target1.pubtarg.tenablesecurity.com',
    'created_at': '2020-01-02T21:53:55.428Z',
    'updated_at': '2020-01-02T21:54:28.156Z',
    'started_at': None,
    'finalized_at': None,
    'requested_action': 'start',
    'status': 'stopping',
    'metadata': {
        'estimate_crawl_percent_complete': 100,
        'queued_urls': 0,
        'scan_status': 'stopping',
        'crawled_urls': 1,
        'queued_pages': 0,
        'audited_pages': 1,
        'request_count': 357,
        'response_time': 0
    },
    'scanner': None,
    'template_name': 'scan',
    'config_metadata': {
        'template': {
            'name': 'scan',
            'description':
                'A scan that checks a web application for vulnerabilities.',
            'template_id': 'b223f18e-5a94-4e02-b560-77a4a8246cd3'
        }
    }
}


@responses.activate
def test_delete(api):
    '''
    Test was scans delete method
    '''
    responses.add(
        responses.DELETE,
        f'{WAS_SCANS_BASE_URL}/scans/{SAMPLE_SCAN_ID}'
    )
    result = api.v3.was.scans.delete(SAMPLE_SCAN_ID)
    assert result is None


@responses.activate
def test_details(api):
    '''
    Test was scans details method
    '''
    responses.add(
        responses.GET,
        f'{WAS_SCANS_BASE_URL}/scans/{SAMPLE_SCAN_ID}',
        json=SAMPLE_SCAN
    )
    result = api.v3.was.scans.details(SAMPLE_SCAN_ID)
    assert isinstance(result, dict)
    assert result == SAMPLE_SCAN


@responses.activate
def test_download(api):
    sample_report = Path(__file__).parent / Path('sample_report.csv')

    with open(sample_report, 'rb') as report:
        file_contents = report.read()

    responses.add(
        responses.GET,
        f'{WAS_SCANS_BASE_URL}/scans/{SAMPLE_SCAN_ID}/report',
        body=file_contents
    )

    received_report = Path(__file__).parent / Path('received_report.csv')
    with open(received_report, 'wb') as report:
        api.v3.was.scans.download(SAMPLE_SCAN_ID, 'text/csv', report)

    with open(received_report, 'rb') as report:
        assert report.read() == file_contents

    received_report.unlink()


@responses.activate
def test_export(api):
    responses.add(
        responses.PUT,
        f'{WAS_SCANS_BASE_URL}/scans/{SAMPLE_SCAN_ID}/report'
    )
    result = api.v3.was.scans.export(SAMPLE_SCAN_ID)
    assert result is None


@responses.activate
def test_launch(api):
    '''
    Test was scans update status method
    '''
    responses.add(
        responses.POST,
        f'{WAS_SCANS_BASE_URL}/configs/{SAMPLE_CONFIG_ID}/scans',
        json={'id': SAMPLE_SCAN_ID}
    )
    result = api.v3.was.scans.launch(SAMPLE_CONFIG_ID)
    assert result == SAMPLE_SCAN_ID


@responses.activate
def test_notes(api):
    with pytest.raises(NotImplementedError):
        api.v3.was.scans.notes(SAMPLE_SCAN_ID)


@responses.activate
def test_search(api):
    with pytest.raises(NotImplementedError):
        api.v3.was.scans.search(SAMPLE_SCAN_ID)


@responses.activate
def test_update_status(api):
    '''
    Test was scans update status method
    '''
    responses.add(
        responses.PATCH,
        f'{WAS_SCANS_BASE_URL}/scans/{SAMPLE_SCAN_ID}'
    )
    result = api.v3.was.scans.update_status(SAMPLE_SCAN_ID, 'stop')
    assert result is None


@responses.activate
def test_search_vulnerabilities(api):
    with pytest.raises(NotImplementedError):
        api.v3.was.scans.search_vulnerabilities(SAMPLE_SCAN_ID)
