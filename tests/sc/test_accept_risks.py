'''
test file to test various scenarios
in sc accept_risks
'''
import pytest

from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception
from ..checker import check


def test_accept_risks_constructor_repos_typeerror(security_center):
    '''
    testing accept risks constructor for repos type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(repos=1)


def test_accept_risks_constructor_repos_item_typeerror(security_center):
    '''
    testing accept risks constructor for repos item type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(repos=['one'])


def test_accept_risks_constructor_plugin_id_typeerror(security_center):
    '''
    testing accept risks constructor for plugin id type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(plugin_id='nope')


def test_accept_risks_constructor_port_typeerror(security_center):
    '''
    testing accept risks constructor for port type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(port='nope')


def test_accept_risks_constructor_protocol_typeerror(security_center):
    '''
    testing accept risks constructor for protocol type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(protocol='nothing')


def test_accept_risks_constructor_comments_typeerror(security_center):
    '''
    testing accept risks constructor for comments type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(comments=1)


def test_accept_risks_constructor_expires_typeerror(security_center):
    '''
    testing accept risks constructor for expires type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(expires='nope')


def test_accept_risks_constructor_ips_typeerror(security_center):
    '''
    testing accept risks constructor for ips type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(ips=1)


def test_accept_risks_constructor_ips_item_typeerror(security_center):
    '''
    testing accept risks constructor for ips item type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(ips=[1])


def test_accept_risks_constructor_uuids_typeerror(security_center):
    '''
    testing accept risks constructor for uuids type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(uuids=1)


def test_accept_risks_constructor_uuids_item_typeerror(security_center):
    '''
    testing accept risks constructor for uuids item type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(uuids=[1])


def test_accept_risks_constructor_asset_list_typeerror(security_center):
    '''
    testing accept risks constructor for asset list type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks._constructor(asset_list='nope')


def test_accept_risks_constructor_success(security_center):
    '''
    testing accept risks constructor for success
    '''
    resp = security_center.accept_risks._constructor(
        repos=[1, 2],
        plugin_id=19506,
        port=0,
        protocol=1,
        comments='comment',
        expires=9999999999,
        ips=['192.168.0.1']
    )
    assert resp == {
        'repositories': [{'id': 1}, {'id': 2}],
        'plugin': {'id': "19506"},
        'port': '0',
        'protocol': '1',
        'comments': 'comment',
        'expires': 9999999999,
        'hostType': 'ip',
        'hostValue': '192.168.0.1'
    }
    resp = security_center.accept_risks._constructor(
        uuids=['UUID1', 'UUID2']
    )
    assert resp == {
        'hostType': 'uuid',
        'hostValue': 'UUID1,UUID2'
    }
    resp = security_center.accept_risks._constructor(
        asset_list=1
    )
    assert resp == {
        'hostType': 'asset',
        'hostValue': {'id': 1}
    }


@pytest.fixture
def accept_risk(request, security_center, vcr):
    '''
    test fixture for accept_risk
    '''
    with vcr.use_cassette('test_accept_risks_create_success'):
        accept_risk = security_center.accept_risks.create(19506, [1],
                                                          ips=['127.0.0.1'])

    def teardown():
        try:
            with vcr.use_cassette('test_accept_risks_delete_success'):
                security_center.accept_risks.delete(int(accept_risk['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return accept_risk


@pytest.mark.vcr()
def test_accept_risks_list_success_for_fields(security_center):
    '''
    testing accept risks list success for fields
    '''
    accept_risks = security_center.accept_risks.list(fields=['id', 'hostType', 'port'],
                                                     plugin_id=1,
                                                     port=1234,
                                                     org_ids=[1, 2],
                                                     repo_ids=[3, 4])
    assert isinstance(accept_risks, list)
    for accept_risk in accept_risks:
        check(accept_risk, 'id', str)
        check(accept_risk, 'hostType', str)
        check(accept_risk, 'port', str)


@pytest.mark.vcr()
def test_accept_risks_list_success(security_center):
    '''
    testing accept risks list success
    '''
    resp = security_center.accept_risks.list()
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


@pytest.mark.vcr()
def test_accept_risks_create_success(accept_risk):
    '''
    testing accept risks for create success
    '''
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


@pytest.mark.vcr()
def test_accept_risks_details_success_for_fields(security_center, accept_risk):
    '''
    testing accept risks details success for fields
    '''
    accept_risk = security_center.accept_risks.details(int(accept_risk['id']), fields=['id', 'hostType', 'hostValue', 'port'])
    check(accept_risk, 'id', str)
    check(accept_risk, 'hostType', str)
    check(accept_risk, 'hostValue', str)
    check(accept_risk, 'port', str)


@pytest.mark.vcr()
def test_accept_risks_details_success(security_center, accept_risk):
    '''
    testing accept risks for details success
    '''
    accept_risk = security_center.accept_risks.details(int(accept_risk['id']))
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


@pytest.mark.vcr()
def test_accept_risks_delete_success(security_center, accept_risk):
    '''
    testing accept risks for delete success
    '''
    security_center.accept_risks.delete(int(accept_risk['id']))


def test_accept_risks_apply_id_typeerror(security_center):
    '''
    testing accept risks for apply id type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks.apply('one', 1)


def test_accept_risks_apply_repo_typeerror(security_center):
    '''
    testing accept risks for apply repo type error
    '''
    with pytest.raises(TypeError):
        security_center.accept_risks.apply(1, 'one')


@pytest.mark.vcr()
def test_accept_risks_apply_success(security_center, accept_risk):
    '''
    testing accept risks for apply success
    '''
    security_center.accept_risks.apply(int(accept_risk['id']), 1)
