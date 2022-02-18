from pathlib import Path

import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.was_iterator import (CSVChunkIterator,
                                                       SearchIterator)

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
    api_response = {
        'pagination': {
            'total': 1,
            'offset': 0,
            'limit': 200,
            'sort': [
                {
                    'name': 'created_at',
                    'order': 'desc'
                }
            ]
        },
        'items': [
            {
                'scan_note_id': '79c83486-d589-4568-9bdb-5cdccc315ccb',
                'scan_id': 'e51094c7-ebe2-4296-a978-ba2563d0cb66',
                'created_at': '2020-04-07T00:17:37Z',
                'severity': 'high',
                'title': 'Authentication Failed',
                'message': 'The scanner was unable to authenticate to \
                    the web application using the given options.'
            }
        ]
    }
    QP = '?limit=200&offset=0'
    responses.add(
        responses.POST,
        f'{WAS_SCANS_BASE_URL}/scans/{SAMPLE_SCAN_ID}/notes{QP}',
        json=api_response
    )

    iterator = api.v3.was.scans.notes(SAMPLE_SCAN_ID, limit=200)
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.was.scans.notes(SAMPLE_SCAN_ID,
                                      return_csv=True, limit=200
                                      )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.was.scans.notes(SAMPLE_SCAN_ID,
                                  return_resp=True, limit=200
                                  )
    assert isinstance(resp, Response)


@responses.activate
def test_search(api):
    fields = [
        'scan_id',
        'user_id',
        'config_id',
        'asset_id',
        'target',
        'application_uri',
        'created_at',
        'updated_at',
        'started_at',
        'finalized_at',
        'requested_action',
        'status',
        'metadata',
        'scanner',
        'template_name'
    ]
    sort = [('created_at', 'desc')]
    filters = {
        'and': [{
                'property': 'scan_id',
                'operator': 'eq',
                'value': ['0d94f5b4-f811-44cb-802a-7f1c600818c3',
                          '6f1ed550-7894-40b3-a6ea-3be06f9338a4']
                },
                {
                'property': 'user_id',
                'operator': 'eq',
                'value': '01c924ee-e6ab-4d55-b283-dffba6dcce4c'
                }
                ]
    }

    payload = {
        'fields': fields,
        'filter': filters,
    }

    api_response = {
        'pagination': {
            'total': 2,
            'offset': 0,
            'limit': 200,
            'sort': [{
                'name': 'created_at',
                'order': 'desc'
            }]
        },
        'items': [{
            'scan_id': '0d94f5b4-f811-44cb-802a-7f1c600818c3',
            'user_id': '01c924ee-e6ab-4d55-b283-dffba6dcce4c',
            'config_id': '988cd296-58b0-419e-bd43-0d884080daf6',
            'asset_id': 'f8598420-1e33-4aed-abd0-56d114e96d3e',
            'target': 'http://example.com/',
            'created_at': '2020-12-07T20:00:14.319827Z',
            'updated_at': '2020-12-07T20:01:19.815217Z',
            'started_at': '2020-12-07T20:01:00.386897Z',
            'finalized_at': '2020-12-07T20:01:19.808199Z',
            'requested_action': 'start',
            'status': 'completed',
            'metadata': {
                'found_urls': 1,
                'queued_urls': 0,
                'scan_status': 'running',
                'audited_urls': 1,
                'queued_pages': 0,
                'audited_pages': 1,
                'request_count': 163,
                'response_time': 0
            },
            'scanner': {
                'group_name': 'US Cloud Scanner'
            },
            'template_name': 'config_audit'
        },
            {
                'scan_id': '6f1ed550-7894-40b3-a6ea-3be06f9338a4',
                'user_id': '01c924ee-e6ab-4d55-b283-dffba6dcce4c',
                'config_id': '988cd296-58b0-419e-bd43-0d884080daf6',
                'asset_id': 'f8598420-1e33-4aed-abd0-56d114e96d3e',
                'target': 'http://example.com/',
                'created_at': '2020-12-04T20:00:20.058359Z',
                'updated_at': '2020-12-04T20:01:34.843822Z',
                'started_at': '2020-12-04T20:01:15.837083Z',
                'finalized_at': '2020-12-04T20:01:34.831731Z',
                'requested_action': 'start',
                'status': 'completed',
                'metadata': {
                    'found_urls': 1,
                    'queued_urls': 0,
                    'scan_status': 'running',
                    'audited_urls': 1,
                    'queued_pages': 0,
                    'audited_pages': 1,
                    'request_count': 162,
                    'response_time': 0
                },
                'scanner': {
                    'group_name': 'US Cloud Scanner'
                },
                'template_name': 'config_audit'
        }
        ]
    }
    QP = '?limit=200&sort=name&sort=order&offset=0'
    responses.add(
        responses.POST,
        f'{WAS_SCANS_BASE_URL}/configs/{SAMPLE_CONFIG_ID}/scans/search{QP}',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.was.scans.search(SAMPLE_CONFIG_ID,
                                       fields=fields,
                                       limit=200,
                                       sort=sort,
                                       filter=filters)
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.was.scans.search(SAMPLE_CONFIG_ID,
                                       fields=fields,
                                       return_csv=True,
                                       sort=sort,
                                       limit=200,
                                       filter=filters)
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.was.scans.search(SAMPLE_CONFIG_ID,
                                   fields=fields,
                                   return_resp=True,
                                   limit=200,
                                   sort=sort,
                                   filter=filters)
    assert isinstance(resp, Response)


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
    fields = [
        'vuln_id',
        'scan_id',
        'plugin_id',
        'created_at',
        'uri',
        'details',
        'attachments'
    ]
    sort = [('created_at', 'desc')]
    filters = {
        'and': [{
                'property': 'vuln_id',
                'operator': 'eq',
                'value': ['a1dc9d88-44de-4f5c-9258-3dbb02baa010',
                          '3072f8d9-a0c2-443f-bca8-b47e63ebaa80'
                          ]
                },
                {
                'property': 'scan_id',
                'operator': 'eq',
                'value': '7f3428c5-0f5a-4812-a728-fffbcbf7c132'
                }
                ]
    }

    payload = {
        'fields': fields,
        'filter': filters,
    }

    api_response = {
        'pagination': {
            'total': 2,
            'offset': 0,
            'limit': 200,
            'sort': [{
                'name': 'created_at',
                'order': 'desc'
            }]
        },
        'items': [{
            'vuln_id': '3072f8d9-a0c2-443f-bca8-b47e63ebaa80',
            'scan_id': '7f3428c5-0f5a-4812-a728-fffbcbf7c132',
            'plugin_id': 98009,
            'created_at': '2020-02-05T23:25:31Z',
            'uri': 'http://192.0.2.119',
            'is_page': False,
            'details': {
                'input_name': None,
                'input_type': None,
                'output': 'The scan has discovered 23 distinct URLs',
                'proof': None,
                'payload': None,
                'selector': None,
                'selector_url': None,
                'signature': None,
                'request': None,
                'response': None
            },
            'attachments': [{
                'attachment_id': 'b13a9fb5-cb0d-47d8-a6c1-063fbe6f8250',
                'created_at': '2020-02-05T23:25:33.740Z',
                'attachment_name': 'sitemap.csv',
                'md5': 'md5:b2e06491f801f7f5b5f229bbf6efd7e9',
                'file_type': 'text/plain',
                'size': 0
            }]
        },
            {
                'vuln_id': 'a1dc9d88-44de-4f5c-9258-3dbb02baa010',
                'scan_id': '7f3428c5-0f5a-4812-a728-fffbcbf7c132',
                'plugin_id': 98000,
                'created_at': '2020-01-01T23:25:31Z',
                'uri': 'http://192.0.2.119',
                'is_page': False,
                'details': {
                    'input_name': None,
                    'input_type': None,
                    'output': '\nEngine Version 0.41.0',
                    'proof': None,
                    'payload': None,
                    'selector': None,
                    'selector_url': None,
                    'signature': None,
                    'request': None,
                    'response': None
                },
                'attachments': []
        }
        ]
    }
    URL = 'vulnerabilities/search?limit=200&sort=name&sort=order&offset=0'
    responses.add(
        responses.POST,
        f'{WAS_SCANS_BASE_URL}/scans/{SAMPLE_SCAN_ID}/{URL}',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.was.scans.search_vulnerabilities(SAMPLE_SCAN_ID,
                                                       fields=fields,
                                                       limit=200,
                                                       sort=sort,
                                                       filter=filters
                                                       )
    assert isinstance(iterator, SearchIterator)
    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.was.scans.search_vulnerabilities(SAMPLE_SCAN_ID,
                                                       fields=fields,
                                                       return_csv=True,
                                                       sort=sort,
                                                       limit=200,
                                                       filter=filters
                                                       )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.was.scans.search_vulnerabilities(SAMPLE_SCAN_ID,
                                                   fields=fields,
                                                   return_resp=True,
                                                   limit=200,
                                                   sort=sort,
                                                   filter=filters
                                                   )
    assert isinstance(resp, Response)
