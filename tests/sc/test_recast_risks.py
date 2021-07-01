import pytest
from ..checker import check
from tenable.errors import APIError
from tests.pytenable_log_handler import log_exception


def test_recast_risks_constructor_repos_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(repos=1)


def test_recast_risks_constructor_repos_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(repos=['one'])


def test_recast_risks_constructor_plugin_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(plugin_id='nope')


def test_recast_risks_constructor_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(port='nope')


def test_recast_risks_constructor_protocol_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(protocol='nothing')


def test_recast_risks_constructor_comments_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(comments=1)


def test_recast_risks_constructor_severity_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(severity_id='nope')


def test_recast_risks_constructor_ips_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(ips=1)


def test_recast_risks_constructor_ips_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(ips=[1])


def test_recast_risks_constructor_uuids_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(uuids=1)


def test_recast_risks_constructor_uuids_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(uuids=[1])


def test_recast_risks_constructor_asset_list_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks._constructor(asset_list='nope')


def test_recast_risks_constructor_success(sc):
    resp = sc.recast_risks._constructor(
        repos=[1, 2],
        plugin_id=19506,
        port=0,
        protocol=1,
        comments='comment',
        severity_id=0,
        ips=['192.168.0.1']
    )
    assert resp == {
        'repositories': [{'id': 1}, {'id': 2}],
        'plugin': {'id': "19506"},
        'port': '0',
        'protocol': '1',
        'comments': 'comment',
        'newSeverity': {'id': 0},
        'hostType': 'ip',
        'hostValue': '192.168.0.1'
    }
    resp = sc.recast_risks._constructor(
        uuids=['UUID1', 'UUID2']
    )
    assert resp == {
        'hostType': 'uuid',
        'hostValue': 'UUID1,UUID2'
    }
    resp = sc.recast_risks._constructor(
        asset_list=1
    )
    assert resp == {
        'hostType': 'asset',
        'hostValue': {'id': 1}
    }


@pytest.fixture
def arisk(request, sc, vcr):
    with vcr.use_cassette('test_recast_risks_create_success'):
        arisk = sc.recast_risks.create(19506, [1], 0,
                                   ips=['127.0.0.1'])

    def teardown():
        try:
            with vcr.use_cassette('test_recast_risks_delete_success'):
                sc.recast_risks.delete(int(arisk['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return arisk


@pytest.mark.vcr()
def test_recast_risks_list_success(sc):
    resp = sc.recast_risks.list()
    assert isinstance(resp, list)
    risk = resp[0]
    check(risk, 'id', str)
    check(risk, 'hostType', str)
    check(risk, 'hostValue', str)
    check(risk, 'port', str)
    check(risk, 'protocol', str)
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


@pytest.mark.vcr()
def test_recast_risks_list_success_params(sc):
    resp = sc.recast_risks.list(fields=['id', 'hostType', 'hostValue', 'port'],
                                plugin_id=1234,
                                port=1234,
                                org_ids=[1234],
                                repo_ids=[1234])
    assert isinstance(resp, list)
    risk = resp[0]
    check(risk, 'id', str)
    check(risk, 'hostType', str)
    check(risk, 'hostValue', str)
    check(risk, 'port', str)

@pytest.mark.vcr()
def test_recast_risks_create_success(sc, arisk):
    assert isinstance(arisk, dict)
    check(arisk, 'id', str)
    check(arisk, 'hostType', str)
    check(arisk, 'hostValue', str)
    check(arisk, 'port', str)
    check(arisk, 'protocol', str)
    check(arisk, 'comments', str)
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


@pytest.mark.vcr()
def test_recast_risks_details_success(sc, arisk):
    risk = sc.recast_risks.details(int(arisk['id']))
    check(risk, 'id', str)
    check(risk, 'hostType', str)
    check(risk, 'hostValue', str)
    check(risk, 'port', str)
    check(risk, 'protocol', str)
    check(risk, 'comments', str)
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


@pytest.mark.vcr()
def test_recast_risks_details_success_for_fields(sc, arisk):
    details = sc.recast_risks.details(int(arisk['id']),
                                      fields=['id', 'hostType', 'hostValue', 'port'])
    check(details, 'id', str)
    check(details, 'hostType', str)
    check(details, 'hostValue', str)
    check(details, 'port', str)


@pytest.mark.vcr()
def test_recast_risks_delete_success(sc, arisk):
    sc.recast_risks.delete(int(arisk['id']))


def test_recast_risks_apply_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks.apply('one', 1)


def test_recast_risks_apply_repo_typeerror(sc):
    with pytest.raises(TypeError):
        sc.recast_risks.apply(1, 'one')


@pytest.mark.vcr()
def test_recast_risks_apply_success(sc, arisk):
    sc.recast_risks.apply(int(arisk['id']), 1)
