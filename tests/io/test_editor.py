"""
test editor
"""

import uuid

import pytest
import responses

from tenable.base.endpoint import APIEndpoint
from tenable.errors import NotFoundError

###
### As the editor endpoints are really meant to drive the UI, the tests here
### are mostly focused on checking the error conditions for the endpoints that
### were exposed in the API documentation to verify that we will be sending
### clean data to the API.  We will NOT be making any calls here, except
### for the list command.
###


@responses.activate
def test_editor_template_list(tvm):
    """test to get template list"""
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/templates',
        json={
            'templates': [
                {
                    'name': 'basic',
                    'title': 'Basic Network Scan',
                    'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65',
                }
            ]
        },
    )
    items = tvm.editor.template_list('scan')
    assert isinstance(items, list)
    assert items[0]['name'] == 'basic'


def test_editor_parse_creds(tvm):
    """test to parse creds"""
    data = [
        {
            'types': [
                {
                    'instances': [
                        {
                            'id': 12,
                            'type': 'entry',
                            'modes': 'nothing',
                            'summary': 'sample1',
                        },
                        {'id': 34, 'default': 145, 'summary': 'sample2'},
                    ],
                    'name': 'Josh',
                }
            ],
            'name': 'Joseph',
        },
        {
            'types': [
                {
                    'instances': [
                        {
                            'id': 12,
                            'type': 'entry',
                            'modes': 'nothing',
                            'summary': 'sample3',
                        },
                        {'id': 34, 'summary': 'sample4', 'default': 145},
                    ],
                    'name': 'Dale',
                }
            ],
            'name': 'David',
        },
    ]

    tvm.editor.parse_creds(data)


def test_editor_parse_audits(tvm):
    """test to parse audits"""
    data = [
        {
            'audits': [
                {'free': 0, 'type': 'custom', 'summary': 'File: file1', 'id': 1}
            ],
            'name': 'Josh',
        },
        {
            'audits': [
                {'free': 0, 'type': 'Nothing', 'summary': 'File: file2', 'id': 2}
            ],
            'name': 'Leo',
        },
    ]
    tvm.editor.parse_audits(data)


@responses.activate
def test_editor_details(tvm):
    """
    test the details of the editor for the given scan_id
    """
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/templates',
        json={
            'templates': [
                {
                    'name': 'advanced',
                    'title': 'Advanced Network Scan',
                    'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
                }
            ]
        },
    )
    responses.add(
        responses.POST,
        'https://nourl/scans',
        json={
            'scan': {
                'tag_type': None,
                'container_id': 'd8631403-ed95-4aa9-9137-e691b6dc3b4e',
                'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
                'uuid': 'template-eb597c22-abfc-8199-5a8e-a7a88b5f4b18a98bfecf267a1bf9',
                'name': 'pytest: d4e6e596-3c2b-4cf6-a02f-9c9c17048907',
                'description': None,
                'policy_id': 453,
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
                'last_modification_date': 1624371108,
                'creation_date': 1624371108,
                'type': 'public',
                'id': 454,
            }
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/scan/454',
        json={
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
            'compliance': {
                'data': [
                    {
                        'name': 'Adtran AOS',
                        'settings': {
                            'compliance': {
                                'inputs': None,
                                'title': 'Compliance Auditing',
                                'groups': [
                                    {
                                        'inputs': None,
                                        'title': 'Adtran AOS',
                                        'name': 'adtran',
                                        'sections': [
                                            {
                                                'inputs': [
                                                    {
                                                        'type': 'file',
                                                        'name': 'AOS config file(s)',
                                                        'id': 'adtran_aos_offline_configs',
                                                    }
                                                ],
                                                'desc': 'Upload an Adtran AOS configuration file to audit. A single configuration file should be uploaded as a .txt file.  Multip',
                                                'title': 'Offline Configuration Auditing',
                                                'name': 'offline',
                                            }
                                        ],
                                    }
                                ],
                            }
                        },
                        'offline_allowed': True,
                        'audits': [
                            {
                                'type': 'custom',
                                'name': '(Upload a custom Adtran AOS audit file)',
                                'free': 1,
                                'unlimited': True,
                            }
                        ],
                    }
                ]
            },
            'is_was': None,
            'user_permissions': 128,
            'is_agent': None,
            'owner': 'pytenable_test_user@tenable.com',
            'title': 'Advanced Network Scan',
            'uuid': 'ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66',
            'plugins': {
                'families': {'Backdoors': {'count': 121, 'id': 9, 'status': 'enabled'}}
            },
            'settings': {
                'basic': {
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
                'report': {
                    'inputs': None,
                    'modes': {'default': 'Custom'},
                    'title': 'Report',
                },
            },
            'name': 'advanced',
        },
    )
    responses.add(responses.DELETE, 'https://nourl/scans/454')
    flag = True
    scan_ids_list = []
    while flag:
        scan_id = tvm.scans.create(
            name='pytest: {}'.format(uuid.uuid4()),
            template='advanced',
            targets=['127.0.0.1'],
        )['id']
        scan_ids_list.append(scan_id)
        editor_details = tvm.editor.obj_details('scan', scan_id)
        if 'compliance' in editor_details and 'plugins' in editor_details:
            tvm.editor.details('scan', scan_id)
            flag = False
    for each_scan_id in scan_ids_list:
        tvm.scans.delete(each_scan_id)


def test_editor_parse_plugins_family_id_keyerror(tvm):
    """test to raise the exception when family id not found"""
    families = {'family': {'status': 'mixed'}}
    with pytest.raises(KeyError) as key_error:
        tvm.editor.parse_plugins('policy', families, 'uuid')
    assert 'id' in key_error.value.args[0], (
        'Validation is not raised in case of family id is not provided.'
    )


@responses.activate
def test_editor_parse_plugins_notfounderror(tvm):
    """test to raise the exception when found unknown policy id"""
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/28/families/1',
        json={'error': 'Unknown policy ID: 28.'},
        status=404,
    )
    families = {
        'family': {'id': 1, 'status': 'mixed'},
    }
    with pytest.raises(NotFoundError) as not_found_error:
        tvm.editor.parse_plugins('policy', families, 28)
    assert 'Unknown policy ID: 28' in not_found_error.value.msg, (
        'Validation is not raised in case of invalid policy id is provided.'
    )


@responses.activate
def test_editor_parse_plugins_response(tvm):
    """test to parse_plugins method"""
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/112/families/28',
        json={
            'plugins': [
                {'status': 'enabled', 'name': 'AIX 5.1 : IY19744', 'id': 22372},
                {'status': 'enabled', 'name': 'AIX 5.1 : IY20486', 'id': 22373},
            ]
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/112/families/30',
        json={
            'plugins': [
                {
                    'status': 'enabled',
                    'name': 'AlmaLinux 8 : .NET 5.0 (ALSA-2021:3819)',
                    'id': 157673,
                },
                {
                    'status': 'enabled',
                    'name': 'AlmaLinux 8 : .NET 5.0 (ALSA-2022:0495)',
                    'id': 158849,
                },
            ]
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/editor/policy/112/families/27',
        json={
            'plugins': [
                {
                    'status': 'enabled',
                    'name': 'Adtran AOS Compliance Checks',
                    'id': 71991,
                },
                {
                    'status': 'enabled',
                    'name': 'Alcatel TiMOS Compliance Checks',
                    'id': 102730,
                },
            ]
        },
    )
    families = {
        0: {
            'count': 11459,
            'id': 28,
            'name': 'AIX Local Security Checks',
            'status': 'mixed',
        },
        1: {
            'count': 360,
            'id': 30,
            'name': 'Alma Linux Local Security Checks',
            'status': 'mixed',
        },
        2: {'count': 60, 'id': 27, 'name': 'Policy Compliance', 'status': 'mixed'},
    }
    endpoint_obj = APIEndpoint(tvm)

    tvm.editor.parse_plugins(
        endpoint_obj._check(
            name='etype', obj='policy', expected_type=str, choices=['scan', 'policy']
        ),
        endpoint_obj._check(name='families', obj=families, expected_type=dict),
        endpoint_obj._check(name='plugin_id', obj=112, expected_type=int),
    )
