"""
test file to test various scenarios
in sc accept_risks
"""

import pytest
import responses
from responses import matchers
import uuid

from ..checker import check


def test_accept_risks_constructor_repos_typeerror(tsc):
    """
    testing accept risks constructor for repos type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(repos=1)


def test_accept_risks_constructor_repos_item_typeerror(tsc):
    """
    testing accept risks constructor for repos item type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(repos=['one'])


def test_accept_risks_constructor_plugin_id_typeerror(tsc):
    """
    testing accept risks constructor for plugin id type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(plugin_id='nope')


def test_accept_risks_constructor_port_typeerror(tsc):
    """
    testing accept risks constructor for port type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(port='nope')


def test_accept_risks_constructor_protocol_typeerror(tsc):
    """
    testing accept risks constructor for protocol type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(protocol='nothing')


def test_accept_risks_constructor_comments_typeerror(tsc):
    """
    testing accept risks constructor for comments type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(comments=1)


def test_accept_risks_constructor_expires_typeerror(tsc):
    """
    testing accept risks constructor for expires type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(expires='nope')


def test_accept_risks_constructor_ips_typeerror(tsc):
    """
    testing accept risks constructor for ips type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(ips=1)


def test_accept_risks_constructor_ips_item_typeerror(tsc):
    """
    testing accept risks constructor for ips item type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(ips=[1])


def test_accept_risks_constructor_uuids_typeerror(tsc):
    """
    testing accept risks constructor for uuids type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(uuids=1)


def test_accept_risks_constructor_uuids_item_typeerror(tsc):
    """
    testing accept risks constructor for uuids item type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(uuids=[1])


def test_accept_risks_constructor_asset_list_typeerror(tsc):
    """
    testing accept risks constructor for asset list type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(asset_list='nope')


def test_accept_risks_constructur_host_uuid_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(host_uuids='nope')


def test_accept_risks_constructor_host_uuid_item_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.accept_risks._constructor(host_uuids=[1])


def test_accept_risks_constructor_host_uuid_success(tsc):
    tuuid = str(uuid.uuid4())
    resp = tsc.accept_risks._constructor(host_uuids=[tuuid])
    assert resp == {'hostType': 'hostUUID', 'hostValue': tuuid}


def test_accept_risks_constructor_success(tsc):
    """
    testing accept risks constructor for success
    """
    resp = tsc.accept_risks._constructor(
        repos=[1, 2],
        plugin_id=19506,
        port=0,
        protocol=1,
        comments='comment',
        expires=9999999999,
        ips=['192.168.0.1'],
    )
    assert resp == {
        'repositories': [{'id': 1}, {'id': 2}],
        'plugin': {'id': '19506'},
        'port': '0',
        'protocol': '1',
        'comments': 'comment',
        'expires': 9999999999,
        'hostType': 'ip',
        'hostValue': '192.168.0.1',
    }
    resp = tsc.accept_risks._constructor(uuids=['UUID1', 'UUID2'])
    assert resp == {'hostType': 'uuid', 'hostValue': 'UUID1,UUID2'}
    resp = tsc.accept_risks._constructor(asset_list=1)
    assert resp == {'hostType': 'asset', 'hostValue': {'id': 1}}


@pytest.fixture
def accept_risk():
    """
    test fixture for accept_risk
    """
    return {
        'id': '24',
        'hostType': 'ip',
        'hostValue': '127.0.0.1',
        'port': 'any',
        'protocol': 'any',
        'comments': '',
        'expires': '-1',
        'status': '0',
        'createdTime': '1553612053',
        'modifiedTime': '1553612053',
        'repository': {'id': '1', 'name': 'Default', 'description': ''},
        'organization': {'id': '1', 'name': 'HomeNet', 'description': ''},
        'user': {'id': '2', 'username': 'api', 'firstname': 'api', 'lastname': 'user'},
        'plugin': {
            'id': '19506',
            'name': 'Nessus Scan Information',
            'description': 'This plugin displays, for each tested host, information about the scan itself :\n\n  - The version of the plugin set.\n  - ',
        },
    }


@responses.activate
def test_accept_risks_list_success_for_fields(tsc):
    """
    testing accept risks list success for fields
    """
    responses.get(
        'https://nourl/rest/acceptRiskRule',
        json={
            'type': 'regular',
            'response': [
                {'id': '5', 'hostType': 'ip', 'port': 'any'},
                {'id': '6', 'hostType': 'ip', 'port': 'any'},
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553612053,
        },
        match=[
            matchers.query_param_matcher(
                {
                    'fields': 'id,hostType,port',
                    'pluginID': '1',
                    'port': '1234',
                    'organizationIDs': '1,2',
                    'repositoryIDs': '3,4',
                }
            )
        ],
    )
    accept_risks = tsc.accept_risks.list(
        fields=['id', 'hostType', 'port'],
        plugin_id=1,
        port=1234,
        org_ids=[1, 2],
        repo_ids=[3, 4],
    )
    assert isinstance(accept_risks, list)
    for accept_risk in accept_risks:
        check(accept_risk, 'id', str)
        check(accept_risk, 'hostType', str)
        check(accept_risk, 'port', str)


@responses.activate
def test_accept_risks_list_success(tsc):
    """
    testing accept risks list success
    """
    responses.get(
        'https://nourl/rest/acceptRiskRule',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '5',
                    'hostType': 'ip',
                    'hostValue': '192.168.100.1,192.168.101.1,192.168.102.1,192.168.103.1,192.168.104.1,192.168.105.1,192.168.106.1,192.168.199.1',
                    'port': '0',
                    'protocol': 'TCP',
                    'expires': '-1',
                    'status': '0',
                    'repository': {'id': '1', 'name': 'Default', 'description': ''},
                    'organization': {'id': '1', 'name': 'HomeNet', 'description': ''},
                    'user': {
                        'id': '1',
                        'username': 'steve',
                        'firstname': 'Steve',
                        'lastname': 'McGrath',
                    },
                    'plugin': {
                        'id': '33850',
                        'name': 'Unix Operating System Unsupported Version Detection',
                        'description': 'According to its self-reported version number, the Unix operating system running on the remote host is no longer support',
                    },
                }
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553612053,
        },
    )
    resp = tsc.accept_risks.list()
    assert isinstance(resp, list)
    a_resp = resp[0]
    check(a_resp, 'id', str)
    check(a_resp, 'hostType', str)
    check(a_resp, 'hostValue', str)
    check(a_resp, 'port', str)
    check(a_resp, 'protocol', str)
    check(a_resp, 'expires', str)
    check(a_resp, 'status', str)
    check(a_resp, 'repository', dict)
    check(a_resp['repository'], 'id', str)
    check(a_resp['repository'], 'name', str)
    check(a_resp['repository'], 'description', str)
    check(a_resp, 'organization', dict)
    check(a_resp['organization'], 'id', str)
    check(a_resp['organization'], 'name', str)
    check(a_resp['organization'], 'description', str)
    check(a_resp, 'user', dict)
    check(a_resp['user'], 'id', str)
    check(a_resp['user'], 'username', str)
    check(a_resp['user'], 'firstname', str)
    check(a_resp['user'], 'lastname', str)
    check(a_resp, 'plugin', dict)
    check(a_resp['plugin'], 'id', str)
    check(a_resp['plugin'], 'name', str)
    check(a_resp['plugin'], 'description', str)


@responses.activate
def test_accept_risks_create_success(tsc):
    """
    testing accept risks for create success
    """
    responses.post(
        'https://nourl/rest/acceptRiskRule',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '24',
                    'hostType': 'ip',
                    'hostValue': '127.0.0.1',
                    'port': 'any',
                    'protocol': 'any',
                    'comments': '',
                    'expires': '-1',
                    'status': '0',
                    'createdTime': '1553612053',
                    'modifiedTime': '1553612053',
                    'repository': {'id': '1', 'name': 'Default', 'description': ''},
                    'organization': {'id': '1', 'name': 'HomeNet', 'description': ''},
                    'user': {
                        'id': '2',
                        'username': 'api',
                        'firstname': 'api',
                        'lastname': 'user',
                    },
                    'plugin': {
                        'id': '19506',
                        'name': 'Nessus Scan Information',
                        'description': 'This plugin displays, for each tested host, information about the scan itself :\n\n  - The version of the plugin set.\n  - ',
                    },
                }
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553612052,
        },
    )
    accept_risk = tsc.accept_risks.create(19506, [1], ips=['127.0.0.1'])
    assert isinstance(accept_risk, dict)
    check(accept_risk, 'id', str)
    check(accept_risk, 'hostType', str)
    check(accept_risk, 'hostValue', str)
    check(accept_risk, 'port', str)
    check(accept_risk, 'protocol', str)
    check(accept_risk, 'comments', str)
    check(accept_risk, 'expires', str)
    check(accept_risk, 'status', str)
    check(accept_risk, 'repository', dict)
    check(accept_risk['repository'], 'id', str)
    check(accept_risk['repository'], 'name', str)
    check(accept_risk['repository'], 'description', str)
    check(accept_risk, 'organization', dict)
    check(accept_risk['organization'], 'id', str)
    check(accept_risk['organization'], 'name', str)
    check(accept_risk['organization'], 'description', str)
    check(accept_risk, 'user', dict)
    check(accept_risk['user'], 'id', str)
    check(accept_risk['user'], 'username', str)
    check(accept_risk['user'], 'firstname', str)
    check(accept_risk['user'], 'lastname', str)
    check(accept_risk, 'plugin', dict)
    check(accept_risk['plugin'], 'id', str)
    check(accept_risk['plugin'], 'name', str)
    check(accept_risk['plugin'], 'description', str)


@responses.activate
def test_accept_risks_details_success_for_fields(tsc, accept_risk):
    """
    testing accept risks details success for fields
    """
    responses.get(
        'https://nourl/rest/acceptRiskRule/24',
        json={
            'type': 'regular',
            'response': {
                'id': '26',
                'hostType': 'ip',
                'hostValue': '127.0.0.1',
                'port': 'any',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553612055,
        },
        match=[matchers.query_param_matcher({'fields': 'id,hostType,hostValue,port'})],
    )
    accept_risk = tsc.accept_risks.details(
        int(accept_risk['id']), fields=['id', 'hostType', 'hostValue', 'port']
    )
    check(accept_risk, 'id', str)
    check(accept_risk, 'hostType', str)
    check(accept_risk, 'hostValue', str)
    check(accept_risk, 'port', str)


@responses.activate
def test_accept_risks_details_success(tsc, accept_risk):
    """
    testing accept risks for details success
    """
    responses.get(
        'https://nourl/rest/acceptRiskRule/24',
        json={
            'type': 'regular',
            'response': {
                'id': '26',
                'hostType': 'ip',
                'hostValue': '127.0.0.1',
                'port': 'any',
                'protocol': 'any',
                'comments': '',
                'expires': '-1',
                'status': '0',
                'createdTime': '1553612055',
                'modifiedTime': '1553612055',
                'repository': {'id': '1', 'name': 'Default', 'description': ''},
                'organization': {'id': '1', 'name': 'HomeNet', 'description': ''},
                'user': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'plugin': {
                    'id': '19506',
                    'name': 'Nessus Scan Information',
                    'description': 'This plugin displays, for each tested host, information about the scan itself :\n\n  - The version of the plugin set.\n  - ',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553612055,
        },
    )
    accept_risk = tsc.accept_risks.details(int(accept_risk['id']))
    check(accept_risk, 'id', str)
    check(accept_risk, 'hostType', str)
    check(accept_risk, 'hostValue', str)
    check(accept_risk, 'port', str)
    check(accept_risk, 'protocol', str)
    check(accept_risk, 'comments', str)
    check(accept_risk, 'expires', str)
    check(accept_risk, 'status', str)
    check(accept_risk, 'repository', dict)
    check(accept_risk['repository'], 'id', str)
    check(accept_risk['repository'], 'name', str)
    check(accept_risk['repository'], 'description', str)
    check(accept_risk, 'organization', dict)
    check(accept_risk['organization'], 'id', str)
    check(accept_risk['organization'], 'name', str)
    check(accept_risk['organization'], 'description', str)
    check(accept_risk, 'user', dict)
    check(accept_risk['user'], 'id', str)
    check(accept_risk['user'], 'username', str)
    check(accept_risk['user'], 'firstname', str)
    check(accept_risk['user'], 'lastname', str)
    check(accept_risk, 'plugin', dict)
    check(accept_risk['plugin'], 'id', str)
    check(accept_risk['plugin'], 'name', str)
    check(accept_risk['plugin'], 'description', str)


@responses.activate
def test_accept_risks_delete_success(tsc, accept_risk):
    """
    testing accept risks for delete success
    """
    responses.delete(
        'https://nourl/rest/acceptRiskRule/24',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553612053,
        },
    )
    tsc.accept_risks.delete(int(accept_risk['id']))


def test_accept_risks_apply_id_typeerror(tsc):
    """
    testing accept risks for apply id type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks.apply('one', 1)


def test_accept_risks_apply_repo_typeerror(tsc):
    """
    testing accept risks for apply repo type error
    """
    with pytest.raises(TypeError):
        tsc.accept_risks.apply(1, 'one')


@responses.activate
def test_accept_risks_apply_success(tsc, accept_risk):
    """
    testing accept risks for apply success
    """
    responses.post(
        'https://nourl/rest/acceptRiskRule/24/apply',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553613070,
        },
    )
    tsc.accept_risks.apply(int(accept_risk['id']), 1)
