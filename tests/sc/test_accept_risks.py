import pytest
from ..checker import check
from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception


def test_accept_risks_constructor_repos_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(repos=1)


def test_accept_risks_constructor_repos_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(repos=['one'])


def test_accept_risks_constructor_plugin_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(plugin_id='nope')


def test_accept_risks_constructor_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(port='nope')


def test_accept_risks_constructor_protocol_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(protocol='nothing')


def test_accept_risks_constructor_comments_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(comments=1)


def test_accept_risks_constructor_expires_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(expires='nope')


def test_accept_risks_constructor_ips_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(ips=1)


def test_accept_risks_constructor_ips_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(ips=[1])


def test_accept_risks_constructor_uuids_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(uuids=1)


def test_accept_risks_constructor_uuids_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(uuids=[1])


def test_accept_risks_constructor_asset_list_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks._constructor(asset_list='nope')


def test_accept_risks_constructor_success(sc):
    resp = sc.accept_risks._constructor(
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
    resp = sc.accept_risks._constructor(
        uuids=['UUID1', 'UUID2']
    )
    assert resp == {
        'hostType': 'uuid',
        'hostValue': 'UUID1,UUID2'
    }
    resp = sc.accept_risks._constructor(
        asset_list=1
    )
    assert resp == {
        'hostType': 'asset',
        'hostValue': {'id': 1}
    }


@pytest.fixture
def accept_risk(request, sc, vcr):
    with vcr.use_cassette('test_accept_risks_create_success'):
        accept_risk = sc.accept_risks.create(19506, [1],
                                   ips=['127.0.0.1'])

    def teardown():
        try:
            with vcr.use_cassette('test_accept_risks_delete_success'):
                sc.accept_risks.delete(int(accept_risk['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return accept_risk


@pytest.mark.vcr()
def test_accept_risks_list_success_for_fields(sc):
    accept_risks = sc.accept_risks.list(fields=['id', 'hostType', 'port'],
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
def test_accept_risks_list_success(sc):
    resp = sc.accept_risks.list()
    assert isinstance(resp, list)
    a = resp[0]
    check(a, 'id', str)
    check(a, 'hostType', str)
    check(a, 'hostValue', str)
    check(a, 'port', str)
    check(a, 'protocol', str)
    check(a, 'expires', str)
    check(a, 'status', str)
    check(a, 'repository', dict)
    check(a['repository'], 'id', str)
    check(a['repository'], 'name', str)
    check(a['repository'], 'description', str)
    check(a, 'organization', dict)
    check(a['organization'], 'id', str)
    check(a['organization'], 'name', str)
    check(a['organization'], 'description', str)
    check(a, 'user', dict)
    check(a['user'], 'id', str)
    check(a['user'], 'username', str)
    check(a['user'], 'firstname', str)
    check(a['user'], 'lastname', str)
    check(a, 'plugin', dict)
    check(a['plugin'], 'id', str)
    check(a['plugin'], 'name', str)
    check(a['plugin'], 'description', str)


@pytest.mark.vcr()
def test_accept_risks_create_success(accept_risk):
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
def test_accept_risks_details_success_for_fields(sc, accept_risk):
    accept_risk = sc.accept_risks.details(int(accept_risk['id']), fields=['id', 'hostType', 'hostValue', 'port'])
    check(accept_risk, 'id', str)
    check(accept_risk, 'hostType', str)
    check(accept_risk, 'hostValue', str)
    check(accept_risk, 'port', str)


@pytest.mark.vcr()
def test_accept_risks_details_success(sc, accept_risk):
    accept_risk = sc.accept_risks.details(int(accept_risk['id']))
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
def test_accept_risks_delete_success(sc, accept_risk):
    sc.accept_risks.delete(int(accept_risk['id']))


def test_accept_risks_apply_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks.apply('one', 1)


def test_accept_risks_apply_repo_typeerror(sc):
    with pytest.raises(TypeError):
        sc.accept_risks.apply(1, 'one')


@pytest.mark.vcr()
def test_accept_risks_apply_success(sc, accept_risk):
    sc.accept_risks.apply(int(accept_risk['id']), 1)
