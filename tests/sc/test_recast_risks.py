"""
test file for testing various scenarios in security center's recast risk
functionality
"""

import pytest
import responses
from responses import matchers
import uuid

from ..checker import check


def test_recast_risks_constructor_repos_typeerror(tsc):
    """
    test recast risks constructor for repos type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(repos=1)


def test_recast_risks_constructor_repos_item_typeerror(tsc):
    """
    test recast risks constructor for 'repos item' type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(repos=['one'])


def test_recast_risks_constructor_plugin_id_typeerror(tsc):
    """
    test recast risks constructor for 'plugin id' type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(plugin_id='nope')


def test_recast_risks_constructor_port_typeerror(tsc):
    """
    test recast risks constructor for port type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(port='nope')


def test_recast_risks_constructor_protocol_typeerror(tsc):
    """
    test recast risks constructor for protocol type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(protocol='nothing')


def test_recast_risks_constructor_comments_typeerror(tsc):
    """
    test recast risks constructor for comments type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(comments=1)


def test_recast_risks_constructor_expires_typeerror(tsc):
    """
    test recast risks constructor for expires type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(expires='nope')


def test_recast_risks_constructor_severity_id_typeerror(tsc):
    """
    test recast risks constructor for 'severity id' type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(severity_id='nope')


def test_recast_risks_constructor_ips_typeerror(tsc):
    """
    test recast risks constructor for ips type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(ips=1)


def test_recast_risks_constructor_ips_item_typeerror(tsc):
    """
    test recast risks constructor for 'ips item' type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(ips=[1])


def test_recast_risks_constructor_uuids_typeerror(tsc):
    """
    test recast risks constructor for uuids type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(uuids=1)


def test_recast_risks_constructor_uuids_item_typeerror(tsc):
    """
    test recast risks constructor for 'uuids item' type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(uuids=[1])


def test_recast_risks_constructor_asset_list_typeerror(tsc):
    """
    test recast risks constructor for 'asset list' type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(asset_list='nope')


def test_recast_risks_constructur_host_uuid_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(host_uuids='nope')


def test_recast_risks_constructor_host_uuid_item_typeerror(tsc):
    with pytest.raises(TypeError):
        tsc.recast_risks._constructor(host_uuids=[1])


def test_recast_risks_constructor_host_uuid_success(tsc):
    tuuid = str(uuid.uuid4())
    resp = tsc.recast_risks._constructor(host_uuids=[tuuid])
    assert resp == {'hostType': 'hostUUID', 'hostValue': tuuid}


def test_recast_risks_constructor_success(tsc):
    """
    test recast risks constructor for success
    """
    resp = tsc.recast_risks._constructor(
        repos=[1, 2],
        plugin_id=19506,
        port=0,
        protocol=1,
        comments='comment',
        severity_id=0,
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
        'newSeverity': {'id': 0},
        'hostType': 'ip',
        'hostValue': '192.168.0.1',
    }
    resp = tsc.recast_risks._constructor(uuids=['UUID1', 'UUID2'])
    assert resp == {'hostType': 'uuid', 'hostValue': 'UUID1,UUID2'}
    resp = tsc.recast_risks._constructor(asset_list=1)
    assert resp == {'hostType': 'asset', 'hostValue': {'id': 1}}


@pytest.fixture
def arisk():
    """
    test fixture for a risk
    """
    return {
        'id': '1',
        'newSeverity': '0',
        'hostType': 'ip',
        'hostValue': '127.0.0.1',
        'port': 'any',
        'protocol': 'any',
        'comments': '',
        'expires': '-1',
        'order': '1',
        'status': '0',
        'createdTime': '1554731789',
        'modifiedTime': '1554731789',
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
def test_recast_risks_list_success(tsc):
    """
    test recast risks list for success
    """
    responses.get(
        'https://nourl/rest/recastRiskRule',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '1',
                    'newSeverity': '0',
                    'hostType': 'ip',
                    'hostValue': '127.0.0.1',
                    'port': 'any',
                    'protocol': 'any',
                    'expires': '-1',
                    'order': '1',
                    'status': '0',
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
            'timestamp': 1554731790,
        },
    )
    resp = tsc.recast_risks.list()
    assert isinstance(resp, list)
    risk = resp[0]
    check(risk, 'id', str)
    check(risk, 'hostType', str)
    check(risk, 'hostValue', str)
    check(risk, 'port', str)
    check(risk, 'protocol', str)
    check(risk, 'expires', str)
    check(risk, 'newSeverity', str)
    check(risk, 'status', str)
    check(risk, 'repository', dict)
    check(risk['repository'], 'id', str)
    check(risk['repository'], 'name', str)
    check(risk['repository'], 'description', str)
    check(risk, 'organization', dict)
    check(risk['organization'], 'id', str)
    check(risk['organization'], 'name', str)
    check(risk['organization'], 'description', str)
    check(risk, 'user', dict)
    check(risk['user'], 'id', str)
    check(risk['user'], 'username', str)
    check(risk['user'], 'firstname', str)
    check(risk['user'], 'lastname', str)
    check(risk, 'plugin', dict)
    check(risk['plugin'], 'id', str)
    check(risk['plugin'], 'name', str)
    check(risk['plugin'], 'description', str)


@responses.activate
def test_recast_risks_list_success_params(tsc):
    """
    test recast risks list success for params
    """
    responses.get(
        'https://nourl/rest/recastRiskRule',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '1',
                    'newSeverity': '0',
                    'hostType': 'ip',
                    'hostValue': '127.0.0.1',
                    'port': 'any',
                    'protocol': 'any',
                    'order': '1',
                    'status': '0',
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
            'timestamp': 1554731790,
        },
        match=[
            matchers.query_param_matcher(
                {
                    'fields': 'id,hostType,hostValue,port',
                    'pluginID': '1234',
                    'port': '1234',
                    'organizationIDs': '1234',
                    'repositoryIDs': '1234',
                }
            )
        ],
    )
    resp = tsc.recast_risks.list(
        fields=['id', 'hostType', 'hostValue', 'port'],
        plugin_id=1234,
        port=1234,
        org_ids=[1234],
        repo_ids=[1234],
    )
    assert isinstance(resp, list)
    risk = resp[0]
    check(risk, 'id', str)
    check(risk, 'hostType', str)
    check(risk, 'hostValue', str)
    check(risk, 'port', str)


@responses.activate
def test_recast_risks_create_success(tsc):
    """
    test recast risks create for success
    """
    responses.post(
        'https://nourl/rest/recastRiskRule',
        json={
            'type': 'regular',
            'response': [
                {
                    'id': '1',
                    'newSeverity': '0',
                    'hostType': 'ip',
                    'hostValue': '127.0.0.1',
                    'port': 'any',
                    'protocol': 'any',
                    'comments': '',
                    'expires': '-1',
                    'order': '1',
                    'status': '0',
                    'createdTime': '1554731789',
                    'modifiedTime': '1554731789',
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
            'timestamp': 1554731789,
        },
    )
    arisk = tsc.recast_risks.create(19506, [1], 0, ips=['127.0.0.1'])
    assert isinstance(arisk, dict)
    check(arisk, 'id', str)
    check(arisk, 'hostType', str)
    check(arisk, 'hostValue', str)
    check(arisk, 'port', str)
    check(arisk, 'protocol', str)
    check(arisk, 'comments', str)
    check(arisk, 'expires', str)
    check(arisk, 'newSeverity', str)
    check(arisk, 'status', str)
    check(arisk, 'repository', dict)
    check(arisk['repository'], 'id', str)
    check(arisk['repository'], 'name', str)
    check(arisk['repository'], 'description', str)
    check(arisk, 'organization', dict)
    check(arisk['organization'], 'id', str)
    check(arisk['organization'], 'name', str)
    check(arisk['organization'], 'description', str)
    check(arisk, 'user', dict)
    check(arisk['user'], 'id', str)
    check(arisk['user'], 'username', str)
    check(arisk['user'], 'firstname', str)
    check(arisk['user'], 'lastname', str)
    check(arisk, 'plugin', dict)
    check(arisk['plugin'], 'id', str)
    check(arisk['plugin'], 'name', str)
    check(arisk['plugin'], 'description', str)


@responses.activate
def test_recast_risks_details_success(tsc, arisk):
    """
    test recast risks details for success
    """
    responses.get(
        'https://nourl/rest/recastRiskRule/1',
        json={
            'type': 'regular',
            'response': {
                'id': '3',
                'newSeverity': '0',
                'hostType': 'ip',
                'hostValue': '127.0.0.1',
                'port': 'any',
                'protocol': 'any',
                'comments': '',
                'expires': '-1',
                'order': '1',
                'status': '0',
                'createdTime': '1554731791',
                'modifiedTime': '1554731791',
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
            'timestamp': 1554731791,
        },
    )
    risk = tsc.recast_risks.details(int(arisk['id']))
    check(risk, 'id', str)
    check(risk, 'hostType', str)
    check(risk, 'hostValue', str)
    check(risk, 'port', str)
    check(risk, 'protocol', str)
    check(risk, 'comments', str)
    check(risk, 'expires', str)
    check(risk, 'newSeverity', str)
    check(risk, 'status', str)
    check(risk, 'repository', dict)
    check(risk['repository'], 'id', str)
    check(risk['repository'], 'name', str)
    check(risk['repository'], 'description', str)
    check(risk, 'organization', dict)
    check(risk['organization'], 'id', str)
    check(risk['organization'], 'name', str)
    check(risk['organization'], 'description', str)
    check(risk, 'user', dict)
    check(risk['user'], 'id', str)
    check(risk['user'], 'username', str)
    check(risk['user'], 'firstname', str)
    check(risk['user'], 'lastname', str)
    check(risk, 'plugin', dict)
    check(risk['plugin'], 'id', str)
    check(risk['plugin'], 'name', str)
    check(risk['plugin'], 'description', str)


@responses.activate
def test_recast_risks_details_success_for_fields(tsc, arisk):
    """
    test recast risks details success for fields
    """
    responses.get(
        'https://nourl/rest/recastRiskRule/1',
        json={
            'type': 'regular',
            'response': {
                'id': '3',
                'hostType': 'ip',
                'hostValue': '127.0.0.1',
                'port': 'any',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1554731791,
        },
        match=[matchers.query_param_matcher({'fields': 'id,hostType,hostValue,port'})],
    )
    details = tsc.recast_risks.details(
        int(arisk['id']), fields=['id', 'hostType', 'hostValue', 'port']
    )
    check(details, 'id', str)
    check(details, 'hostType', str)
    check(details, 'hostValue', str)
    check(details, 'port', str)


@responses.activate
def test_recast_risks_delete_success(tsc, arisk):
    """
    test recast risks delete for success
    """
    responses.delete(
        'https://nourl/rest/recastRiskRule/1',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1554731790,
        },
    )
    tsc.recast_risks.delete(int(arisk['id']))


def test_recast_risks_apply_id_typeerror(tsc):
    """
    test recast risks apply for id type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks.apply('one', 1)


def test_recast_risks_apply_repo_typeerror(tsc):
    """
    test recast risks apply for repo type error
    """
    with pytest.raises(TypeError):
        tsc.recast_risks.apply(1, 'one')


@responses.activate
def test_recast_risks_apply_success(tsc, arisk):
    """
    test recast risks apply for success
    """
    responses.post(
        'https://nourl/rest/recastRiskRule/1/apply',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1554731794,
        },
    )
    tsc.recast_risks.apply(int(arisk['id']), 1)
