import pytest
import responses
from responses import matchers

from tenable.io import TenableIO
from tenable.io.was.iterator import WasIterator


@responses.activate
def test_was_export(tvm: TenableIO):
    """
    Basic test to ensure WasIterator is returned and values are returned when the iterator is traversed.
    """
    responses.add(
        responses.POST,
        'https://nourl/was/v2/configs/search',
        json={
            'pagination': {'total': 1, 'offset': 0, 'limit': 200},
            'items': [
                {
                    'target': 'https://github.com/aseemsavio/dogehouse?rel=nofollow,noopener,noreferrer&target=_blank',
                    'config_id': '07695269-03dd-423e-bd7b-5cc5cfc6e922',
                    'owner_id': '894f462b-b55a-4d71-8941-0e42f37ade38',
                    'is_shared': True,
                    'user_permissions': 'configure',
                    'name': 'Aseem_TEST_14',
                    'target_count': 2,
                    'description': 'test',
                    'created_at': '2023-03-21T05:23:29.399922Z',
                    'updated_at': '2023-03-21T05:23:29.399922Z',
                    'schedule': None,
                    'in_trash': False,
                    'imported': False,
                    'template_id': '3e5862a6-e672-4a22-97b8-9301ec3439c8',
                    'last_scan': {
                        'scan_id': '48044403-c6ec-41a2-b7f2-1116035b99c6',
                        'user_id': '894f462b-b55a-4d71-8941-0e42f37ade38',
                        'config_id': '07695269-03dd-423e-bd7b-5cc5cfc6e922',
                        'created_at': '2023-03-23T10:26:43.432587Z',
                        'updated_at': '2023-03-23T10:38:50.802481Z',
                        'started_at': '2023-03-23T10:28:45.027294Z',
                        'finalized_at': '2023-03-23T10:38:50.800838Z',
                        'requested_action': 'start',
                        'status': 'completed',
                        'template_name': 'quick',
                    },
                    'user_template': None,
                }
            ],
        },
        match=[matchers.query_param_matcher({'limit': '200', 'offset': '0'})],
    )
    responses.add(
        responses.POST,
        'https://nourl/was/v2/scans/48044403-c6ec-41a2-b7f2-1116035b99c6/vulnerabilities/by-targets/search',
        json={
            'pagination': {
                'total': 2,
                'offset': 0,
                'limit': 200,
                'sort': [{'name': 'target', 'order': 'desc'}],
            },
            'items': [
                {
                    'target': {
                        'target_id': '37eb2954-5cf5-45ed-944f-41f168481fad',
                        'asset_id': '857619e8-a3dc-4ae8-851e-2056d7acf818',
                        'target_url': 'https://github.com/aseemsavio/dynamo-kt?rel=nofollow,noopener,noreferrer&target=_blank',
                    },
                    'scan': {
                        'scan_id': '009a9d16-ab40-4143-99d8-64a95797d5a8',
                        'created_at': '2023-03-23T10:26:43.432057Z',
                        'started_at': '2023-03-23T10:28:45.017104Z',
                        'status': 'completed',
                        'estimate_percent_complete': None,
                    },
                    'findings': {
                        'finding_count': 4,
                        'info_vulns': 17,
                        'low_vulns': 3,
                        'medium_vulns': 1,
                        'high_vulns': 0,
                        'critical_vulns': 0,
                    },
                }
            ],
        },
        match=[matchers.query_param_matcher({'limit': '200', 'offset': '0'})],
    )
    responses.add(
        responses.POST,
        'https://nourl/was/v2/scans/48044403-c6ec-41a2-b7f2-1116035b99c6/vulnerabilities/by-targets/search',
        json={
            'pagination': {
                'total': 2,
                'offset': 200,
                'limit': 200,
                'sort': [{'name': 'target', 'order': 'desc'}],
            },
            'items': [],
        },
        match=[matchers.query_param_matcher({'limit': '200', 'offset': '200'})],
    )
    responses.add(
        responses.GET,
        'https://nourl/was/v2/scans/009a9d16-ab40-4143-99d8-64a95797d5a8/report',
        json={
            'config': {
                'config_id': '07695269-03dd-423e-bd7b-5cc5cfc6e922',
                'owner_id': '894f462b-b55a-4d71-8941-0e42f37ade38',
                'additional_properties': None,
                'scanner_type': 'cloud',
                'scanner_instance_id': None,
                'name': 'Aseem_TEST_14',
                'description': 'test',
            },
            'scan': {
                'user_id': '894f462b-b55a-4d71-8941-0e42f37ade38',
                'scan_id': '009a9d16-ab40-4143-99d8-64a95797d5a8',
                'status': 'completed',
                'started_at': '2023-03-23T10:28:45.017104+00:00',
                'finalized_at': '2023-03-23T10:38:50.766253+00:00',
                'asset_id': '857619e8-a3dc-4ae8-851e-2056d7acf818',
                'target': 'https://github.com/aseemsavio/dynamo-kt?rel=nofollow,noopener,noreferrer&target=_blank',
                'created_at': '2023-03-23T10:26:43.432057+00:00',
            },
            'findings': [
                {
                    'plugin_publication_date': '2017-03-31T00:00:00+00:00',
                    'plugin_modification_date': '2017-03-31T00:00:00+00:00',
                    'plugin_id': 98000,
                    'cvssv3': None,
                    'cvssv3_vector': None,
                    'cvss': None,
                    'cvss_vector': None,
                    'risk_factor': 'info',
                    'uri': 'https://github.com/aseemsavio/dynamo-kt?rel=nofollow,noopener,noreferrer&target=_blank',
                    'name': 'Scan Information',
                    'family': 'General',
                    'synopsis': 'Scan Information',
                    'description': 'Provides scan information and statistics of plugins run.',
                    'solution': None,
                    'input_name': None,
                    'input_type': None,
                    'proof': None,
                    'request_headers': None,
                    'response_headers': None,
                    'payload': None,
                    'output': '\nEngine Version      1.55.5-899\nPlugins Version     202303221333\nScan ID             009a9d16-ab40-4143-99d8-64a95797d5a',
                }
            ],
        },
    )
    findings_iterator = tvm.was.export(
        and_filter=[
            ('scans_started_at', 'gte', '2023/03/23'),
            ('scans_status', 'contains', ['completed']),
        ]
    )

    findings = [finding for finding in findings_iterator]

    assert isinstance(findings_iterator, WasIterator)
    assert len(findings) > 0


@responses.activate
def test_ensure_iterator_does_not_break_on_no_data_found(tvm: TenableIO):
    """
    Test to ensure iterator doesn't break on no data found
    """
    responses.add(
        responses.POST,
        'https://nourl/was/v2/configs/search',
        json={
            'pagination': {
                'total': 0,
                'offset': 0,
                'limit': 200,
                'sort': [{'name': 'configs.updated_at', 'order': 'desc'}],
            },
            'items': [],
        },
        match=[matchers.query_param_matcher({'limit': '200', 'offset': '0'})],
    )
    findings_iterator = tvm.was.export(
        and_filter=[
            ('scans_started_at', 'gte', '2100/03/23'),
            ('scans_status', 'contains', ['completed']),
        ]
    )

    findings = [finding for finding in findings_iterator]

    assert isinstance(findings_iterator, WasIterator)
    assert len(findings) == 0


def test_exception_raised_on_wrong_filters__single_with_and_filter(tvm: TenableIO):
    """
    Test to ensure exception is raised when user attempts to pass `and_filter` with `single_filter`
    """
    with pytest.raises(AttributeError):
        findings_iterator = tvm.was.export(
            single_filter=('scans_started_at', 'gte', '2100/03/23'),
            and_filter=[
                ('scans_started_at', 'gte', '2023/03/23'),
                ('scans_status', 'contains', ['completed']),
            ],
        )


def test_exception_raised_on_wrong_filters__single_with_or_filter(tvm: TenableIO):
    """
    Test to ensure exception is raised when user attempts to pass `or_filter` with `single_filter`
    """
    with pytest.raises(AttributeError):
        findings_iterator = tvm.was.export(
            single_filter=('scans_started_at', 'gte', '2100/03/23'),
            or_filter=[
                ('scans_started_at', 'gte', '2023/03/23'),
                ('scans_status', 'contains', ['completed']),
            ],
        )
