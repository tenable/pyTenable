'''
Testing Schema for scans endpoint
'''
import responses

from tenable.io.v3.vm.scans.schema import (ScanCheckAutoTargetSchema,
                                           ScanConfigureScheduleSchema,
                                           ScanDocumentCreateSchema,
                                           ScanExportSchema, ScanSchema)


def test_scan_schema():
    data = {
        'key': 'test',
        'name': 'test_name',
        'folder_id': 'dfsds9d8f9sdfasdfasd0f8a0ds',
        'history_id': 'dfsds9d8f9sdfasdfasd0f8a0ds',
        'password': 'password',
        'aggregate': True,
        'alt_targets': ['test', 'test2'],
        'read_status': False,
        'enabled': True,
        'limit': 10,
        'matched_resource_limit': 2
    }

    schema = ScanSchema()
    payload = schema.dump(schema.load(data))
    assert payload == data


def test_check_auto_targets():
    data = {
        'network_id': '00000000-0000-0000-0000-000000000000',
        'tags': ['00000000-0000-0000-0000-000000000000',
                 '00000000-0000-0000-0000-000000000000'],
        'target_list': ['127.0.0.1', '0.0.0.0']
    }

    validated_data = {
        'network_id': '00000000-0000-0000-0000-000000000000',
        'tags': ['00000000-0000-0000-0000-000000000000',
                 '00000000-0000-0000-0000-000000000000'],
        'target_list': '127.0.0.1,0.0.0.0'
    }
    schema = ScanCheckAutoTargetSchema()
    payload = schema.dump(schema.load(data))
    assert payload == validated_data


def test_scan_document_create():
    data = {
        'name': 'test',
        'template': 'basic',
        'scanner': 'test',
        'targets': ['127.0.0.1', '0.0.0.0'],
        'file_targets': 'test_targets',
        'credentials': {},
        'compliance': {},
        'plugins': {},
        'schedule_scan': {}
    }

    validated_data = {
        'template': 'basic',
        'file_targets': 'test_targets',
        'name': 'test',
        'schedule_scan': {},
        'credentials': {},
        'scanner': 'test',
        'plugins': {},
        'compliance': {},
        'targets': '127.0.0.1,0.0.0.0'
    }
    context_data = dict()
    context_data['templates_choices'] = ['basic']
    context_data['scanners_choices'] = ['test']
    schema = ScanDocumentCreateSchema(context=context_data)
    payload = schema.dump(schema.load(data))
    assert payload == validated_data


@responses.activate
def test_configure_schedule(api):
    data = {
        'frequency': 'ONETIME',
        'interval': None,
        'weekdays': ['SU', 'MO', 'TU'],
        'day_of_month': 31,
        'starttime': None,
        'timezone': None
    }

    validated_data = {
        'starttime': '2021-12-30T15:42:14+00:00',
        'frequency': 'ONETIME',
        'timezone': 'Etc/UTC',
        'interval': 1,
        'day_of_month': 31,
        'weekdays': 'SU,MO,TU'
    }
    responses.add(
        responses.GET,
        url='https://cloud.tenable.com/scans/timezones',
        json={
            'timezones': [
                {
                    'name': 'Africa/Abidjan',
                    'value': 'Africa/Abidjan'
                },
                {
                    'name': 'Europe/Tiraspol',
                    'value': 'Europe/Tiraspol'
                }
            ]
        }
    )
    context_data = dict()
    context_data['existing_rules'] = {}
    context_data['timezone_choices'] = api._tz
    schema = ScanConfigureScheduleSchema(context=context_data)
    payload = schema.dump(schema.load(data))
    assert payload['frequency'] == validated_data['frequency']


def test_export():
    data = {
        'history_id': 'fasfsdf9as8d7f98s7df8as79df8',
        'scan_type': 'web-app',
        'password': 'password',
        'filter_type': 'and',
        'format': 'html',
        'chapters': ['vuln_by_host']
    }
    validated_data = {
        'password': 'password',
        'filter_type': 'and',
        'format': 'html',
        'history_id': 'fasfsdf9as8d7f98s7df8as79df8',
        'scan_type': 'web-app',
        'chapters': 'vuln_by_host'
    }
    schema = ScanExportSchema()
    payload = schema.dump(schema.load(data))
    assert payload == validated_data
