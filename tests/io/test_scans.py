"""
test scans
"""

import datetime
import os
import time
import uuid
from io import BytesIO
from sys import stdout

import pytest
from responses import matchers
import responses
from responses.matchers import query_param_matcher

from tenable.errors import BadRequestError, NotFoundError, UnexpectedValueError
from tenable.io import TenableIO
from tenable.reports.nessusv2 import NessusReportv2
from tests.checker import check, single
from tests.io.conftest import SCAN_ID_WITH_RESULTS
from tests.pytenable_log_handler import log_exception

NESSUS_REPORT = (
    '<?xml version="1.0" ?><NessusClientData_v2>'
    '<Report name="pytest-scan"><ReportHost name="127.0.0.1">'
    '<HostProperties><tag name="host-ip">127.0.0.1</tag></HostProperties>'
    '<ReportItem port="0" svc_name="general" protocol="tcp" severity="0" '
    'pluginID="19506" pluginName="Nessus Scan Information" pluginFamily="Settings">'
    '<description>Information about this scan.</description>'
    '</ReportItem></ReportHost></Report></NessusClientData_v2>'
)

EDITOR_POLICY_TEMPLATES = {
    'templates': [
        {
            'name': 'advanced',
            'title': 'Advanced Network Scan',
            'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        },
        {
            'name': 'basic',
            'title': 'Basic Network Scan',
            'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
        },
        {
            'name': 'was_scan',
            'title': 'Web App Scan',
            'uuid': '09805055-a034-4088-8986-aac5e1c57d5f0d44f09d736969bf',
        },
    ]
}

EDITOR_SCAN_POLICY = {
    'credentials': {
        'data': [
            {
                'types': [
                    {'max': -1, 'name': 'Database', 'instances': [], 'settings': None}
                ],
                'name': 'Database',
                'default_expand': 0,
            }
        ]
    },
    'policy_has_credentials': False,
    'is_was': None,
    'user_permissions': None,
    'owner': None,
    'title': 'Custom Scan',
    'is_agent': None,
    'uuid': 'ab4bacd2-05f6-425c-9d79-3ba3940ad1c24e51e1f403febe40',
    'settings': {
        'basic': {
            'inputs': [
                {'type': 'entry', 'name': 'Name', 'id': 'name', 'required': True}
            ],
            'title': 'Basic',
            'groups': [{'title': 'Schedule', 'name': 'schedule'}],
        }
    },
    'name': 'custom',
}

EDITOR_SCAN_TEMPLATES = {
    'is_was': None,
    'user_permissions': None,
    'is_agent': None,
    'owner': None,
    'title': 'Advanced Network Scan',
    'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
    'settings': {
        'basic': {
            'inputs': [
                {
                    'type': 'select',
                    'id': 'scanner_id',
                    'name': 'Scanner',
                    'default': None,
                    'options': [],
                }
            ],
            'title': 'Basic',
        }
    },
    'name': 'advanced',
}

EDITOR_SCAN_TEMPLATES_2 = {
    'is_was': True,
    'user_permissions': None,
    'owner': None,
    'title': 'Web App Scan',
    'is_agent': False,
    'uuid': '09805055-a034-4088-8986-aac5e1c57d5f0d44f09d736969bf',
    'settings': {
        'basic': {
            'inputs': [
                {
                    'type': 'select',
                    'id': 'scanner_id',
                    'name': 'Scanner',
                    'default': None,
                    'options': [
                        {
                            'id': '00000000-0000-0000-0000-00000000000000000000000000001',
                            'name': 'US Cloud Scanner',
                            'type': 'local',
                            'environment_name': 'Default',
                            'linked': True,
                            'status': 'on',
                        }
                    ],
                }
            ],
            'title': 'Basic',
        }
    },
    'name': 'was_scan',
}

SCANS_TIMEZONES = {
    'timezones': [
        {'name': 'Africa/Abidjan', 'value': 'Africa/Abidjan'},
        {'name': 'Etc/UTC', 'value': 'Etc/UTC'},
    ]
}

EDITOR_SCAN = {
    'credentials': {
        'data': [
            {
                'types': [
                    {
                        'max': 1,
                        'name': 'IBM DataPower Gateway',
                        'instances': [],
                        'settings': None,
                    }
                ],
                'name': 'API Gateway',
                'default_expand': 0,
            }
        ]
    },
    'is_was': None,
    'user_permissions': 128,
    'owner': 'pytenable_test_user@tenable.com',
    'title': 'Basic Network Scan',
    'is_agent': None,
    'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
    'settings': {
        'basic': {
            'inputs': [
                {
                    'type': 'select',
                    'id': 'scanner_id',
                    'name': 'Scanner',
                    'default': '00000000-0000-0000-0000-00000000000000000000000000001',
                    'options': [
                        {
                            'id': '00000000-0000-0000-0000-00000000000000000000000000001',
                            'name': 'US Cloud Scanner',
                            'type': 'local',
                            'linked': True,
                            'status': 'on',
                        }
                    ],
                }
            ],
            'title': 'Basic',
            'groups': [
                {
                    'title': 'Schedule',
                    'name': 'schedule',
                    'enabled': True,
                    'rrules': None,
                    'timezone': None,
                    'starttime': None,
                }
            ],
        },
        'advanced': {
            'inputs': None,
            'modes': {
                'id': 'advanced_mode',
                'name': 'mode',
                'type': 'ui_radio',
                'default': 'Custom',
            },
            'title': 'Advanced',
        },
    },
    'name': 'basic',
}

EDITOR_SCAN_2 = {
    'credentials': {
        'data': [
            {
                'types': [
                    {
                        'max': 1,
                        'name': 'IBM DataPower Gateway',
                        'instances': [],
                        'settings': None,
                    }
                ],
                'name': 'API Gateway',
                'default_expand': 0,
            }
        ]
    },
    'is_was': None,
    'user_permissions': 128,
    'owner': 'pytenable_test_user@tenable.com',
    'title': 'Basic Network Scan',
    'is_agent': None,
    'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
    'settings': {
        'basic': {
            'inputs': [
                {
                    'type': 'select',
                    'id': 'scanner_id',
                    'name': 'Scanner',
                    'default': '00000000-0000-0000-0000-00000000000000000000000000001',
                    'options': [
                        {
                            'id': '00000000-0000-0000-0000-00000000000000000000000000001',
                            'name': 'US Cloud Scanner',
                            'type': 'local',
                            'linked': True,
                            'status': 'on',
                        }
                    ],
                }
            ],
            'title': 'Basic',
            'groups': [
                {
                    'title': 'Schedule',
                    'name': 'schedule',
                    'enabled': True,
                    'rrules': 'FREQ=ONETIME;INTERVAL=1',
                    'timezone': 'Etc/UTC',
                    'starttime': '20210324T143000',
                }
            ],
        },
        'advanced': {
            'inputs': None,
            'modes': {
                'id': 'advanced_mode',
                'name': 'mode',
                'type': 'ui_radio',
                'default': 'Custom',
            },
            'title': 'Advanced',
        },
    },
    'name': 'basic',
}

FILTERS_SCANS_REPORTS = {
    'filters': [
        {
            'name': 'host.id',
            'readable_name': 'Asset ID',
            'control': {
                'type': 'entry',
                'regex': '[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*',
                'readable_regex': '01234567-abcd-ef01-2345-6789abcdef01',
            },
            'operators': ['eq', 'neq', 'match'],
            'group_name': 'vulnerability',
        },
        {
            'name': 'plugin.attributes.exploit_framework_canvas',
            'readable_name': 'CANVAS Exploit Framework',
            'control': {'type': 'dropdown', 'list': ['true', 'false']},
            'operators': ['eq', 'neq'],
            'group_name': 'vulnerability',
        },
    ]
}

SCANS_HOSTS = {
    'info': {
        'mac-address': None,
        'host-fqdn': None,
        'host-ip': '162.159.129.83',
        'operating-system': None,
        'host_end': 'Thu Jun 10 11:37:06 2021',
        'host_start': 'Thu Jun 10 11:24:12 2021',
    },
    'vulnerabilities': [
        {
            'count': 13,
            'host_id': 2,
            'hostname': '162.159.129.83',
            'plugin_family': 'Web Servers',
            'plugin_id': 10107,
            'plugin_name': 'HTTP Server Type and Version',
            'severity': 0,
            'severity_index': 0,
            'vuln_index': 0,
        }
    ],
    'compliance': [],
}

SCANS = {
    'hosts': [
        {
            'asset_id': 1829,
            'host_id': 1829,
            'uuid': '9a0bcbc9-68fe-4d79-a6ed-30b888a124e0',
            'hostname': '172.105.154.216',
            'progress': '100-100/200-200',
            'scanprogresscurrent': 100,
            'scanprogresstotal': 100,
            'numchecksconsidered': 100,
            'totalchecksconsidered': 100,
            'severity': 176,
            'score': 2858,
            'info': 148,
            'low': 1,
            'medium': 27,
            'high': 0,
            'critical': 0,
            'host_index': 0,
        }
    ],
    'vulnerabilities': [
        {
            'count': 641,
            'plugin_id': 11219,
            'plugin_name': 'Nessus SYN scanner',
            'severity': 0,
            'plugin_family': 'Port scanners',
            'vuln_index': 1,
        },
        {
            'count': 554,
            'plugin_id': 22964,
            'plugin_name': 'Service Detection',
            'severity': 0,
            'plugin_family': 'Service detection',
            'vuln_index': 2,
        },
    ],
}


@pytest.fixture(name='scheduled_scan')
def fixture_scheduled_scan():
    """
    Fixture to create scheduled scan
    """
    return {
        'tag_type': None,
        'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
        'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
        'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
        'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
        'description': None,
        'policy_id': 81,
        'scanner_id': None,
        'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
        'emails': None,
        'sms': '',
        'enabled': True,
        'include_aggregate': True,
        'scan_time_window': None,
        'custom_targets': '127.0.0.1',
        'target_network_uuid': None,
        'auto_routed': 0,
        'remediation': 0,
        'starttime': '20210324T143000',
        'rrules': 'FREQ=ONETIME;INTERVAL=1',
        'timezone': 'Etc/UTC',
        'notification_filters': None,
        'shared': 0,
        'user_permissions': 128,
        'default_permissions': 0,
        'owner': 'pytenable_test_user@tenable.com',
        'owner_id': 2201492,
        'last_modification_date': 1616594477,
        'creation_date': 1616594477,
        'type': 'public',
        'id': 82,
    }


@responses.activate
def test_scan_progress(tvm):
    responses.get('https://nourl/scans/1/progress', json={'progress': 50})
    assert tvm.scans.progress(1) == 50


@responses.activate
def test_scan_create_scan_document_template_typeerror(tvm):
    """
    test to raise exception when type of template param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    with pytest.raises(TypeError):
        getattr(tvm.scans, '_create_scan_document')({'template': 123})


@responses.activate
def test_scan_create_scan_document_template_unexpected_value_error(tvm):
    """
    test to raise exception when template param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.scans, '_create_scan_document')({'template': 'nothing_here'})


@responses.activate
def test_scan_create_scan_socument_template_pass(tvm):
    """
    test to create scan document basic template
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    templates = tvm.policies.templates()
    resp = getattr(tvm.scans, '_create_scan_document')({'template': 'basic'})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    assert resp['uuid'] == templates['basic']


@responses.activate
def test_scan_create_scan_document_policies_id_pass(tvm):
    """
    test to create scan document policy param using id
    """
    responses.add(
        responses.GET,
        'https://nourl/policies',
        json={
            'policies': [
                {
                    'no_target': 'false',
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'description': None,
                    'name': '03640b8b-7709-4483-b4e6-a5c3c600dc13',
                    'owner': 'test_admin@pytenable.io',
                    'visibility': 'private',
                    'shared': 0,
                    'user_permissions': 128,
                    'last_modification_date': 1521561156,
                    'creation_date': 1521561156,
                    'owner_id': 3,
                    'id': 101,
                }
            ]
        },
    )
    responses.add(
        responses.GET, 'https://nourl/editor/scan/policy/101', json=EDITOR_SCAN_POLICY
    )
    policies = tvm.policies.list()
    policy = policies[0]
    resp = getattr(tvm.scans, '_create_scan_document')({'policy': policy['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']


@responses.activate
def test_scan_create_scan_document_policies_name_pass(tvm):
    """
    test to create scan document with policy param using name
    """
    responses.add(
        responses.GET,
        'https://nourl/policies',
        json={
            'policies': [
                {
                    'no_target': 'false',
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'description': None,
                    'name': '03640b8b-7709-4483-b4e6-a5c3c600dc13',
                    'owner': 'test_admin@pytenable.io',
                    'visibility': 'private',
                    'shared': 0,
                    'user_permissions': 128,
                    'last_modification_date': 1521561156,
                    'creation_date': 1521561156,
                    'owner_id': 3,
                    'id': 101,
                }
            ]
        },
    )
    responses.add(
        responses.GET, 'https://nourl/editor/scan/policy/101', json=EDITOR_SCAN_POLICY
    )
    policies = tvm.policies.list()
    policy = policies[0]
    resp = getattr(tvm.scans, '_create_scan_document')({'policy': policy['name']})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == policy['id']


def test_scan_create_scan_document_file_target_name(tvm):
    """
    test to create scan document with file targets param and uploaded file name
    """
    resp = getattr(tvm.scans, '_create_scan_document')({'file_targets': 'file.txt'})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'file_targets', str)
    assert resp['settings']['file_targets'] == 'file.txt'


@responses.activate
def test_scan_create_scan_document_scanner_unexpectedvalueerror(tvm):
    """
    test to raise exception when scanner param value does not match the choices.
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        json={
            'is_was': None,
            'user_permissions': None,
            'is_agent': None,
            'owner': None,
            'title': 'Advanced Network Scan',
            'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
            'settings': {'basic': {'inputs': [], 'title': 'Basic'}},
            'name': 'advanced',
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/09805055-a034-4088-8986-aac5e1c57d5f0d44f09d736969bf',
        json={
            'is_was': True,
            'user_permissions': None,
            'owner': None,
            'title': 'Web App Scan',
            'is_agent': False,
            'uuid': '09805055-a034-4088-8986-aac5e1c57d5f0d44f09d736969bf',
            'settings': {
                'basic': {
                    'inputs': [
                        {
                            'type': 'entry',
                            'name': 'Name',
                            'id': 'name',
                            'required': True,
                        }
                    ],
                    'title': 'Basic',
                }
            },
            'name': 'was_scan',
        },
    )
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.scans, '_create_scan_document')({'scanner': 'nothing to see here'})


@responses.activate
def test_scan_create_scan_document_scanner_uuid_pass(tvm):
    """
    test to create scan document with scanner uuid param
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        json=EDITOR_SCAN_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/09805055-a034-4088-8986-aac5e1c57d5f0d44f09d736969bf',
        json=EDITOR_SCAN_TEMPLATES_2,
    )
    scanners = tvm.scanners.allowed_scanners()
    scanner = scanners[0]
    resp = getattr(tvm.scans, '_create_scan_document')({'scanner': scanner['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', 'scanner-uuid')
    assert resp['settings']['scanner_id'] == scanner['id']


@responses.activate
def test_scan_create_scan_document_scanner_name_pass(tvm):
    """
    test to create scan document with scanner name param
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
        json=EDITOR_SCAN_TEMPLATES,
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates/09805055-a034-4088-8986-aac5e1c57d5f0d44f09d736969bf',
        json=EDITOR_SCAN_TEMPLATES_2,
    )
    scanners = tvm.scanners.allowed_scanners()
    scanner = scanners[0]
    resp = getattr(tvm.scans, '_create_scan_document')({'scanner': scanner['name']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', str)
    assert resp['settings']['scanner_id'] == scanner['id']


# @pytest.mark.vcr()
# def test_scan_attachment_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.attachment('nope', 1)


def test_scan_attachment_attachement_id_typeerror(tvm):
    """
    test to raise exception when type of attachment_id param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.attachment(1, 'nope')


@pytest.mark.xfail(raises=BadRequestError)
@responses.activate
def test_scan_attachement_notfounderror(tvm):
    """
    test to raise exception when attachment not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/1/attachments/1',
        json={'error': "Invalid 'key' field: invalid key format"},
        status=400,
        match=[matchers.query_param_matcher({'key': 'none'})],
    )
    with pytest.raises(NotFoundError):
        tvm.scans.attachment(1, 1, 'none')


def test_scan_create_scan_schedule_freq_typeerror(tvm):
    """
    test to raise exception when type of frequency param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.create_scan_schedule(enabled=True, frequency=1)


def test_scan_create_scan_schedule_freq_unexpectedvalueerror(tvm):
    """
    test to raise exception when frequency param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.scans.create_scan_schedule(enabled=True, frequency='nope')


def test_scan_create_scan_schedule_interval_typeerror(tvm):
    """
    test to raise exception when type of interval param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.create_scan_schedule(enabled=True, interval='nope')


def test_scan_create_scan_schedule_day_of_month_typeerror(tvm):
    """
    test to raise exception when type of day_of_month param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.create_scan_schedule(
            enabled=True, frequency='monthly', day_of_month='nope'
        )


def test_scan_create_scan_schedule_day_of_month_unexpectedvalueerror(tvm):
    """
    test to raise exception when day_of_month param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.scans.create_scan_schedule(
            enabled=True, frequency='monthly', day_of_month=300
        )


def test_scan_create_scan_schedule_weekdays_typeerror(tvm):
    """
    test to raise exception when type of weekdays param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.create_scan_schedule(
            enabled=True, frequency='weekly', weekdays='nope'
        )


def test_scan_create_scan_schedule_weekdays_unexpectedvalueerror(tvm):
    """
    test to raise exception when weekdays param value does not match the choices.
    """
    with pytest.raises(UnexpectedValueError):
        tvm.scans.create_scan_schedule(
            enabled=True, frequency='weekly', weekdays=['MO', 'WE', 'nope']
        )


def test_scan_create_scan_schedule_starttime_typeerror(tvm):
    """
    test to raise exception when type of starttime param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.create_scan_schedule(enabled=True, starttime='fail')


@responses.activate
def test_scan_create_scan_schedule_timezone_typeerror(tvm):
    """
    test to raise exception when type of timezone param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.scans.create_scan_schedule(enabled=True, timezone=1)


@responses.activate
def test_scan_create_scan_schedule_timezone_unexpectedvalueerror(tvm):
    """
    test to raise exception when timezone param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(UnexpectedValueError):
        tvm.scans.create_scan_schedule(enabled=True, timezone='the zone of time')


@responses.activate
def test_scan_configure_scan_schedule_freq_typeerror(tvm, scan):
    """
    test to raise exception when type of frequency param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(TypeError):
        tvm.scans.configure_scan_schedule(scan['id'], enabled=True, frequency=1)


@responses.activate
def test_scan_configure_scan_schedule_freq_unexpectedvalueerror(tvm, scan):
    """
    test to raise exception when frequency param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(UnexpectedValueError):
        tvm.scans.configure_scan_schedule(scan['id'], enabled=True, frequency='nope')


@responses.activate
def test_scan_configure_scan_schedule_interval_typeerror(tvm, scan):
    """
    test to raise exception when type of interval param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(TypeError):
        tvm.scans.configure_scan_schedule(scan['id'], enabled=True, interval='nope')


@responses.activate
def test_scan_configure_scan_schedule_day_of_month_typeerror(tvm, scan):
    """
    test to raise exception when type of day_of_month param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(TypeError):
        tvm.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='monthly', day_of_month='nope'
        )


@responses.activate
def test_scan_configure_scan_schedule_day_of_month_unexpectedvalueerror(tvm, scan):
    """
    test to raise exception when day_of_month param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(UnexpectedValueError):
        tvm.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='monthly', day_of_month=300
        )


@responses.activate
def test_scan_configure_scan_schedule_weekdays_typeerror(tvm, scan):
    """
    test to raise exception when type of weekdays param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(TypeError):
        tvm.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='weekly', weekdays='nope'
        )


@responses.activate
def test_scan_configure_scan_schedule_weekdays_unexpectedvalueerror(tvm, scan):
    """
    test to raise exception when weekdays param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(UnexpectedValueError):
        tvm.scans.configure_scan_schedule(
            scan['id'], enabled=True, frequency='weekly', weekdays=['MO', 'WE', 'nope']
        )


@responses.activate
def test_scan_configure_scan_schedule_starttime_typeerror(tvm, scan):
    """
    test to raise exception when type of starttime param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    with pytest.raises(TypeError):
        tvm.scans.configure_scan_schedule(scan['id'], enabled=True, starttime='fail')


@responses.activate
def test_scan_configure_scan_schedule_timezone_typeerror(tvm, scan):
    """
    test to raise exception when type of timezone param does not match the expected type.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(TypeError):
        tvm.scans.configure_scan_schedule(scan['id'], enabled=True, timezone=1)


@responses.activate
def test_scan_configure_scan_schedule_timezone_unexpectedvalueerror(tvm, scan):
    """
    test to raise exception when timezone param value does not match the choices.
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    with pytest.raises(UnexpectedValueError):
        tvm.scans.configure_scan_schedule(
            scan['id'], enabled=True, timezone='the zone of time'
        )


# @pytest.mark.vcr()
# def test_scan_configure_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.configure('abc123')

# @pytest.mark.vcr()
# def test_scan_configure_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.configure('nope')


@responses.activate
def test_scan_configure_notfounderror(tvm):
    """
    test to raise exception when scan_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/1',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scans.configure(1, name=str(uuid.uuid4()))


@responses.activate
def test_scan_configure(tvm, scan):
    """
    test to configure scan
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/221',
        json={
            'credentials': {
                'data': [
                    {
                        'types': [
                            {
                                'max': -1,
                                'name': 'Database',
                                'instances': [],
                                'settings': None,
                            }
                        ],
                        'name': 'Database',
                        'default_expand': 0,
                    }
                ]
            },
            'is_was': None,
            'user_permissions': 128,
            'owner': 'pytenable_test_user@tenable.com',
            'title': 'Basic Network Scan',
            'is_agent': None,
            'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
            'settings': {
                'basic': {
                    'inputs': [
                        {
                            'type': 'select',
                            'id': 'scanner_id',
                            'name': 'Scanner',
                            'default': '00000000-0000-0000-0000-00000000000000000000000000001',
                            'options': [
                                {
                                    'id': '00000000-0000-0000-0000-00000000000000000000000000001',
                                    'name': 'US Cloud Scanner',
                                    'type': 'local',
                                    'environment_name': None,
                                    'linked': True,
                                    'status': 'on',
                                }
                            ],
                        }
                    ],
                    'title': 'Basic',
                    'groups': [
                        {
                            'title': 'Schedule',
                            'name': 'schedule',
                            'enabled': True,
                            'rrules': None,
                            'timezone': None,
                            'starttime': None,
                        }
                    ],
                },
                'advanced': {
                    'inputs': None,
                    'modes': {
                        'id': 'advanced_mode',
                        'name': 'mode',
                        'type': 'ui_radio',
                        'default': 'Custom',
                    },
                    'title': 'Advanced',
                },
            },
            'name': 'basic',
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/scans/221',
        json={
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-f5e70c2a-e66f-e236-0288-b4bd57c121e19c4288ebdff2ddb2',
            'name': 'MODIFIED',
            'description': None,
            'policy_id': 220,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'dashboard_file': None,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'starttime': None,
            'rrules': None,
            'timezone': None,
            'notification_filters': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1544815411,
            'creation_date': 1544815410,
            'type': 'public',
            'id': 221,
        },
    )
    mod = tvm.scans.configure(scan['id'], name='MODIFIED')
    assert mod['id'] == scan['id']
    assert mod['name'] == 'MODIFIED'


@responses.activate
def test_scan_configure_schedule_onetime_to_daily(tvm, scheduled_scan):
    """
    test to edit scan schedule frequency from onetime to daily
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(responses.GET, 'https://nourl/editor/scan/82', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/82',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
            'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
            'description': None,
            'policy_id': 81,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=DAILY;INTERVAL=1',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594480,
            'creation_date': 1616594477,
            'type': 'public',
            'id': 82,
        },
    )
    schedule = tvm.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='daily'
    )
    mod = tvm.scans.configure(scheduled_scan['id'], schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=DAILY;INTERVAL=1'


@responses.activate
def test_scan_configure_schedule_onetime_to_weekly_valdefault(tvm, scheduled_scan):
    """
    test to edit scheduled scan frequency from onetime to weekly
    and assign default value to weekdays param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(responses.GET, 'https://nourl/editor/scan/82', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/82',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
            'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
            'description': None,
            'policy_id': 81,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=WEEKLY;INTERVAL=1;BYDAY=SU,MO,TU,WE,TH,FR,SA',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594494,
            'creation_date': 1616594491,
            'type': 'public',
            'id': 82,
        },
    )
    schedule = tvm.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='weekly'
    )
    mod = tvm.scans.configure(scheduled_scan['id'], schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=SU,MO,TU,WE,TH,FR,SA'


@responses.activate
def test_scan_configure_schedule_onetime_to_weekly_valassigned(tvm, scheduled_scan):
    """
    test to edit scheduled scan frequency from onetime to weekly
    and assign user defined value to weekdays param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(responses.GET, 'https://nourl/editor/scan/82', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/82',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
            'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
            'description': None,
            'policy_id': 81,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594507,
            'creation_date': 1616594504,
            'type': 'public',
            'id': 82,
        },
    )
    schedule = tvm.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='weekly', weekdays=['MO', 'TU']
    )
    mod = tvm.scans.configure(scheduled_scan['id'], schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU'


@responses.activate
def test_scan_configure_schedule_freq_weekly_valavailable(tvm):
    """
    test to edit weekly scheduled scan and assign existing weekdays values to weekdays param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-235b34f7-3457-028e-e9b3-735c714f774b10c5f6cc31235cbd',
                'name': 'pytest: 1bbf265f-1933-4a97-9481-aa6386f5ad32',
                'description': None,
                'policy_id': 87,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T143000',
                'rrules': 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616594517,
                'creation_date': 1616594517,
                'type': 'public',
                'id': 88,
            }
        },
    )
    responses.add(responses.GET, 'https://nourl/editor/scan/88', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/88',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-235b34f7-3457-028e-e9b3-735c714f774b10c5f6cc31235cbd',
            'name': 'pytest: 1bbf265f-1933-4a97-9481-aa6386f5ad32',
            'description': None,
            'policy_id': 87,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TU',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594520,
            'creation_date': 1616594517,
            'type': 'public',
            'id': 88,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/88')
    create_schedule = tvm.scans.create_scan_schedule(
        enabled=True, frequency='weekly', weekdays=['MO', 'TU']
    )
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=create_schedule,
    )
    update_schedule = tvm.scans.configure_scan_schedule(scan_id=scan['id'], interval=2)
    mod = tvm.scans.configure(scan['id'], schedule_scan=update_schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TU'
    tvm.scans.delete(mod['id'])


def test_upsert_aws_credentials(tvm):
    """
    test to check if aws credentials can be added to edit section of credentials
    dict of scan
    """
    scan = {
        'credentials': {
            'current': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS1',
                            'secret_key': 'SECRET1',
                            'id': 12346,
                        }
                    ]
                }
            },
            'add': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS2',
                            'secret_key': 'SECRET2',
                            'id': 12347,
                        }
                    ]
                }
            },
        },
    }

    scan_output = {
        'credentials': {
            'current': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS1',
                            'secret_key': 'SECRET1',
                            'id': 12346,
                        }
                    ]
                }
            },
            'add': {'Cloud Services': {}},
            'edit': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS2',
                            'secret_key': 'SECRET2',
                            'id': 12347,
                        }
                    ]
                }
            },
        },
    }
    scan_actual = tvm.scans.upsert_aws_credentials(scan)
    assert isinstance(scan_actual, dict)
    assert scan_output == scan_actual


def test_upsert_aws_credentials_no_current(tvm):
    """
    test to check if aws credentials can be added to edit section of credentials
    dict of scan when there is no current
    """
    scan = {
        'credentials': {
            'current': {},
            'add': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS2',
                            'secret_key': 'SECRET2',
                            'id': 12347,
                        }
                    ]
                }
            },
        },
    }
    scan_expected = {
        'credentials': {
            'current': {},
            'add': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS2',
                            'secret_key': 'SECRET2',
                            'id': 12347,
                        }
                    ]
                }
            },
        },
    }
    scan_actual = tvm.scans.upsert_aws_credentials(scan)
    assert isinstance(scan_actual, dict)
    assert scan_expected == scan_actual


def test_upsert_aws_credentials_no_add(tvm):
    """
    test to check if aws credentials can be added to edit section of credentials
    dict of scan when there is no add
    """
    scan = {
        'credentials': {
            'current': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS2',
                            'secret_key': 'SECRET2',
                            'id': 12346,
                        }
                    ]
                }
            },
            'add': {},
        },
    }
    scan_expected = {
        'credentials': {
            'current': {
                'Cloud Services': {
                    'Amazon AWS': [
                        {
                            'access_key_id': 'ACCESS2',
                            'secret_key': 'SECRET2',
                            'id': 12346,
                        }
                    ]
                }
            },
            'add': {},
        },
    }
    scan_actual = tvm.scans.upsert_aws_credentials(scan)
    assert isinstance(scan_actual, dict)
    assert scan_expected == scan_actual


@responses.activate
def test_scan_configure_schedule_onetime_to_monthly_valdefault(tvm, scheduled_scan):
    """
    test to edit scheduled scan frequency from onetime to monthly
    and assign default value to day_of_month param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(responses.GET, 'https://nourl/editor/scan/82', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/82',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
            'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
            'description': None,
            'policy_id': 81,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=24',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594533,
            'creation_date': 1616594530,
            'type': 'public',
            'id': 82,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/82')
    schedule = tvm.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='monthly'
    )
    mod = tvm.scans.configure(scheduled_scan['id'], schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'].split(';')[0] == 'FREQ=MONTHLY'
    tvm.scans.delete(mod['id'])


@responses.activate
def test_scan_configure_schedule_onetime_to_monthly_valassigned(tvm, scheduled_scan):
    """
    test to edit scheduled scan frequency from onetime to monthly
    and assign user defined value to day_of_month param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(responses.GET, 'https://nourl/editor/scan/82', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/82',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
            'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
            'description': None,
            'policy_id': 81,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=8',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594547,
            'creation_date': 1616594544,
            'type': 'public',
            'id': 82,
        },
    )
    schedule = tvm.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='monthly', day_of_month=8
    )
    mod = tvm.scans.configure(scheduled_scan['id'], schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=8'


@responses.activate
def test_scan_configure_schedule_freq_monthly_valavailable(tvm):
    """
    test to edit scheduled scan and assign existing day_of_month value to day_of_month param
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-1c79f3db-e7a2-910e-539e-cc4f0d6e1d05e3ec7897e36242a8',
                'name': 'pytest: 92140b44-aaa0-40b0-8d2e-e19b06b0354a',
                'description': None,
                'policy_id': 93,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T143000',
                'rrules': 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=8',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616594556,
                'creation_date': 1616594556,
                'type': 'public',
                'id': 94,
            }
        },
    )
    responses.add(responses.GET, 'https://nourl/editor/scan/94', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/94',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-1c79f3db-e7a2-910e-539e-cc4f0d6e1d05e3ec7897e36242a8',
            'name': 'pytest: 92140b44-aaa0-40b0-8d2e-e19b06b0354a',
            'description': None,
            'policy_id': 93,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=8',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594559,
            'creation_date': 1616594556,
            'type': 'public',
            'id': 94,
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/94')
    create_schedule = tvm.scans.create_scan_schedule(
        enabled=True, frequency='monthly', day_of_month=8
    )
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=create_schedule,
    )
    update_schedule = tvm.scans.configure_scan_schedule(scan['id'], interval=2)
    mod = tvm.scans.configure(scan['id'], schedule_scan=update_schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=8'
    tvm.scans.delete(mod['id'])


@responses.activate
def test_scan_configure_schedule_freq_yearly(tvm, scheduled_scan):
    """
    test to edit scheduled schan frequency from onetime to yearly
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(responses.GET, 'https://nourl/editor/scan/82', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/82',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
            'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
            'description': None,
            'policy_id': 81,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T150000',
            'rrules': 'FREQ=YEARLY;INTERVAL=2',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594572,
            'creation_date': 1616594569,
            'type': 'public',
            'id': 82,
        },
    )
    update_schedule = tvm.scans.configure_scan_schedule(
        scheduled_scan['id'], frequency='yearly', interval=2
    )
    mod = tvm.scans.configure(scheduled_scan['id'], schedule_scan=update_schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=YEARLY;INTERVAL=2'


@responses.activate
def test_scan_configure_enable_scan_schedule(tvm, scan):
    """
    test to enable scan schedule
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/221', json=EDITOR_SCAN)
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.PUT,
        'https://nourl/scans/221',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-f5e70c2a-e66f-e236-0288-b4bd57c121e19c4288ebdff2ddb2',
            'name': 'pytest: 9452d6f9-79e6-4079-99da-fb0590e9740d',
            'description': None,
            'policy_id': 220,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': True,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T143000',
            'rrules': 'FREQ=ONETIME;INTERVAL=1',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594585,
            'creation_date': 1616594581,
            'type': 'public',
            'id': 221,
        },
    )
    schedule = tvm.scans.configure_scan_schedule(scan['id'], enabled=True)
    mod = tvm.scans.configure(scan['id'], schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scan['id']
    assert mod['enabled'] is True
    assert mod['rrules'] == 'FREQ=ONETIME;INTERVAL=1'


@responses.activate
def test_scan_configure_disable_scan_schedule(tvm, scheduled_scan):
    """
    test to disable scan schedule
    """
    responses.add(responses.GET, 'https://nourl/editor/scan/82', json=EDITOR_SCAN_2)
    responses.add(
        responses.PUT,
        'https://nourl/scans/82',
        json={
            'tag_type': None,
            'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
            'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
            'uuid': 'template-8d334347-d72d-b804-27b9-50be1dd331cdce6d212ceccf2135',
            'name': 'pytest: 32dd9767-efc4-4db2-afeb-dc3d1a969d75',
            'description': None,
            'policy_id': 81,
            'scanner_id': None,
            'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
            'emails': None,
            'sms': '',
            'enabled': False,
            'include_aggregate': True,
            'scan_time_window': None,
            'custom_targets': '127.0.0.1',
            'target_network_uuid': None,
            'auto_routed': 0,
            'remediation': 0,
            'starttime': '20210324T143000',
            'rrules': 'FREQ=ONETIME;INTERVAL=1',
            'timezone': 'Etc/UTC',
            'notification_filters': None,
            'tag_targets_ip_selection': 3,
            'tag_targets_address_order': None,
            'shared': 0,
            'user_permissions': 128,
            'default_permissions': 0,
            'owner': 'pytenable_test_user@tenable.com',
            'owner_id': 2201492,
            'last_modification_date': 1616594598,
            'creation_date': 1616594595,
            'type': 'public',
            'id': 82,
        },
    )
    schedule = tvm.scans.configure_scan_schedule(scheduled_scan['id'], enabled=False)
    mod = tvm.scans.configure(scheduled_scan['id'], schedule_scan=schedule)
    assert isinstance(mod, dict)
    check(mod, 'creation_date', int)
    check(mod, 'custom_targets', str)
    check(mod, 'default_permissions', int)
    check(mod, 'description', str, allow_none=True)
    check(mod, 'emails', str, allow_none=True)
    check(mod, 'enabled', bool)
    check(mod, 'id', int)
    check(mod, 'last_modification_date', int)
    check(mod, 'owner', str)
    check(mod, 'owner_id', int)
    check(mod, 'policy_id', int)
    check(mod, 'name', str)
    check(mod, 'rrules', str, allow_none=True)
    check(mod, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(mod, 'shared', int)
    check(mod, 'starttime', str, allow_none=True)
    check(mod, 'timezone', str, allow_none=True)
    check(mod, 'type', str)
    check(mod, 'user_permissions', int)
    check(mod, 'uuid', str)
    assert mod['id'] == scheduled_scan['id']
    assert mod['enabled'] is False


# @pytest.mark.vcr()
# def test_scan_copy_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.copy('nope')


def test_scan_copy_folder_id_typeerror(tvm):
    """
    test to raise exception when type of folder_id param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.copy(1, folder_id='nope')


def test_scan_copy_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.copy(1, name=1)


@responses.activate
def test_scan_copy_notfounderror(tvm):
    """
    test to raise exception when scan_id not found.
    """
    responses.add(
        responses.POST,
        'https://nourl/scans/1/copy',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scans.copy(1)


@responses.activate
def test_scan_copy(tvm, scan):
    """
    test to copy scan
    """
    responses.add(
        responses.POST,
        'https://nourl/scans/221/copy',
        json={
            'timezone': None,
            'enabled': True,
            'last_modification_date': 1544138488,
            'id': 13223,
            'status': 'empty',
            'user_permissions': 128,
            'owner': 'pytenable_test_user@tenable.com',
            'starttime': None,
            'control': True,
            'uuid': '61468253-a5b5-0713-9ad7-7f5345088b37226393737aa9a964',
            'rrules': None,
            'creation_date': 1544138488,
            'read': False,
            'shared': False,
            'name': 'Copy of pytest: 9452d6f9-79e6-4079-99da-fb0590e9740d',
        },
    )
    clone = tvm.scans.copy(scan['id'])
    assert isinstance(clone, dict)
    check(clone, 'control', bool)
    check(clone, 'creation_date', int)
    check(clone, 'enabled', bool)
    check(clone, 'id', int)
    check(clone, 'last_modification_date', int)
    check(clone, 'owner', str)
    check(clone, 'name', str)
    check(clone, 'read', bool)
    check(clone, 'rrules', str, allow_none=True)
    # This is in the documentation, however isn't always returned oddly.
    # check(clone, 'schedule_uuid', 'scanner-uuid')
    check(clone, 'shared', bool)
    check(clone, 'starttime', str, allow_none=True)
    check(clone, 'status', str)
    check(clone, 'timezone', str, allow_none=True)
    check(clone, 'user_permissions', int)
    check(clone, 'uuid', 'scanner-uuid')


@responses.activate
def test_scan_create_no_template_pass(tvm, scan):
    """
    test to create scan when no template is provided by user
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(responses.POST, 'https://nourl/scans', json={'scan': scan})
    scan = tvm.scans.create(name=scan['name'], targets=['127.0.0.1'])
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)


@responses.activate
def test_scan_create_scheduled_scan_default_schedule(tvm):
    """
    test to create scan with default schedule
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-f82d78a1-5b19-f701-6986-3980aca3df7b44e18f4c72fd66b4',
                'name': 'pytest: 4dd2eeab-ae47-4d48-84d2-c53fa5c38ddc',
                'description': None,
                'policy_id': 47,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T123000',
                'rrules': 'FREQ=ONETIME;INTERVAL=1',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616587244,
                'creation_date': 1616587244,
                'type': 'public',
                'id': 48,
            }
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/48')
    schedule_scan = tvm.scans.create_scan_schedule(enabled=True)
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan,
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=ONETIME;INTERVAL=1'
    tvm.scans.delete(scan['id'])


@responses.activate
def test_scan_create_scheduled_scan_freq_daily(tvm):
    """
    test to create scheduled scan with frequency as daily
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-3263bd86-ede1-a9dd-4444-509217096341b3b887a2d6c9167a',
                'name': 'pytest: 7d11cbc2-f88c-4280-936c-7af74a79db8a',
                'description': None,
                'policy_id': 49,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T123000',
                'rrules': 'FREQ=DAILY;INTERVAL=1',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616587252,
                'creation_date': 1616587252,
                'type': 'public',
                'id': 50,
            }
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/50')
    schedule_scan = tvm.scans.create_scan_schedule(enabled=True, frequency='daily')
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan,
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=DAILY;INTERVAL=1'
    tvm.scans.delete(scan['id'])


@responses.activate
def test_scan_create_scheduled_scan_freq_weekly_valdefault(tvm):
    """
    test to create scheduled scan with frequency as weekly
    and default weekdays value
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-5f379894-735c-fdc4-7088-2bad6abd5160688989be719e9707',
                'name': 'pytest: b592cb35-0b69-4f6a-a6aa-310a46710184',
                'description': None,
                'policy_id': 51,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T123000',
                'rrules': 'FREQ=WEEKLY;INTERVAL=1;BYDAY=SU,MO,TU,WE,TH,FR,SA',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616587261,
                'creation_date': 1616587261,
                'type': 'public',
                'id': 52,
            }
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/52')
    schedule_scan = tvm.scans.create_scan_schedule(enabled=True, frequency='weekly')
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan,
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=SU,MO,TU,WE,TH,FR,SA'
    tvm.scans.delete(scan['id'])


@responses.activate
def test_scan_create_scheduled_scan_freq_weekly_valassigned(tvm):
    """
    test to create scheduled scan with frequency as weekly
    with user defined weekdays values
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-316aa7f1-4269-6fa8-23a4-597132a8ab2910f94bdf0f4334c7',
                'name': 'pytest: 75df6af3-58c3-473d-8cb3-746d1d218b09',
                'description': None,
                'policy_id': 53,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T123000',
                'rrules': 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616587270,
                'creation_date': 1616587270,
                'type': 'public',
                'id': 54,
            }
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/54')
    schedule_scan = tvm.scans.create_scan_schedule(
        enabled=True, frequency='weekly', weekdays=['MO', 'TU']
    )
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan,
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU'
    tvm.scans.delete(scan['id'])


@responses.activate
def test_scan_create_scheduled_scan_freq_monthly_valdefault(tvm):
    """
    test to create scheduled scan with frequency as monthly
    and day_of_month as default value
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-316c2258-66e8-c9c2-441c-6e83853b1e47d0862018b8db7316',
                'name': 'pytest: ff04ef69-b0fa-4ba9-aee9-20fd547a9cc0',
                'description': None,
                'policy_id': 55,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T123000',
                'rrules': 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=24',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616587278,
                'creation_date': 1616587278,
                'type': 'public',
                'id': 56,
            }
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/56')
    schedule_scan = tvm.scans.create_scan_schedule(enabled=True, frequency='monthly')
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan,
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'].split(';')[0] == 'FREQ=MONTHLY'
    tvm.scans.delete(scan['id'])


@responses.activate
def test_scan_create_scheduled_scan_freq_monthly_valassigned(tvm):
    """
    test to create scheduled scan with frequency as monthly
    with user defined day_of_month value
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-8f3f4eee-a8fe-ef18-db78-84b8bd1703fcdac73582db14f5bb',
                'name': 'pytest: c2f7bd03-22a4-434a-8462-100746727ba5',
                'description': None,
                'policy_id': 57,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T123000',
                'rrules': 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=8',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616587287,
                'creation_date': 1616587287,
                'type': 'public',
                'id': 58,
            }
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/58')
    schedule_scan = tvm.scans.create_scan_schedule(
        enabled=True, frequency='monthly', day_of_month=8
    )
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan,
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=MONTHLY;INTERVAL=1;BYMONTHDAY=8'
    tvm.scans.delete(scan['id'])


@responses.activate
def test_scan_create_scheduled_scan_freq_yearly(tvm):
    """
    test to create scheduled scan with frequency as yearly
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-4ae05b1a-c19d-0969-626b-5242cb54ec3152293e5d7ea3f1a3',
                'name': 'pytest: 3f6f2256-3662-4fc7-8579-77ff160d4555',
                'description': None,
                'policy_id': 59,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': '20210324T123000',
                'rrules': 'FREQ=YEARLY;INTERVAL=2',
                'timezone': 'Etc/UTC',
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1616587296,
                'creation_date': 1616587296,
                'type': 'public',
                'id': 60,
            }
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/60')
    schedule_scan = tvm.scans.create_scan_schedule(
        enabled=True, frequency='yearly', interval=2
    )
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'],
        schedule_scan=schedule_scan,
    )
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)
    assert scan['enabled'] is True
    assert scan['rrules'] == 'FREQ=YEARLY;INTERVAL=2'
    tvm.scans.delete(scan['id'])


# @pytest.mark.vcr()
# def test_scan_delete_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.delete('nope')


@responses.activate
def test_scan_delete_notfounderror(tvm):
    """
    test to raise exception when scan_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scans/0',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scans.delete(0)


@responses.activate
def test_scan_delete(tvm, scan):
    """
    test to delete scan
    """
    responses.add(responses.DELETE, 'https://nourl/scans/221')
    tvm.scans.delete(scan['id'])


# @pytest.mark.vcr()
# def test_scan_delete_history_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.delete_history('nope', 1)

# @pytest.mark.vcr()
# def test_scan_delete_history_history_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.delete_history(1, 'nope')


@responses.activate
def test_scan_delete_history_notfounderror(tvm):
    """
    test to raise exception when scan_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/scans/1/history/1',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scans.delete_history(1, 1)


# @pytest.mark.vcr()
# def test_scan_details_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.details('nope')


def test_scan_details_history_it_typeerror(tvm):
    """
    test to raise exception when type of scan_id param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.details(1, 'nope')


@responses.activate
def test_scan_results(tvm):
    """
    test to get scan results
    """
    responses.add(
        responses.GET,
        'https://nourl/scans',
        json={
            'scans': [
                {
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'permissions': 128,
                    'legacy': False,
                    'type': 'ps',
                    'read': True,
                    'last_modification_date': 1623325148,
                    'creation_date': 1623324252,
                    'status': 'completed',
                    'uuid': 'd84bc6a3-1f0a-42a0-85bb-3470dfeed221',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': 'template-49372206-2970-d2a5-ecf1-8093d80f7470c38367de9cad6f94',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': True,
                    'wizard_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'policy_id': 174,
                    'name': 'pytest-scan',
                    'id': 175,
                }
            ],
            'timestamp': 1624011287,
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175',
        json={
            'info': {
                'owner': 'pytenable_test_user@tenable.com',
                'name': 'pytest-scan',
                'no_target': False,
                'folder_id': 18,
                'control': True,
                'user_permissions': 128,
                'schedule_uuid': 'template-49372206-2970-d2a5-ecf1-8093d80f7470c38367de9cad6f94',
                'edit_allowed': False,
                'scanner_name': 'US Cloud Scanner',
                'policy': 'Basic Network Scan',
                'shared': None,
                'object_id': 175,
                'tag_targets': None,
                'acls': [
                    {
                        'permissions': 0,
                        'owner': None,
                        'display_name': None,
                        'name': None,
                        'uuid': None,
                        'id': None,
                        'type': 'default',
                    }
                ],
                'hostcount': 1,
                'uuid': 'd84bc6a3-1f0a-42a0-85bb-3470dfeed221',
                'status': 'completed',
                'scan_type': 'ps',
                'targets': '162.159.129.83/32',
                'alt_targets_used': False,
                'pci-can-upload': False,
                'scan_start': 1623324252,
                'timestamp': 1623325148,
                'is_archived': False,
                'reindexing': False,
                'scan_end': 1623325148,
                'haskb': True,
                'hasaudittrail': True,
                'scanner_start': None,
                'scanner_end': None,
            },
            'hosts': [
                {
                    'asset_id': 2,
                    'host_id': 2,
                    'uuid': '44d62c42-1539-4c9d-8079-ea2f87120006',
                    'hostname': '162.159.129.83',
                    'progress': '100-100/200-200',
                    'scanprogresscurrent': 100,
                    'scanprogresstotal': 100,
                    'numchecksconsidered': 100,
                    'totalchecksconsidered': 100,
                    'severitycount': {},
                    'severity': 133,
                    'score': 133,
                    'info': 133,
                    'low': 0,
                    'medium': 0,
                    'high': 0,
                    'critical': 0,
                    'host_index': 0,
                }
            ],
            'vulnerabilities': [
                {
                    'count': 13,
                    'plugin_id': 10107,
                    'plugin_name': 'HTTP Server Type and Version',
                    'severity': 0,
                    'plugin_family': 'Web Servers',
                    'vuln_index': 1,
                }
            ],
            'comphosts': [],
            'compliance': [],
            'history': [
                {
                    'history_id': 12164587,
                    'owner_id': 2201492,
                    'creation_date': 1623324252,
                    'last_modification_date': 1623325148,
                    'uuid': 'd84bc6a3-1f0a-42a0-85bb-3470dfeed221',
                    'type': 'ps',
                    'status': 'completed',
                    'scheduler': 0,
                    'alt_targets_used': False,
                    'is_archived': False,
                }
            ],
            'notes': [],
            'remediations': {
                'num_cves': 6,
                'num_hosts': 1,
                'num_remediated_cves': 0,
                'num_impacted_hosts': 0,
                'remediations': [],
            },
        },
    )
    scan_list = [
        id['id']
        for id in list(
            filter(lambda value: value['status'] == 'completed', tvm.scans.list())
        )
    ]
    if scan_list:
        scan_results = tvm.scans.results(scan_list[0])
        assert isinstance(scan_results, dict)
        result = scan_results
        check(result, 'info', dict)
        info = result['info']
        check(info, 'acls', list, allow_none=True)
        if result['info']['acls']:
            for acls in result['info']['acls']:
                check(acls, 'owner', int, allow_none=True)
                check(acls, 'type', str, allow_none=True)
                check(acls, 'permissions', int, allow_none=True)
                check(acls, 'id', int, allow_none=True)
                check(acls, 'name', str, allow_none=True)
                check(acls, 'display_name', str, allow_none=True)
        check(info, 'schedule_uuid', str, allow_none=True)
        check(info, 'edit_allowed', bool)
        check(info, 'status', str)
        check(info, 'alt_targets_used', bool, allow_none=True)
        check(info, 'scanner_start', int, allow_none=True)
        check(info, 'policy', str, allow_none=True)
        check(info, 'pci-can-upload', bool, allow_none=True)
        check(info, 'scan_start', int, allow_none=True)
        check(info, 'hasaudittrail', bool)
        check(info, 'user_permissions', int)
        check(info, 'folder_id', int, allow_none=True)
        check(info, 'no_target', bool)
        check(info, 'owner', str)
        check(info, 'targets', str, allow_none=True)
        check(info, 'control', bool)
        check(info, 'object_id', int, allow_none=True)
        check(info, 'scanner_name', str, allow_none=True)
        check(info, 'uuid', str)
        check(info, 'haskb', bool)
        check(info, 'scanner_end', int, allow_none=True)
        check(info, 'scan_end', int)
        # check(info, 'hostcount', int)
        check(info, 'scan_type', str, allow_none=True)
        check(info, 'name', str)

        check(result, 'comphosts', list)
        if 'comphosts' in result and len(result['comphosts']) > 0:
            for comphosts in result['comphosts']:
                check(comphosts, 'totalchecksconsidered', int)
                check(comphosts, 'numchecksconsidered', int)
                check(comphosts, 'scanprogresstotal', int)
                check(comphosts, 'scanprogresscurrent', int)
                check(comphosts, 'host_index', int)
                check(comphosts, 'score', int)
                check(comphosts, 'severitycount', dict)
                check(comphosts, 'progress', str)
                check(comphosts, 'critical', int)
                check(comphosts, 'high', int)
                check(comphosts, 'medium', int)
                check(comphosts, 'low', int)
                check(comphosts, 'info', int)
                check(comphosts, 'host_id', int)
                check(comphosts, 'hostname', str)

        check(result, 'hosts', list)
        if 'hosts' in result and len(result['hosts']) > 0:
            for hosts in result['hosts']:
                check(hosts, 'totalchecksconsidered', int)
                check(hosts, 'numchecksconsidered', int)
                check(hosts, 'scanprogresstotal', int)
                check(hosts, 'scanprogresscurrent', int)
                check(hosts, 'host_index', int)
                check(hosts, 'score', int)
                check(hosts, 'severitycount', dict)
                check(hosts, 'progress', str)
                check(hosts, 'critical', int)
                check(hosts, 'high', int)
                check(hosts, 'medium', int)
                check(hosts, 'low', int)
                check(hosts, 'info', int)
                check(hosts, 'host_id', int)
                check(hosts, 'hostname', str)

        check(result, 'notes', list)
        if len(result['notes']) > 0:
            for notes in result['notes']:
                check(notes, 'title', str)
                check(notes, 'message', str)
                check(notes, 'severity', int)

        check(result, 'remediations', dict)
        check(result['remediations'], 'num_hosts', int)
        check(result['remediations'], 'num_cves', int)
        check(result['remediations'], 'num_impacted_hosts', int)
        check(result['remediations'], 'num_remediated_cves', int)
        check(result['remediations'], 'remediations', list)

        if len(result['remediations']['remediations']) > 0:
            for remediation in result['remediations']['remediations']:
                check(remediation, 'value', str)
                check(remediation, 'remediation', str)
                check(remediation, 'hosts', int)
                check(remediation, 'vulns', int)

        check(result, 'vulnerabilities', list)
        if 'vulnerabilities' in result and len(result['vulnerabilities']) > 0:
            for vulnerability in result['vulnerabilities']:
                check(vulnerability, 'count', int)
                check(vulnerability, 'plugin_name', str)
                check(vulnerability, 'vuln_index', int)
                check(vulnerability, 'severity', int)
                check(vulnerability, 'plugin_id', int)
                # Mentioned in the docs, however doesn't appear to show in testing
                # check(vulnerability, 'severity_index', int)
                check(vulnerability, 'plugin_family', str)

        check(result, 'history', list)
        for history in result['history']:
            check(history, 'alt_targets_used', bool)
            check(history, 'scheduler', int)
            check(history, 'status', str)
            check(history, 'type', str, allow_none=True)
            check(history, 'uuid', str)
            check(history, 'last_modification_date', int)
            check(history, 'creation_date', int)
            check(history, 'owner_id', int)
            check(history, 'history_id', int)
            check(history, 'is_archived', bool)

        check(result, 'compliance', list)
        if 'compliance' in result and len(result['compliance']) > 0:
            for compliance in result['compliance']:
                check(compliance, 'count', int)
                check(compliance, 'plugin_name', str)
                check(compliance, 'vuln_index', int)
                check(compliance, 'severity', int)
                check(compliance, 'plugin_id', int)
                # Mentioned in the docs, however doesn't appear to show in testing
                # check(compliance, 'severity_index', int)
                check(compliance, 'plugin_family', str)


# @pytest.mark.vcr()
# def test_scan_export_scan_id_typeerror(api):
#    with pytest.raises(TypeError):
#        api.scans.export('nope')


@responses.activate
def test_scan_export_history_id_typeerror(tvm):
    """
    test to raise exception when type of history_id param does not match the expected type.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(TypeError):
        tvm.scans.export(1, history_id='nope')


@responses.activate
def test_scan_export_format_typeerror(tvm):
    """
    test to raise exception when type of format param does not match the expected type.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(TypeError):
        tvm.scans.export(1, format=1)


@responses.activate
def test_scan_export_format_unexpectedvalueerror(tvm):
    """
    test to raise exception when format param value does not match the choices.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(UnexpectedValueError):
        tvm.scans.export(1, format='something else')


@responses.activate
def test_scan_export_password_typeerror(tvm):
    """
    test to raise exception when type of password param does not match the expected type.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(TypeError):
        tvm.scans.export(1, password=1)


@responses.activate
def test_scan_export_chapters_typeerror(tvm):
    """
    test to raise exception when type of chapter param does not match the expected type.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(TypeError):
        tvm.scans.export(1, chapters=1)


@responses.activate
def test_scan_export_chapters_unexpectedvalueerror(tvm):
    """
    test to raise exception when chapter param value does not match the choices.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(UnexpectedValueError):
        tvm.scans.export(1, chapters=['nothing to see here'])


@responses.activate
def test_scan_export_filter_type_typeerror(tvm):
    """
    test to raise exception when type of filter_type param does not match the expected type.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(TypeError):
        tvm.scans.export(1, filter_type=1)


@responses.activate
def test_scan_export_filter_type_unexpectedvalueerror(tvm):
    """
    test to raise exception when filter_type param value does not match the choices.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(UnexpectedValueError):
        tvm.scans.export(1, filter_type='nothing')


@responses.activate
def test_scan_export_was_typeerror(tvm):
    """
    test to raise exception when scan_type param value does not match the choices.
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    with pytest.raises(UnexpectedValueError):
        tvm.scans.export(SCAN_ID_WITH_RESULTS, scan_type='bad-value')


@responses.activate
def test_scan_export_bytesio_stream_hook(tvm, scan_results):
    """
    test to export scan using optional `stream_hook` kwarg, provided by user (Issue #305)
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    responses.add(
        responses.POST,
        'https://nourl/scans/175/export',
        json={'file': 'SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/status',
        json={'status': 'ready'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/download',
        body=NESSUS_REPORT,
        content_type='application/octet-stream',
        headers={'Content-Disposition': 'attachment; filename=pytest-scan.nessus'},
    )

    def stream_hook(response, _fobj, chunk_size=1024):
        """This is an example callable, the caller provides this"""
        progress_bytes = 0
        total_size = int(response.headers.get('content-length', 0))
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                progress_bytes += len(chunk)
                stdout.write('Progress: %d / %d\n' % (progress_bytes, total_size))
                _fobj.write(chunk)
        stdout.write(
            'Complete, %d/%d bytes received in stream_hook\n'
            % (progress_bytes, total_size)
        )

    fobj = tvm.scans.export(scan_results['id'], stream_hook=stream_hook)
    assert isinstance(fobj, BytesIO)

    counter = 0
    for _ in NessusReportv2(fobj):
        counter += 1
        if counter > 10:
            break


@responses.activate
def test_scan_export_bytesio(tvm):
    """
    test to export scan
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scans',
        json={
            'scans': [
                {
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'permissions': 128,
                    'legacy': False,
                    'type': 'ps',
                    'read': True,
                    'last_modification_date': 1623325148,
                    'creation_date': 1623324252,
                    'status': 'completed',
                    'uuid': 'd84bc6a3-1f0a-42a0-85bb-3470dfeed221',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': 'template-49372206-2970-d2a5-ecf1-8093d80f7470c38367de9cad6f94',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': True,
                    'wizard_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'policy_id': 174,
                    'name': 'pytest-scan',
                    'id': 175,
                }
            ],
            'timestamp': 1624011165,
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/scans/175/export',
        json={'file': 'SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/status',
        json={'status': 'ready'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/download',
        body=NESSUS_REPORT,
        content_type='application/octet-stream',
        headers={'Content-Disposition': 'attachment; filename=pytest-scan.nessus'},
    )
    scan_list = [
        id['id']
        for id in list(
            filter(lambda value: value['status'] == 'completed', tvm.scans.list())
        )
    ]
    if scan_list:
        fobj = tvm.scans.export(scan_list[0])
        assert isinstance(fobj, BytesIO)

        counter = 0
        for _ in NessusReportv2(fobj):
            counter += 1
            if counter > 10:
                break


@responses.activate
def test_scan_export_file_object(tvm):
    """
    test to export scan file object
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scans',
        json={
            'scans': [
                {
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'permissions': 128,
                    'legacy': False,
                    'type': 'ps',
                    'read': True,
                    'last_modification_date': 1623325148,
                    'creation_date': 1623324252,
                    'status': 'completed',
                    'uuid': 'd84bc6a3-1f0a-42a0-85bb-3470dfeed221',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': 'template-49372206-2970-d2a5-ecf1-8093d80f7470c38367de9cad6f94',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': True,
                    'wizard_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'policy_id': 174,
                    'name': 'pytest-scan',
                    'id': 175,
                }
            ],
            'timestamp': 1624011151,
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/scans/175/export',
        json={'file': 'SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/status',
        json={'status': 'ready'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/download',
        body=NESSUS_REPORT,
        content_type='application/octet-stream',
        headers={'Content-Disposition': 'attachment; filename=pytest-scan.nessus'},
    )
    scan_list = [
        id['id']
        for id in list(
            filter(lambda value: value['status'] == 'completed', tvm.scans.list())
        )
    ]
    if scan_list:
        filename = '{}.nessus'.format(uuid.uuid4())
        with open(filename, 'wb') as fobj:
            tvm.scans.export(scan_list[0], fobj=fobj)

        with open(filename, 'rb') as fobj:
            counter = 0
            for _ in NessusReportv2(fobj):
                counter += 1
                if counter > 10:
                    break
        os.remove(filename)


@responses.activate
def test_scan_host_details_notfounderror(tvm):
    """
    test to raise exception when scan_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/1/hosts/1',
        json={'error': 'The requested file was not found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.scans.host_details(1, 1)


@responses.activate
def test_scan_host_details(tvm, scan_results):
    """
    test to retrieve the host details from a specific scan
    """
    responses.add(responses.GET, 'https://nourl/scans/175/hosts/2', json=SCANS_HOSTS)
    try:
        host = tvm.scans.host_details(
            scan_results['id'], scan_results['results']['hosts'][0]['asset_id']
        )
        assert isinstance(host, dict)
        check(host, 'info', dict)
        check(host['info'], 'host-fqdn', str, allow_none=True)
        check(host['info'], 'host_end', str)
        check(host['info'], 'host_start', str)
        check(host['info'], 'operating-system', list, allow_none=True)
        check(host['info'], 'host-ip', str)
        check(host['info'], 'mac-address', str, allow_none=True)

        check(host, 'vulnerabilities', list)
        for vulnerability in host['vulnerabilities']:
            check(vulnerability, 'count', int)
            check(vulnerability, 'severity', int)
            check(vulnerability, 'plugin_family', str)
            check(vulnerability, 'hostname', str)
            check(vulnerability, 'plugin_name', str)
            check(vulnerability, 'severity_index', int)
            check(vulnerability, 'vuln_index', int)
            check(vulnerability, 'host_id', int)
            check(vulnerability, 'plugin_id', int)

        check(host, 'compliance', list)
        for compliance in host['compliance']:
            check(compliance, 'count', int)
            check(compliance, 'plugin_name', str)
            check(compliance, 'vuln_index', int)
            check(compliance, 'severity', int)
            check(compliance, 'plugin_id', int)
            check(compliance, 'severity_index', int)
            check(compliance, 'plugin_family', str)
    except KeyError as key:
        log_exception(key)
        print('Key error: ', key)


def test_scan_import_scan_folder_id_typeerror(tvm):
    """
    test to raise exception when type of folder_id param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.import_scan(None, folder_id='nope')


def test_scan_import_scan_password_typeerror(tvm):
    """
    test to raise exception when type of password param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.scans.import_scan(None, password=1)


@responses.activate
def test_scan_import_scan(tvm):
    """
    test to import scan
    """
    responses.add(
        responses.GET, 'https://nourl/filters/scans/reports', json=FILTERS_SCANS_REPORTS
    )
    responses.add(
        responses.GET,
        'https://nourl/scans',
        json={
            'scans': [
                {
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'permissions': 128,
                    'legacy': False,
                    'type': 'ps',
                    'read': True,
                    'last_modification_date': 1623325148,
                    'creation_date': 1623324252,
                    'status': 'completed',
                    'uuid': 'd84bc6a3-1f0a-42a0-85bb-3470dfeed221',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': 'template-49372206-2970-d2a5-ecf1-8093d80f7470c38367de9cad6f94',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': True,
                    'wizard_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'policy_id': 174,
                    'name': 'pytest-scan',
                    'id': 175,
                }
            ],
            'timestamp': 1624011101,
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/scans/175/export',
        json={'file': 'SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/status',
        json={'status': 'ready'},
    )
    responses.add(
        responses.GET,
        'https://nourl/scans/175/export/SSE-d84bc6a3-1f0a-42a0-85bb-3470dfeed221-nessus/download',
        body=NESSUS_REPORT,
        content_type='application/octet-stream',
        headers={'Content-Disposition': 'attachment; filename=pytest-scan.nessus'},
    )
    responses.add(
        responses.POST, 'https://nourl/file/upload', json={'fileuploaded': 'Filedata'}
    )
    responses.add(
        responses.POST,
        'https://nourl/scans/import',
        json={
            'scan': {
                'timezone': None,
                'id': 286,
                'last_modification_date': 1624011108,
                'status': 'imported',
                'user_permissions': 128,
                'folder_id': None,
                'owner': 'pytenable_test_user@tenable.com',
                'control': None,
                'starttime': None,
                'uuid': '711bc471-0fc4-f3e6-1739-3d92a0726d786ebb0ee48db711e1',
                'rrules': None,
                'creation_date': 1624011108,
                'read': False,
                'name': 'pytest-scan',
                'shared': False,
            }
        },
        match=[matchers.query_param_matcher({'include_aggregate': '1'})],
    )
    scan_list = [
        id['id']
        for id in list(
            filter(lambda value: value['status'] == 'completed', tvm.scans.list())
        )
    ]
    if scan_list:
        fobj = tvm.scans.export(scan_list[0])
        tvm.scans.import_scan(fobj)


@pytest.mark.skip(reason='Switching between scan states can be tricky')
def test_scan_launch(tvm, scan):
    """
    test to launch scan
    """
    tvm.scans.launch(scan['id'])
    time.sleep(5)
    tvm.scans.stop(scan['id'], block=True)


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
def test_scan_launch_alt_targets(tvm, scan):
    """
    test to launch scan
    """
    tvm.scans.launch(scan['id'], targets=['127.0.0.2'])
    time.sleep(5)
    tvm.scans.stop(scan['id'], block=True)


@responses.activate
def test_scan_list(tvm):
    """
    test to get list of scans
    """
    responses.add(
        responses.GET,
        'https://nourl/scans',
        json={
            'scans': [
                {
                    'legacy': False,
                    'permissions': 128,
                    'type': None,
                    'read': False,
                    'last_modification_date': 1539119706,
                    'creation_date': 1539119706,
                    'status': 'imported',
                    'uuid': '150a7972-9e3e-61b5-9b82-0fe39f9f349c93bd4df29d1bae9e',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'test_admin@pytenable.io',
                    'schedule_uuid': '6b66d30f-b790-e55b-0645-894c424ae5eb714aa20b722ee6d6',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': False,
                    'name': 'Office - Network Scan - Auth',
                    'id': 7171,
                }
            ],
            'timestamp': 1544138532,
        },
    )
    scans = tvm.scans.list()
    assert isinstance(scans, list)
    scan = scans[0]
    check(scan, 'control', bool)
    check(scan, 'creation_date', int)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'legacy', bool)
    check(scan, 'owner', str)
    check(scan, 'name', str)
    check(scan, 'permissions', int)
    check(scan, 'read', bool)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'schedule_uuid', 'scanner-uuid')
    check(scan, 'shared', bool)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'status', str)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', 'scanner-uuid')


@pytest.mark.skip(reason='Switching between scan states can be tricky')
def test_scan_pause_scan(tvm, scan):
    """
    test to pause scan
    """
    _ = tvm.scans.launch(scan['id'])
    tvm.scans.pause(scan['id'], block=True)


@responses.activate
def test_scan_plugin_output(tvm, scan_results):
    """
    test to get scan plugin output
    """
    responses.add(responses.GET, 'https://nourl/scans/175/hosts/2', json=SCANS_HOSTS)
    responses.add(
        responses.GET,
        'https://nourl/scans/175/hosts/2/plugins/10107',
        json={
            'outputs': [
                {
                    'ports': {'2087 / tcp / www': [{'hostname': '162.159.129.83'}]},
                    'has_attachment': 0,
                    'severity': 0,
                    'plugin_output': 'The remote web server type is :\n\ncloudflare',
                    'hosts': None,
                    'custom_description': None,
                }
            ],
            'info': {
                'plugindescription': {
                    'severity': 0,
                    'pluginname': 'HTTP Server Type and Version',
                    'pluginattributes': {
                        'synopsis': 'A web server is running on the remote host.',
                        'description': 'This plugin attempts to determine the type and the version of the   remote web server.',
                        'risk_information': {
                            'risk_factor': 'None',
                            'cvss3_temporal_score': '0.0',
                            'cvss_base_score': '0.0',
                            'cvss_temporal_score': '0.0',
                            'cvss3_base_score': '0.0',
                        },
                        'see_also': None,
                        'has_patch': False,
                        'plugin_information': {
                            'plugin_version': '1.141',
                            'plugin_id': 10107,
                            'plugin_type': 'remote',
                            'plugin_publication_date': '2000-01-04T00:00:00Z',
                            'plugin_family': 'Web Servers',
                            'plugin_modification_date': '2020-10-30T00:00:00Z',
                        },
                        'solution': None,
                    },
                    'pluginfamily': 'Web Servers',
                    'pluginid': '10107',
                }
            },
        },
    )
    try:
        host = tvm.scans.host_details(
            scan_results['id'], scan_results['results']['hosts'][0]['asset_id']
        )
        output = tvm.scans.plugin_output(
            scan_results['id'],
            host['vulnerabilities'][0]['host_id'],
            host['vulnerabilities'][0]['plugin_id'],
        )
        output_info_pdesc = output['info']['plugindescription']
        output_info_pdesc_patt = output_info_pdesc['pluginattributes']
        output_info_pdesc_patt_pinfo = output_info_pdesc['pluginattributes'][
            'plugin_information'
        ]
        assert isinstance(output, dict)
        check(output, 'info', dict)
        check(output['info'], 'plugindescription', dict)
        check(output_info_pdesc, 'pluginattributes', dict)
        check(output_info_pdesc, 'pluginfamily', str)
        check(output_info_pdesc, 'pluginid', str)
        check(output_info_pdesc, 'pluginname', str)
        check(output_info_pdesc, 'severity', int)
        check(output_info_pdesc_patt, 'description', str)
        check(output_info_pdesc_patt, 'has_patch', bool)
        check(output_info_pdesc_patt, 'plugin_information', dict)
        check(output_info_pdesc_patt_pinfo, 'plugin_family', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_id', int)
        check(output_info_pdesc_patt_pinfo, 'plugin_modification_date', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_publication_date', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_type', str)
        check(output_info_pdesc_patt_pinfo, 'plugin_version', str)
        check(output_info_pdesc_patt, 'risk_information', dict)
        check(output_info_pdesc_patt['risk_information'], 'risk_factor', str)
        check(output_info_pdesc_patt, 'solution', str, allow_none=True)
        check(output_info_pdesc_patt, 'synopsis', str, allow_none=True)

        check(output, 'outputs', list)
        for data in output['outputs']:
            check(data, 'has_attachment', int)
            check(data, 'hosts', list, allow_none=True)
            check(data, 'plugin_output', str, allow_none=True)
            check(data, 'ports', dict)
            for port in data['ports']:
                check(data['ports'], port, list)
                for port_detail in data['ports'][port]:
                    check(port_detail, 'hostname', str)
            check(data, 'severity', int)
    except KeyError as error:
        log_exception(error)
        print('Invalid key', error)


@responses.activate
def test_scan_read_status(tvm, scan):
    """
    test to get scan read status
    """
    responses.add(
        responses.GET,
        'https://nourl/scans',
        json={
            'scans': [
                {
                    'legacy': False,
                    'permissions': 128,
                    'type': None,
                    'read': False,
                    'last_modification_date': 1539119706,
                    'creation_date': 1539119706,
                    'status': 'imported',
                    'uuid': '150a7972-9e3e-61b5-9b82-0fe39f9f349c93bd4df29d1bae9e',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': '6b66d30f-b790-e55b-0645-894c424ae5eb714aa20b722ee6d6',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': False,
                    'name': 'Office - Network Scan - Auth',
                    'id': 7171,
                }
            ],
            'timestamp': 1544138536,
        },
    )
    responses.add(responses.PUT, 'https://nourl/scans/7171/status')
    responses.add(
        responses.GET,
        'https://nourl/scans',
        json={
            'folders': [
                {
                    'unread_count': 48,
                    'custom': 0,
                    'default_tag': 0,
                    'type': 'trash',
                    'name': 'Trash',
                    'id': 10,
                },
                {
                    'unread_count': 104,
                    'custom': 0,
                    'default_tag': 1,
                    'type': 'main',
                    'name': 'My Scans',
                    'id': 11,
                },
            ],
            'scans': [
                {
                    'legacy': False,
                    'permissions': 128,
                    'type': None,
                    'read': True,
                    'last_modification_date': 1539119706,
                    'creation_date': 1539119706,
                    'status': 'imported',
                    'uuid': '150a7972-9e3e-61b5-9b82-0fe39f9f349c93bd4df29d1bae9e',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': '6b66d30f-b790-e55b-0645-894c424ae5eb714aa20b722ee6d6',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': False,
                    'name': 'Office - Network Scan - Auth',
                    'id': 7171,
                },
                {
                    'legacy': False,
                    'permissions': 128,
                    'type': None,
                    'read': False,
                    'last_modification_date': 1538748904,
                    'creation_date': 1538748904,
                    'status': 'imported',
                    'uuid': '1e6e8542-ffcc-7a22-700d-1e6fcc9f86085abfcd7e430ba18d',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': 'cc40d7e1-3370-7fbf-453e-5002e43f93b0817a945ddd82ff82',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': False,
                    'name': 'Office - Network Scan - Auth',
                    'id': 6923,
                },
                {
                    'legacy': False,
                    'permissions': 128,
                    'type': 'ps',
                    'read': True,
                    'last_modification_date': 1538516758,
                    'creation_date': 1538516623,
                    'status': 'canceled',
                    'uuid': '96711c3b-11f5-4d59-b64b-256a74081650',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': 'template-81690036-99b8-88a1-0e0d-42fcfd9ca0a3cb902f3afa3ad22b',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': True,
                    'control': True,
                    'name': 'pytest: 34b2d6ea-deca-4690-a019-f1047559dd9a',
                    'id': 4354,
                },
                {
                    'legacy': False,
                    'permissions': 128,
                    'type': None,
                    'read': False,
                    'last_modification_date': 1539644478,
                    'creation_date': 1539644478,
                    'status': 'imported',
                    'uuid': '987cd189-c12b-136b-9b6d-df7c558b515ea65721465965f785',
                    'shared': False,
                    'user_permissions': 128,
                    'owner': 'pytenable_test_user@tenable.com',
                    'schedule_uuid': 'cac3111a-85d1-e1b9-adee-f55c03a8b064d4d56d3b18f6744b',
                    'timezone': None,
                    'rrules': None,
                    'starttime': None,
                    'enabled': False,
                    'control': False,
                    'name': 'Office - Network Scan - Auth',
                    'id': 7729,
                },
            ],
            'timestamp': 1544138537,
        },
    )
    scans = tvm.scans.list()
    scan = scans[0]
    tvm.scans.set_read_status(scans[0]['id'], not scans[0]['read'])
    for resp in tvm.scans.list():
        if resp['id'] == scan['id']:
            assert scan['read'] != resp['read']


@pytest.mark.skip(reason='Switching between scan states can be tricky')
def test_scan_resume(tvm, scan):
    """
    test to resume scan
    """
    tvm.scans.launch(scan['id'])
    time.sleep(5)
    tvm.scans.pause(scan['id'], block=True)
    time.sleep(5)
    tvm.scans.resume(scan['id'])
    time.sleep(5)
    tvm.scans.stop(scan['id'], block=True)


@pytest.mark.skip(reason='Need to configure the scan w/ a schedule.')
def test_scan_schedule(tvm, scan):
    """
    test to disable scan schedule
    """
    tvm.scans.schedule(scan['id'], False)


@pytest.mark.skip(reason='Switching between scan states can be tricky')
def test_scan_stop(tvm, scan):
    """
    test to stop scan
    """
    tvm.scans.launch(scan['id'])
    time.sleep(5)
    tvm.scans.stop(scan['id'])


@responses.activate
def test_scan_status(tvm, scan):
    """
    test to check scan status
    """
    responses.add(
        responses.GET, 'https://nourl/scans/221/latest-status', json={'status': 'empty'}
    )
    status = tvm.scans.status(scan['id'])
    single(status, str)


@responses.activate
def test_scan_timezones(tvm):
    """
    test to get list of allowed timezone strings
    """
    responses.add(responses.GET, 'https://nourl/scans/timezones', json=SCANS_TIMEZONES)
    assert isinstance(tvm.scans.timezones(), list)


@responses.activate
def test_scan_check_auto_targets_success(tvm):
    """
    test to evaluates a list of targets and/or tags against
    the scan route configuration of scanner groups
    """
    responses.add(
        responses.POST,
        'https://nourl/scans/check-auto-targets',
        json={
            'missed_targets': ['127.0.0.1'],
            'total_missed_targets': 1,
            'matched_resource_uuids': [],
            'total_matched_resource_uuids': 0,
        },
        match=[
            matchers.query_param_matcher({'limit': '10', 'matched_resource_limit': '5'})
        ],
    )
    resp = tvm.scans.check_auto_targets(10, 5, targets=['127.0.0.1'])
    assert isinstance(resp, dict)
    check(resp, 'matched_resource_uuids', list)
    check(resp, 'missed_targets', list)
    check(resp, 'total_matched_resource_uuids', int)
    check(resp, 'total_missed_targets', int)


def test_scan_create_scan_schedule_success(tvm):
    """test to create a scan schedule"""
    tvm.scans.create_scan_schedule(enabled=False)


@responses.activate
def test_scan_create_scan_success(tvm):
    """
    test to create a scan
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json=EDITOR_POLICY_TEMPLATES,
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-5c5743c6-adce-33fb-cddf-9af8e8549f83ae8e48a6a19f3219',
                'name': 'pytest: 88d49b04-6a92-42cd-9e15-0ac20085fed2',
                'description': None,
                'policy_id': 261,
                'scanner_id': None,
                'scanner_uuid': '00000000-0000-0000-0000-00000000000000000000000000001',
                'emails': None,
                'sms': '',
                'enabled': True,
                'include_aggregate': True,
                'scan_time_window': None,
                'custom_targets': '127.0.0.1',
                'target_network_uuid': None,
                'auto_routed': 0,
                'remediation': 0,
                'starttime': None,
                'rrules': None,
                'timezone': None,
                'notification_filters': None,
                'shared': 0,
                'user_permissions': 128,
                'default_permissions': 0,
                'owner': 'pytenable_test_user@tenable.com',
                'owner_id': 2201492,
                'last_modification_date': 1623992910,
                'creation_date': 1623992910,
                'type': 'public',
                'id': 262,
            }
        },
    )
    scan = tvm.scans.create(
        name='pytest: {}'.format(uuid.uuid4()), targets=['127.0.0.1']
    )
    assert isinstance(scan, dict)
    check(scan, 'tag_type', None, allow_none=True)
    check(scan, 'container_id', 'uuid')
    check(scan, 'owner_uuid', 'uuid')
    check(scan, 'uuid', str)
    check(scan, 'name', str)
    check(scan, 'description', None, allow_none=True)
    check(scan, 'policy_id', int)
    check(scan, 'scanner_id', None, allow_none=True)
    check(scan, 'scanner_uuid', str)
    check(scan, 'emails', None, allow_none=True)
    check(scan, 'sms', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'include_aggregate', bool)
    check(scan, 'scan_time_window', None, allow_none=True)
    check(scan, 'custom_targets', str)
    check(scan, 'target_network_uuid', None, allow_none=True)
    check(scan, 'rrules', None, allow_none=True)
    check(scan, 'default_permissions', int)
    check(scan, 'timezone', None, allow_none=True)
    check(scan, 'notification_filters', None, allow_none=True)
    check(scan, 'auto_routed', int)
    check(scan, 'remediation', int)
    check(scan, 'user_permissions', int)
    check(scan, 'starttime', None, allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'creation_date', int)
    check(scan, 'type', str)
    check(scan, 'id', int)


@responses.activate
def test_scan_create_scan_document_policy_setting_valueerror(tvm):
    """
    test to raise when policy setting is invalid
    """
    responses.add(
        responses.GET,
        'https://nourl/policies',
        json={
            'policies': [
                {
                    'no_target': 'false',
                    'template_uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                    'description': None,
                    'name': 'c3e9fec8-0676-43cb-9128-48bca2b45d07',
                    'owner': 'pytenable_test_user@tenable.com',
                    'visibility': 'private',
                    'shared': 0,
                    'user_permissions': 128,
                    'last_modification_date': 1623213793,
                    'creation_date': 1623213793,
                    'owner_id': 2201492,
                    'id': 154,
                }
            ]
        },
    )
    with pytest.raises(UnexpectedValueError):
        getattr(tvm.scans, '_create_scan_document')({'policy': 'some_policy'})


@responses.activate
def test_scan_create_scan_document_credentials_pass(tvm):
    """
    test to create a scan document along with credentials
    """
    responses.add(
        responses.GET,
        'https://nourl/credentials',
        json={
            'credentials': [],
            'pagination': {
                'total': 0,
                'limit': 50,
                'offset': 0,
                'sort': [{'name': 'created_date', 'order': 'desc'}],
            },
        },
        match=[matchers.query_param_matcher({'limit': '50', 'offset': '0'})],
    )
    credentials = tvm.credentials.list()
    for credential in credentials:
        getattr(tvm.scans, '_create_scan_document')({'credentials': credential})


@responses.activate
def test_block_while_running(tvm):
    """
    test _block_while_running with expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/583',
        json={
            'info': {
                'owner': 'triage_musikaar@tenable.com',
                'name': 'LabTargetsScan',
                'no_target': False,
                'folder_id': 581,
                'control': False,
                'user_permissions': 128,
                'schedule_uuid': '6f9ecccc-eddd-d6d9-dc7c-8cf75b33d1d796d102cc47a40400',
                'edit_allowed': False,
                'scanner_name': None,
                'policy': None,
                'shared': None,
                'object_id': 583,
                'tag_targets': None,
                'uuid': '9477d719-0062-a90b-0583-efd953e444844ed0a28e93c665e3',
                'status': 'imported',
                'scan_type': None,
                'targets': None,
                'alt_targets_used': None,
                'pci-can-upload': None,
                'scan_start': 1613578190,
                'timestamp': 1613578190,
                'is_archived': True,
                'reindexing': False,
                'scan_end': 1613578190,
                'haskb': False,
                'hasaudittrail': False,
                'scanner_start': None,
                'scanner_end': None,
            }
        },
    )
    tvm.scans._block_while_running(scan_id=583, sleeper=5)


@responses.activate
def test_scan_results_scan_not_found_error(tvm):
    """
    test to raise exception when scan not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/583',
        json={'error': 'Scan not found'},
        status=404,
        match=[
            matchers.query_param_matcher(
                {'history_id': '123e4567-e89b-12d3-a456-426614174000'}
            )
        ],
    )
    with pytest.raises(NotFoundError) as not_found_error:
        tvm.scans.results(
            scan_id=583, history_uuid='123e4567-e89b-12d3-a456-426614174000'
        )
    assert 'Scan not found' in not_found_error.value.msg, (
        'Invalid type validation error for scan_id parameter is not raised by test-case.'
    )


@responses.activate
def test_scan_results_without_history(tvm):
    """
    requests using only Scan ID
    """
    responses.add(responses.GET, 'https://nourl/scans/419', json=SCANS)
    scan = tvm.scans.results(scan_id=419)
    assert len(scan['vulnerabilities']) == 2


@responses.activate
def test_scan_results_with_history_id(tvm):
    """
    requests using only Scan ID
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/419',
        json=SCANS,
        match=[matchers.query_param_matcher({'history_id': '15184619'})],
    )
    scan = tvm.scans.results(scan_id=419, history_id=15184619)
    assert len(scan['hosts']) == 1


@responses.activate
def test_scan_results_with_history_uuid(tvm):
    """
    requests using only Scan ID
    """
    responses.add(
        responses.GET,
        'https://nourl/scans/419',
        json=SCANS,
        match=[
            matchers.query_param_matcher(
                {'history_id': 'b6e2280a-119f-42c8-9af5-a16ae269fb75'}
            )
        ],
    )
    scan = tvm.scans.results(
        scan_id=419, history_uuid='b6e2280a-119f-42c8-9af5-a16ae269fb75'
    )
    assert len(scan['hosts']) == 1


def test_scan_history_sort_direction(tvm):
    """
    test scan history for sort direction.
    """
    tvm.scans.history(
        scan_id=11,
        limit=10,
        offset='1',
        pages=3,
        sort=(('name', 'asc'), ('description', 'desc')),
    )


def test_scan_create_scan_document_credentials_compliance_plugins(tvm):
    """
    test to create scan document with credentials, compliance and plugins
    """
    getattr(tvm.scans, '_create_scan_document')(
        {
            'credentials': {
                'Host': {
                    'Windows': [
                        {
                            'domain': '',
                            'username': 'test',
                            'password': 'test',
                            'auth_method': 'Password',
                        }
                    ]
                }
            },
            'compliance': {'test': 'testvalue'},
            'plugins': {12122: 13, 12050: 13},
        }
    )


@responses.activate
def test_list_api():
    dt = datetime.datetime(2024, 1, 1)
    dt_int = int(time.mktime(dt.timetuple()))
    responses.get(
        'https://nourl/scans',
        json={'scans': []},
        match=[query_param_matcher({'last_modification_date': dt_int, 'folder_id': 1})],
    )
    tvm = TenableIO(url='https://nourl', access_key='something', secret_key='something')
    assert tvm.scans.list(folder_id=1, last_modified=dt) == []
    assert tvm.scans.list(folder_id=1, last_modified=dt_int) == []
