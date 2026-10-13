"""conftest"""

import os

import pytest
import responses

from tenable.io import TenableIO
from tenable.io.filters import FiltersAPI
from tests.pytenable_log_handler import setup_logging_to_file

SCAN_ID_WITH_RESULTS = 6799


@pytest.fixture
@responses.activate
def tvm():
    return TenableIO(
        url='https://nourl', access_key='ACCESS_KEY', secret_key='SECRET_KEY'
    )


@pytest.fixture(autouse=True)
def clear_filter_cache():
    """
    The filter cache lives on the FiltersAPI class, so without this a test's
    filter lookups would depend on which tests happened to run before it.
    """
    FiltersAPI._cache.clear()


@pytest.fixture
def api():
    """api keys fixture"""
    setup_logging_to_file()
    return TenableIO(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing',
    )


@pytest.fixture
def agent():
    """agent fixture"""
    return {
        'id': 2022688,
        'uuid': 'f3800546-1813-499d-8352-57d28d58dc97',
        'name': '00fc9870f38d',
        'platform': 'LINUX',
        'distro': 'es7-x86-64',
        'ip': '172.17.0.2',
        'linked_on': 1522359489,
        'status': 'off',
    }


@pytest.fixture
def folder():
    """fixture to create a folder"""
    return 13203


@pytest.fixture
def policy():
    """fixture to create a policy"""
    return {'policy_id': 13329, 'policy_name': 'bb600ca4-704b-4265-a894-e962afe41a21'}


@pytest.fixture
def user():
    """fixture to create an user"""
    return {
        'id': 3344,
        'user_name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
        'username': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
        'email': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
        'name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
        'type': 'local',
        'aggregate': True,
        'permissions': 64,
        'login_fail_count': 0,
        'login_fail_total': 0,
        'enabled': True,
        'uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
        'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
        'uuid_id': '88aba081-9505-4e06-9acc-2530b486c8d4',
    }


@pytest.fixture
def scanner():
    """fixture to filter scanner which has owner permission"""
    return {
        'creation_date': 1538594853,
        'distro': 'ubuntu1110-x86-64',
        'engine_version': '8.1.0',
        'group': False,
        'id': 131712,
        'key': '00304ce24d16da1ea4e6181e432010eaca13f3394b94c330965b0c0992ad133d',
        'last_connect': 1544138419,
        'last_modification_date': 1544128451,
        'linked': 1,
        'loaded_plugin_set': '201812051251',
        'name': 'pytenable-scanner',
        'num_hosts': 0,
        'num_scans': 0,
        'num_sessions': 0,
        'num_tcp_sessions': 0,
        'owner': 'system',
        'owner_id': 1,
        'owner_name': 'system',
        'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
        'platform': 'LINUX',
        'pool': False,
        'scan_count': 0,
        'shared': 1,
        'source': 'service',
        'status': 'on',
        'timestamp': 1544128451,
        'type': 'managed',
        'ui_build': '158',
        'ui_version': '8.1.0',
        'user_permissions': 128,
        'uuid': '3e839499-e7a5-4aa5-8a2d-61e621ea343b',
        'remote_uuid': 'bdc6b14f-db20-dacb-04e0-960df14350c7834261cf33a01688',
    }


@pytest.fixture
def scannergroup():
    """
    fixture to create a scanner_group
    """
    return {
        'creation_date': 1544138435,
        'last_modification_date': 1544138435,
        'owner_id': 1,
        'owner': 'system',
        'owner_uuid': 'c2359ea1-4153-4239-ab01-987c4f6c2313',
        'default_permissions': 16,
        'scan_count': 0,
        'uuid': '714a5127-dfb4-4a18-bd2b-ae252501675e',
        'type': 'load_balancing',
        'name': 'f847b33d-1fb6-4cf5-8c89-4b2645303fbd',
        'id': 102797,
        'owner_name': 'system',
    }


@pytest.fixture
def scan():
    """
    fixture to create a scan
    """
    return {
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
        'starttime': None,
        'rrules': None,
        'timezone': None,
        'notification_filters': None,
        'shared': 0,
        'user_permissions': 128,
        'default_permissions': 0,
        'owner': 'pytenable_test_user@tenable.com',
        'owner_id': 2201492,
        'last_modification_date': 1623836953,
        'creation_date': 1623836953,
        'type': 'public',
        'id': 221,
    }


@pytest.fixture
def scan_results():
    """fixture to get the scan results"""
    return {
        'results': {
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
                    'severitycount': {
                        'item': [
                            {'count': 133, 'severitylevel': 0},
                            {'count': 0, 'severitylevel': 1},
                        ]
                    },
                    'severity': 133,
                    'score': 133,
                    'info': 133,
                    'low': 0,
                    'medium': 0,
                    'high': 0,
                    'critical': 0,
                    'host_index': 0,
                }
            ]
        },
        'id': 175,
    }


@pytest.fixture(name='network')
def fixture_network():
    """
    Fixture to create network
    """
    return {
        'owner_uuid': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
        'created': 1614777592524,
        'modified': 1614777592524,
        'scanner_count': 0,
        'uuid': '58ac2d96-81aa-472c-a418-74fcc6082049',
        'name': 'Example',
        'description': '',
        'is_default': False,
        'created_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
        'modified_by': '1a2d0102-11b0-4aee-b04f-7240fb66514f',
        'created_in_seconds': 1614777592,
        'modified_in_seconds': 1614777592,
    }
