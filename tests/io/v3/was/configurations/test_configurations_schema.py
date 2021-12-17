import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.was.configurations.schema import (
    ConfigurationSchema, PermissionConfigurationSchema, ScheduleSchema,
    SettingsSchema)

CONFIGURATION_PAYLOAD = {
    'name': 'Test Schema',
    'owner_id': '3f79d8d6-abc9-493c-b019-086d9de549c9',
    'template_id': 'b223f18e-5a94-4e02-b560-77a4a8246cd3',
    'targets': [
        'https://google.com',
        'http://dogshop.com'
    ],
    'notifications': {
        'emails': [
            'testuser@tenable.com'
        ]
    },
    'permissions': [
        {
            'entity': 'user',
            'entity_id': '3f79d8d6-abc9-493c-b019-086d9de549c9',
            'level': 'configure',
            'permissions_id': '8fbef377-b252-411d-95c8-bc3deac425ed'
        }
    ],
    'schedule': {
        'rrule': 'FREQ=MONTHLY;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1',
        'starttime': '2021-11-09T08:41:09+00:00',
        'timezone': 'America/New_York',
        'enabled': False
    },
    'settings': {
        "timeout": "08:00:00",
        "queue_timeout": "08:00:00",
        "debug_mode": False,
        "credentials": {
            'credential_ids': [
                '00000000-0000-0000-0000-000000000000'
            ]
        },
        "scope": {
            "option": "all",
            "urls": None,
            "exclude_file_extensions": [
                "js",
                "css",
                "png",
                "jpeg",
                "gif",
                "pdf",
                "csv",
                "svn-base",
                "svg",
                "jpg",
                "ico",
                "woff",
                "woff2",
                "exe",
                "msi",
                "zip"
            ],
            "exclude_path_patterns": [
                "logout"
            ],
            "dom_depth_limit": 5,
            "directory_depth_limit": 10,
            "page_limit": 10000,
            "crawl_script": None,
            "decompose_paths": False,
            "exclude_binaries": True,
            "auto_redundant_paths": 5,
            "openapi_file": None,
            "openapi_filename": None,
            "crawl_script_filename": None
        },
        "plugin": {
            "rate_limiter": {
                "requests_per_second": 25,
                "autothrottle": True,
                "timeout_threshold": 100
            },
            "mode": "disable",
            "ids": [],
            "names": [],
            "families": []
        },
        "browser": {
            "screen_width": 1600,
            "screen_height": 1200,
            "ignore_images": True,
            "job_timeout": 60,
            "analysis": None,
            "pool_size": 3
        },
        "http": {
            "response_max_size": 5000000,
            "request_redirect_limit": 2,
            "user_agent": "WAS/%v",
            "custom_user_agent": False,
            "request_headers": {
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5"
            },
            "include_scan_id": False,
            "request_concurrency": 10,
            "request_timeout": 30
        },
        "chrome": {
            "script_finish_wait": 5000,
            "script_page_load_wait": 30000,
            "script_command_wait": 500
        },
        "assessment": {
            "enable": True,
            "dictionary": "limited",
            "rfi_remote_url": "http://rfi.nessus.org/rfi.txt",
            "fingerprinting": None,
            "element_exclusions": None,
            "bruteforce": None
        },
        "audit": {
            "forms": True,
            "cookies": True,
            "ui_forms": True,
            "ui_inputs": True,
            "headers": True,
            "links": True,
            "parameter_names": False,
            "parameter_values": True,
            "jsons": True,
            "xmls": True,
            "path_parameters": False
        }
    }
}


def test_create_configuration_schema():
    '''
    Test the Configuration Schema
    '''

    schema = ConfigurationSchema()
    payload = schema.dump(schema.load(CONFIGURATION_PAYLOAD))

    assert payload['notifications']['emails'][0] == CONFIGURATION_PAYLOAD['notifications']['emails'][0]  # noqa: E501
    assert payload['schedule']['starttime'] == CONFIGURATION_PAYLOAD['schedule']['starttime']  # noqa: E501
    assert payload['settings']['audit']['cookies']
    assert payload['settings']['chrome']['script_finish_wait'] == 5000


def test_notifications_invalid():
    '''
    Test Notification body parameter
    '''

    notification_payload = dict()
    notification_payload['notifications'] = 'test@tenable.com'

    schema = ConfigurationSchema()
    with pytest.raises(ValidationError):
        schema.dump(schema.load(notification_payload))


def test_schedule_invalid():
    '''
    Test Schedule Schema
    '''
    schedule_payload = dict()
    schedule_payload.update(CONFIGURATION_PAYLOAD['schedule'])
    schedule_payload.pop('starttime')
    schedule_payload.pop('rrule')

    schema = ScheduleSchema()
    with pytest.raises(ValidationError):
        schema.dump(schema.load(schedule_payload))


def test_permissions_invalid():
    '''
    Test Permissions Schema
    '''

    permission_payload = dict()
    permission_payload.update(CONFIGURATION_PAYLOAD['permissions'][0])
    permission_payload['level'] = 'no-access'
    schema = PermissionConfigurationSchema()
    with pytest.raises(ValidationError):
        schema.dump(schema.load(permission_payload))


def test_settings_invalid():
    '''
    Test Settings Schema
    '''

    settings_payload = dict()
    settings_payload.update(CONFIGURATION_PAYLOAD['settings'])
    settings_payload['timeout'] = '100:99:99'
    settings_payload['credentials'] = None
    schema = SettingsSchema()
    with pytest.raises(ValidationError):
        schema.dump(schema.load(settings_payload))
