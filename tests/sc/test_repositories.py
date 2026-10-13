"""
test file for testing various scenarios in security center's repositories
functionality
"""

import os

import pytest
import responses
from responses import matchers as m
from responses.registries import OrderedRegistry

from tenable.errors import UnexpectedValueError

from ..checker import check


@pytest.fixture
def repository():
    """
    test fixture for repository
    """
    return {
        'id': '6',
        'name': 'Example Repo',
        'description': '',
        'type': 'Local',
        'dataFormat': 'IPv4',
        'remoteID': None,
        'remoteIP': None,
        'running': 'false',
        'downloadFormat': 'v2',
        'lastSyncTime': '0',
        'createdTime': '1550707168',
        'modifiedTime': '1550707168',
        'lastVulnUpdate': '1550707168',
        'vulnCount': '0',
        'organizations': [],
        'typeFields': {
            'correlation': [],
            'nessusSchedule': {'type': 'never', 'start': '', 'repeatRule': ''},
            'ipRange': '0.0.0.0/0',
            'ipCount': '0',
            'runningNessus': 'false',
            'lastGenerateNessusTime': '0',
            'trendingDays': '0',
            'trendWithRaw': 'false',
            'lastTrendUpdate': '0',
        },
    }


def test_repositories_constructor_nessus_sched_typeerror(tsc):
    """
    test repositories constructor for 'nessus sched' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(nessus_sched=1)


def test_repositories_constructor_mobile_sched_typeerror(tsc):
    """
    test repositories constructor for 'mobile sched' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(mobile_sched=1)


def test_repositories_constructor_remote_sched_typeerror(tsc):
    """
    test repositories constructor for 'remote sched' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(remote_sched=1)


def test_repositories_constructor_name_typeerror(tsc):
    """
    test repositories constructor for 'name' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(name=1)

    with pytest.raises(TypeError):
        tsc.repositories._constructor(
            nessus_sched={'type': 'dependent', 'dependentID': 1}, name=1
        )


def test_repositories_constructor_description_typeerror(tsc):
    """
    test repositories constructor for 'description' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(description=1)


def test_repositories_constructor_format_typeerror(tsc):
    """
    test repositories constructor for 'format' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(format=1)


def test_repositories_constructor_format_unexpectedvalueerror(tsc):
    """
    test repositories constructor for 'format' unexpected value error.
    """
    with pytest.raises(UnexpectedValueError):
        tsc.repositories._constructor(format='none')


def test_repositories_constructor_orgs_typeerror(tsc):
    """
    test repositories constructor for 'orgs' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(orgs=1)


def test_repositories_constructor_org_item_typeerror(tsc):
    """
    test repositories constructor for 'org item' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(orgs=['one'])


def test_repositories_constructor_trending_typeerror(tsc):
    """
    test repositories constructor for 'trending' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(trending='one')


def test_repositories_constructor_trending_unexpectedvalueerror(tsc):
    """
    test repositories constructor for 'trending' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.repositories._constructor(trending=999)


def test_repositories_constructor_fulltext_search_typerror(tsc):
    """
    test repositories constructor for 'full text search' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(fulltext_search='yup')


def test_repositories_constructor_lce_correlation_typeerror(tsc):
    """
    test repositories constructor for 'lce correlation' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(lce_correlation='yup')


def test_repositories_constructor_allowed_ips_typeerror(tsc):
    """
    test repositories constructor for 'allowed ips' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(allowed_ips='127.0.0.1')


def test_repositories_constructor_allowed_ips_item_typeerror(tsc):
    """
    test repositories constructor for 'allowed ips item' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(allowed_ips=[1])


def test_repositories_constructor_remote_ip_typeerror(tsc):
    """
    test repositories constructor for 'remote ip' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(remote_ip=1)


def test_repositories_constructor_remote_repo_typeerror(tsc):
    """
    test repositories constructor for 'remote repo' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(remote_repo='one')


def test_repositories_constructor_preferences_typeerror(tsc):
    """
    test repositories constructor for 'preferences' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(preferences=1)


def test_repositories_constructor_preferences_key_typeerror(tsc):
    """
    test repositories constructor for 'preferences key' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(preferences={1: 'one'})


def test_repositories_constructor_preferences_value_typeerror(tsc):
    """
    test repositories constructor for 'preferences value' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(preferences={'key': 1})


def test_repositories_constructor_mdm_id_typeerror(tsc):
    """
    test repositories constructor for 'mdm id' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(mdm_id='one')


def test_repositories_constructor_scanner_id_typeerror(tsc):
    """
    test repositories constructor for 'scanner id' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._constructor(scanner_id='one')


def test_repositories_constructor_success(tsc):
    """
    test repositories constructor for success
    """
    resp = tsc.repositories._constructor(
        nessus_sched={'type': 'ical', 'start': 'start', 'repeatRule': 'rule'},
        mobile_sched={'type': 'never'},
        remote_sched={'type': 'never'},
        name='Test Constructor',
        description='Desc',
        format='IPv4',
        repo_type='Local',
        orgs=[1],
        trending=90,
        fulltext_search=True,
        lce_correlation=[1],
        allowed_ips=['127.0.0.1'],
        remote_ip='127.0.0.1',
        remote_repo=1,
        preferences={'name': 'value'},
        mdm_id=1,
        scanner_id=1,
    )
    assert resp == {
        'nessusSchedule': {'type': 'ical', 'start': 'start', 'repeatRule': 'rule'},
        'mobileSchedule': {'type': 'never'},
        'remoteSchedule': {'type': 'never'},
        'name': 'Test Constructor',
        'description': 'Desc',
        'dataFormat': 'IPv4',
        'type': 'Local',
        'organizations': [{'id': 1}],
        'trendingDays': 90,
        'trendWithRaw': 'true',
        'correlation': [{'id': 1}],
        'ipRange': '127.0.0.1',
        'remoteIP': '127.0.0.1',
        'remoteID': 1,
        'preferences': {'name': 'value'},
        'mdm': {'id': 1},
        'scanner': {'id': 1},
    }


@responses.activate
def test_repositories_create_success(tsc):
    """
    test repositories create for success
    """
    responses.post(
        'https://nourl/rest/repository',
        json={
            'type': 'regular',
            'response': {
                'id': '6',
                'name': 'Example Repo',
                'description': '',
                'type': 'Local',
                'dataFormat': 'IPv4',
                'remoteID': None,
                'remoteIP': None,
                'running': 'false',
                'downloadFormat': 'v2',
                'lastSyncTime': '0',
                'createdTime': '1550707168',
                'modifiedTime': '1550707168',
                'lastVulnUpdate': '1550707168',
                'vulnCount': '0',
                'organizations': [],
                'typeFields': {
                    'correlation': [],
                    'nessusSchedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                    'ipRange': '0.0.0.0/0',
                    'ipCount': '0',
                    'runningNessus': 'false',
                    'lastGenerateNessusTime': '0',
                    'trendingDays': '0',
                    'trendWithRaw': 'false',
                    'lastTrendUpdate': '0',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707168,
        },
    )
    repository = tsc.repositories.create(name='Example Repo')
    assert isinstance(repository, dict)
    check(repository, 'createdTime', str)
    check(repository, 'dataFormat', str)
    check(repository, 'description', str)
    check(repository, 'downloadFormat', str)
    check(repository, 'id', str)
    check(repository, 'lastSyncTime', str)
    check(repository, 'lastVulnUpdate', str)
    check(repository, 'modifiedTime', str)
    check(repository, 'name', str)
    check(repository, 'organizations', list)
    check(repository, 'remoteID', str, allow_none=True)
    check(repository, 'remoteIP', str, allow_none=True)
    check(repository, 'running', str)
    check(repository, 'type', str)
    check(repository, 'typeFields', dict)
    check(repository['typeFields'], 'correlation', list)
    check(repository['typeFields'], 'ipCount', str)
    check(repository['typeFields'], 'ipRange', str)
    check(repository['typeFields'], 'lastGenerateNessusTime', str)
    check(repository['typeFields'], 'lastTrendUpdate', str)
    check(repository['typeFields'], 'nessusSchedule', dict)
    check(repository['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(repository['typeFields']['nessusSchedule'], 'start', str)
    check(repository['typeFields']['nessusSchedule'], 'type', str)
    check(repository['typeFields'], 'runningNessus', str)
    check(repository['typeFields'], 'trendWithRaw', str)
    check(repository['typeFields'], 'trendingDays', str)
    check(repository, 'vulnCount', str)


def test_repositories_details_id_typeerror(tsc):
    """
    test repositories details for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.details('one')


def test_repositories_details_fields_typeerror(tsc):
    """
    test repositories details for 'fields' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.details(1, fields=1)


def test_repositories_details_field_item_typeerror(tsc):
    """
    test repositories details for 'field item' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.details(1, fields=[1])


@responses.activate
def test_repositories_remote_sync(tsc):
    """
    test repositories remote sync for success
    """
    responses.post(
        'https://nourl/rest/repository/200001/sync',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707449,
        },
        headers={'content-disposition': 'attachment; filename=repository-4.tar.gz'},
    )
    tsc.repositories.remote_sync(200001)


@responses.activate
def test_repositories_mobile_sync(tsc):
    """
    test repositories mobile sync for success
    """
    responses.post(
        'https://nourl/rest/repository/200001/updateMobileData',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707449,
        },
        headers={'content-disposition': 'attachment; filename=repository-4.tar.gz'},
    )
    tsc.repositories.mobile_sync(200001)


@responses.activate
def test_repositories_details_success(tsc, repository):
    """
    test repositories details for success
    """
    responses.get(
        'https://nourl/rest/repository/6',
        json={
            'type': 'regular',
            'response': {
                'id': '7',
                'name': 'Example Repo',
                'description': '',
                'type': 'Local',
                'dataFormat': 'IPv4',
                'remoteID': None,
                'remoteIP': None,
                'running': 'false',
                'downloadFormat': 'v2',
                'lastSyncTime': '0',
                'createdTime': '1550707449',
                'modifiedTime': '1550707449',
                'lastVulnUpdate': '1550707449',
                'vulnCount': '0',
                'organizations': [],
                'typeFields': {
                    'correlation': [],
                    'nessusSchedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                    'ipRange': '0.0.0.0/0',
                    'ipCount': '0',
                    'runningNessus': 'false',
                    'lastGenerateNessusTime': '0',
                    'trendingDays': '0',
                    'trendWithRaw': 'false',
                    'lastTrendUpdate': '0',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707449,
        },
    )
    repository = tsc.repositories.details(int(repository['id']))
    assert isinstance(repository, dict)
    check(repository, 'createdTime', str)
    check(repository, 'dataFormat', str)
    check(repository, 'description', str)
    check(repository, 'downloadFormat', str)
    check(repository, 'id', str)
    check(repository, 'lastSyncTime', str)
    check(repository, 'lastVulnUpdate', str)
    check(repository, 'modifiedTime', str)
    check(repository, 'name', str)
    check(repository, 'organizations', list)
    check(repository, 'remoteID', str, allow_none=True)
    check(repository, 'remoteIP', str, allow_none=True)
    check(repository, 'running', str)
    check(repository, 'type', str)
    check(repository, 'typeFields', dict)
    check(repository['typeFields'], 'correlation', list)
    check(repository['typeFields'], 'ipCount', str)
    check(repository['typeFields'], 'ipRange', str)
    check(repository['typeFields'], 'lastGenerateNessusTime', str)
    check(repository['typeFields'], 'lastTrendUpdate', str)
    check(repository['typeFields'], 'nessusSchedule', dict)
    check(repository['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(repository['typeFields']['nessusSchedule'], 'start', str)
    check(repository['typeFields']['nessusSchedule'], 'type', str)
    check(repository['typeFields'], 'runningNessus', str)
    check(repository['typeFields'], 'trendWithRaw', str)
    check(repository['typeFields'], 'trendingDays', str)
    check(repository, 'vulnCount', str)


@responses.activate
def test_repositories_list_success(tsc):
    """
    test repositories list for success
    """
    responses.get(
        'https://nourl/rest/repository',
        json={
            'type': 'regular',
            'response': [
                {'id': '7', 'name': 'Example Repo7'},
                {'id': '8', 'name': 'Example Repo8'},
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707449,
        },
        match=[m.query_param_matcher({'type': 'Local', 'fields': 'id,name'})],
    )
    for repo in tsc.repositories.list(fields=['id', 'name'], repo_type='Local'):
        assert isinstance(repo, dict)
        check(repo, 'name', str)
        check(repo, 'id', str)


@responses.activate
def test_repositories_create_success_data_format_ipv6(tsc):
    """
    test repositories create success with data format ipv6
    """
    responses.post(
        'https://nourl/rest/repository',
        json={
            'type': 'regular',
            'response': {
                'id': '10001',
                'name': 'Example Repo',
                'description': '',
                'type': 'Remote',
                'dataFormat': 'IPv6',
                'remoteID': None,
                'remoteIP': None,
                'running': 'false',
                'downloadFormat': 'v2',
                'lastSyncTime': '0',
                'createdTime': '1550707168',
                'modifiedTime': '1550707168',
                'lastVulnUpdate': '1550707168',
                'vulnCount': '0',
                'organizations': [],
                'typeFields': {
                    'correlation': [],
                    'nessusSchedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                    'ipRange': '0.0.0.0/0',
                    'ipCount': '0',
                    'runningNessus': 'false',
                    'lastGenerateNessusTime': '0',
                    'trendingDays': '0',
                    'trendWithRaw': 'false',
                    'lastTrendUpdate': '0',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707168,
        },
    )
    responses.delete(
        'https://nourl/rest/repository/10001',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707450,
        },
    )
    repo = tsc.repositories.create(dataFormat='IPv6', type='remote')
    assert isinstance(repo, dict)
    check(repo, 'name', str)
    check(repo, 'id', str)
    tsc.repositories.delete(int(repo['id']))


@responses.activate
def test_repositories_create_success_data_format_mobile(tsc):
    """
    test repositories create success with data format mobile
    """
    responses.post(
        'https://nourl/rest/repository',
        json={
            'type': 'regular',
            'response': {
                'id': '10001',
                'name': 'Example Repo',
                'description': '',
                'type': 'Local',
                'dataFormat': 'Mobile',
                'remoteID': None,
                'remoteIP': None,
                'running': 'false',
                'downloadFormat': 'v2',
                'lastSyncTime': '0',
                'createdTime': '1550707168',
                'modifiedTime': '1550707168',
                'lastVulnUpdate': '1550707168',
                'vulnCount': '0',
                'organizations': [],
                'typeFields': {
                    'correlation': [],
                    'nessusSchedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                    'ipRange': '0.0.0.0/0',
                    'ipCount': '0',
                    'runningNessus': 'false',
                    'lastGenerateNessusTime': '0',
                    'trendingDays': '0',
                    'trendWithRaw': 'false',
                    'lastTrendUpdate': '0',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707168,
        },
    )
    responses.delete(
        'https://nourl/rest/repository/10001',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707450,
        },
    )
    repo = tsc.repositories.create(dataFormat='mobile')
    assert isinstance(repo, dict)
    check(repo, 'name', str)
    check(repo, 'id', str)
    tsc.repositories.delete(int(repo['id']))


def test_repositories_delete_id_typeerror(tsc):
    """
    test repositories delete for id type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.delete('one')


@responses.activate
def test_repositories_delete_success(tsc, repository):
    """
    test repositories delete for success
    """
    responses.delete(
        'https://nourl/rest/repository/6',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550707450,
        },
    )
    tsc.repositories.delete(int(repository['id']))


def test_repositories_edit_id_typeerror(tsc):
    """
    test repositories edit for id type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.edit('one')


@responses.activate
def test_repositories_edit_success(tsc, repository):
    """
    test repositories edit for success
    """
    responses.patch(
        'https://nourl/rest/repository/6',
        json={
            'type': 'regular',
            'response': {
                'id': '16',
                'name': 'New Name',
                'description': '',
                'type': 'Local',
                'dataFormat': 'IPv4',
                'remoteID': None,
                'remoteIP': None,
                'running': 'false',
                'downloadFormat': 'v2',
                'lastSyncTime': '0',
                'createdTime': '1550708727',
                'modifiedTime': '1550708727',
                'lastVulnUpdate': '1550708727',
                'vulnCount': '0',
                'organizations': [],
                'typeFields': {
                    'correlation': [],
                    'nessusSchedule': {'type': 'never', 'start': '', 'repeatRule': ''},
                    'ipRange': '0.0.0.0/0',
                    'ipCount': '0',
                    'runningNessus': 'false',
                    'lastGenerateNessusTime': '0',
                    'trendingDays': '0',
                    'trendWithRaw': 'false',
                    'lastTrendUpdate': '0',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550708727,
        },
    )
    repository = tsc.repositories.edit(int(repository['id']), name='New Name')
    assert isinstance(repository, dict)
    check(repository, 'createdTime', str)
    check(repository, 'dataFormat', str)
    check(repository, 'description', str)
    check(repository, 'downloadFormat', str)
    check(repository, 'id', str)
    check(repository, 'lastSyncTime', str)
    check(repository, 'lastVulnUpdate', str)
    check(repository, 'modifiedTime', str)
    check(repository, 'name', str)
    check(repository, 'organizations', list)
    check(repository, 'remoteID', str, allow_none=True)
    check(repository, 'remoteIP', str, allow_none=True)
    check(repository, 'running', str)
    check(repository, 'type', str)
    check(repository, 'typeFields', dict)
    check(repository['typeFields'], 'correlation', list)
    check(repository['typeFields'], 'ipCount', str)
    check(repository['typeFields'], 'ipRange', str)
    check(repository['typeFields'], 'lastGenerateNessusTime', str)
    check(repository['typeFields'], 'lastTrendUpdate', str)
    check(repository['typeFields'], 'nessusSchedule', dict)
    check(repository['typeFields']['nessusSchedule'], 'repeatRule', str)
    check(repository['typeFields']['nessusSchedule'], 'start', str)
    check(repository['typeFields']['nessusSchedule'], 'type', str)
    check(repository['typeFields'], 'runningNessus', str)
    check(repository['typeFields'], 'trendWithRaw', str)
    check(repository['typeFields'], 'trendingDays', str)
    check(repository, 'vulnCount', str)


def test_repositories_rules_constructor_plugin_id_typeerror(tsc):
    """
    test repositories rules constructor for 'plugin id' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._rules_constructor(plugin_id='one')


def test_repositories_rules_constructor_port_typeerror(tsc):
    """
    test repositories rules constructor for 'port' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._rules_constructor(port='one')


def test_repositories_rules_constructor_org_typeerror(tsc):
    """
    test repositories rules constructor for 'org' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._rules_constructor(orgs=1)


def test_repositories_rules_constructor_org_item_typeerror(tsc):
    """
    test repositories rules constructor for 'org item' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._rules_constructor(orgs=['one'])


def test_repositories_rules_constructor_fields_typeerror(tsc):
    """
    test repositories rules constructor for 'fields' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._rules_constructor(fields=1)


def test_repositories_rules_constructor_field_item_typeerror(tsc):
    """
    test repositories rules constructor for 'field item' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories._rules_constructor(fields=[1])


def test_repositories_rules_constructor_success(tsc):
    """
    test repositories rules constructor for success
    """
    resp = tsc.repositories._rules_constructor(
        plugin_id=1, port=1, orgs=[1, 2], fields=['name1', 'name2']
    )
    assert resp == {
        'pluginID': 1,
        'port': 1,
        'organizationIDs': '1,2',
        'fields': 'name1,name2',
    }


def test_repositories_accept_risk_rules_id_typeerror(tsc):
    """
    test repositories accept risk rules for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.accept_risk_rules('one')


@pytest.mark.skip(reason='Need VCRed data to test against')
def test_repositories_accept_risk_rules_success():
    """
    test repositories accept risk rules for success
    """
    pass


def test_repositories_recast_risk_rules_id_typeerror(tsc):
    """
    test repositories recast risk rules for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.recast_risk_rules('one')


@pytest.mark.skip(reason='Need VCRed data to test against')
def test_repositories_recast_risk_rules_success():
    """
    test repositories recast risk rules for success
    """
    pass


def test_repositories_asset_intersections_id_typeerror(tsc):
    """
    test repositories asset intersections for id type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.asset_intersections('one')


def test_repositories_asset_intersections_uuid_typeerror(tsc):
    """
    test repositories asset intersections for uuid type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.asset_intersections(1, uuid=1)


def test_repositories_asset_intersections_uuid_unexpectedvalueerror(tsc):
    """
    test repositories asset intersections for uuid unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.repositories.asset_intersections(1, uuid='something')


def test_repositories_asset_intersections_dns_typerrror(tsc):
    """
    test repositories asset intersections for dns type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.asset_intersections(1, dns=1)


def test_repositories_asset_intersections_ip_typeerror(tsc):
    """
    test repositories asset intersections for ip type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.asset_intersections(1, ip=1)


@responses.activate
def test_repositories_asset_intersections_success(tsc, repository):
    """
    test repositories asset intersections for success
    """
    responses.get(
        'https://nourl/rest/repository/6/assetIntersections',
        json={
            'type': 'regular',
            'response': {
                'assets': [
                    {
                        'id': '0',
                        'name': 'All Defined Ranges',
                        'description': 'All defining ranges of the Group in whose context this Asset is being evaluated.',
                    }
                ]
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550766230,
        },
        match=[m.query_param_matcher({'ip': '192.168.0.1'})],
    )
    asset_lists = tsc.repositories.asset_intersections(
        int(repository['id']), ip_address='192.168.0.1'
    )
    assert isinstance(asset_lists, list)
    for asset_list in asset_lists:
        check(asset_list, 'description', str)
        check(asset_list, 'id', str)
        check(asset_list, 'name', str)


def test_repositories_import_repository_id_typeerror(tsc):
    """
    test repositories import repository for id type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.import_repository('one', 1)


@pytest.mark.datafiles(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'test_files', 'sc_repo.tgz'
    )
)
@responses.activate
def test_repositories_import_repository_success(tsc, datafiles, repository):
    """
    test repositories import repository for success
    """
    responses.post(
        'https://nourl/rest/file/upload',
        json={
            'type': 'regular',
            'response': {
                'filename': 'AXz9bd',
                'originalFilename': 'example_repo.tgz',
                'content': '',
                'context': '',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550775513,
        },
    )
    responses.post(
        'https://nourl/rest/repository/6/import',
        json={
            'type': 'regular',
            'response': {
                'objectID': '17',
                'objectType': 'importRepository',
                'type': 'now',
                'ownerID': '1',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550775513,
        },
    )
    # offline = admin.repositories.create(name='Offline', type='Offline')
    with open(os.path.join(str(datafiles), 'sc_repo.tgz'), 'rb') as repo:
        tsc.repositories.import_repository(int(repository['id']), repo)


def test_repositories_export_repository_id_typeerror(tsc):
    """
    test repositories export repository for id type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.export_repository('one', 1)


@responses.activate
def test_repositories_export_repository_success(tsc, repository):
    """
    test repositories export repository for success
    """
    responses.get(
        'https://nourl/rest/repository/6/export',
        body=b'repository archive',
        content_type='application/x-compressed',
        headers={'content-disposition': 'attachment; filename=repository-4.tar.gz'},
    )
    with open('{}'.format(repository['id']), 'wb') as repo:
        tsc.repositories.export_repository(int(repository['id']), repo)
    os.remove('{}'.format(repository['id']))


def test_repositories_device_info_id_typeerror(tsc):
    """
    test repositories device info for id type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.device_info('one')


def test_repositories_device_into_dns_typeerror(tsc):
    """
    test repositories device info for dns type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.device_info(1, dns=1)


def test_repositories_device_info_ip_typeerror(tsc):
    """
    test repositories device info for ip type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.device_info(1, ip=1)


def test_repositories_device_info_uuid_typeerror(tsc):
    """
    test repositories device info for uuid type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.device_info(1, uuid=1)


def test_repositories_device_info_uuid_unexpectedvalueerror(tsc):
    """
    test repositories device info for uuid unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.repositories.device_info(1, uuid='something')


def test_repositories_device_info_fields_typeerror(tsc):
    """
    test repositories device info for fields type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.device_info(1, fields=1)


def test_repositories_device_info_field_item_typeerror(tsc):
    """
    test repositories device info for 'field item' type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.device_info(1, fields=[1])


@responses.activate
def test_repositories_device_info_success(tsc, repository):
    """
    test repositories device info for success
    """
    responses.get(
        'https://nourl/rest/repository/6/deviceInfo',
        json={
            'type': 'regular',
            'response': {
                'ip': '192.168.0.1',
                'uuid': '16ee04f6-e9fa-4394-a9d9-f3823c3b1919',
                'score': '1',
                'total': '98',
                'severityInfo': '97',
                'severityLow': '1',
                'severityMedium': '0',
                'severityHigh': '0',
                'severityCritical': '0',
                'macAddress': '00:0c:29:91:cc:a3',
                'policyName': '6d32dff0-2e6e-5fef-982f-80b05a31fcad-54229/Full Safe Scan',
                'pluginSet': '201902181242',
                'netbiosName': 'UNKNOWN\\server',
                'dnsName': 'server',
                'osCPE': 'cpe:/o:centos:centos:7:update6',
                'biosGUID': '564d0761-89f2-b58d-b62a-bf54b191cca3',
                'tpmID': '',
                'mcafeeGUID': '',
                'lastAuthRun': '1550643025',
                'lastUnauthRun': '1550184636',
                'uniqueness': 'repositoryID,ip,dnsName',
                'severityAll': '0,0,0,1,97',
                'os': 'Linux Kernel 3.10.0-862.14.4.el7.x86_64 on CentOS Linux release 7.6.1810 (Core)',
                'hasPassive': 'No',
                'hasCompliance': 'No',
                'lastScan': '1550647873',
                'links': [],
                'repository': {'id': '1', 'name': 'Default', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550766130,
        },
        match=[m.query_param_matcher({'dnsName': 'server'})],
    )
    repo = tsc.repositories.device_info(int(repository['id']), dns='server')
    assert isinstance(repo, dict)
    check(repo, 'biosGUID', str)
    check(repo, 'hasCompliance', str)
    check(repo, 'hasPassive', str)
    check(repo, 'ip', str)
    check(repo, 'lastAuthRun', str)
    check(repo, 'lastScan', str)
    check(repo, 'lastUnauthRun', str)
    check(repo, 'links', list)
    check(repo, 'macAddress', str)
    check(repo, 'mcafeeGUID', str)
    check(repo, 'netbiosName', str)
    check(repo, 'os', str)
    check(repo, 'osCPE', str)
    check(repo, 'pluginSet', str)
    check(repo, 'pluginSet', str)
    check(repo, 'policyName', str)
    check(repo, 'repository', dict)
    check(repo['repository'], 'description', str)
    check(repo['repository'], 'id', str)
    check(repo['repository'], 'name', str)
    check(repo, 'score', str)
    check(repo, 'severityAll', str)
    check(repo, 'severityCritical', str)
    check(repo, 'severityInfo', str)
    check(repo, 'severityLow', str)
    check(repo, 'severityMedium', str)
    check(repo, 'total', str)
    check(repo, 'tpmID', str)
    check(repo, 'uniqueness', str)
    check(repo, 'uuid', str)


@responses.activate
def test_repositories_device_info_success_ip_info(tsc, repository):
    """
    test repositories device info success with ip info
    """
    responses.get(
        'https://nourl/rest/repository/6/ipInfo',
        json={
            'type': 'regular',
            'response': {
                'ip': '192.168.0.1',
                'uuid': '16ee04f6-e9fa-4394-a9d9-f3823c3b1919',
                'score': '1',
                'total': '98',
                'severityInfo': '97',
                'severityLow': '1',
                'severityMedium': '0',
                'severityHigh': '0',
                'severityCritical': '0',
                'macAddress': '00:0c:29:91:cc:a3',
                'policyName': '6d32dff0-2e6e-5fef-982f-80b05a31fcad-54229/Full Safe Scan',
                'pluginSet': '201902181242',
                'netbiosName': 'UNKNOWN\\server',
                'dnsName': 'server',
                'osCPE': 'cpe:/o:centos:centos:7:update6',
                'biosGUID': '564d0761-89f2-b58d-b62a-bf54b191cca3',
                'tpmID': '',
                'mcafeeGUID': '',
                'lastAuthRun': '1550643025',
                'lastUnauthRun': '1550184636',
                'uniqueness': 'repositoryID,ip,dnsName',
                'severityAll': '0,0,0,1,97',
                'os': 'Linux Kernel 3.10.0-862.14.4.el7.x86_64 on CentOS Linux release 7.6.1810 (Core)',
                'hasPassive': 'No',
                'hasCompliance': 'No',
                'lastScan': '1550647873',
                'links': [],
                'repository': {'id': '1', 'name': 'Default', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550766130,
        },
        match=[m.query_param_matcher({'dnsName': 'server'})],
    )
    tsc._version = '5.6.0'
    repo = tsc.repositories.device_info(int(repository['id']), dns='server')
    assert isinstance(repo, dict)
    check(repo, 'biosGUID', str)
    check(repo, 'hasCompliance', str)
    check(repo, 'hasPassive', str)
    check(repo, 'ip', str)


def test_repositories_remote_authorize_host_typeerror(tsc):
    """
    test repositories remote authorize for host type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.remote_authorize(1, 'user', 'pass')


def test_repositories_remote_authorize_username_typeerror(tsc):
    """
    test repositories remote authorize for username type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.remote_authorize('host', 1, 'pass')


def test_repositories_remote_authorize_password_typeerror(tsc):
    """
    test repositories remote authorize for password type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.remote_authorize('host', 'user', 1)


@pytest.mark.skip(reason='No Downstream SC to Test with yet')
def test_repositories_remote_authorize_success():
    """
    test repositories remote authorize for success
    """
    pass


def test_repositories_remote_fetch_host_typeerror(tsc):
    """
    test repositories remote fetch for host type error
    """
    with pytest.raises(TypeError):
        tsc.repositories.remote_fetch(1)


@pytest.mark.skip(reason='No Downstream SC to Test with yet')
def test_repositories_remote_fetch_success():
    """
    test repositories remote fetch for success
    """
    pass


@responses.activate(registry=OrderedRegistry)
def test_repository_create_types(tsc):
    responses.post(
        'https://nourl/rest/repository',
        json={'response': {}, 'error_code': 0},
        match=[
            m.json_params_matcher(
                {
                    'name': 'test',
                    'type': 'Local',
                    'dataFormat': 'IPv4',
                    'trendingDays': 0,
                    'trendWithRaw': 'false',
                    'ipRange': '0.0.0.0/0',
                    'nessusSchedule': {'type': 'never'},
                }
            )
        ],
    )
    responses.post(
        'https://nourl/rest/repository',
        json={'response': {}, 'error_code': 0},
        match=[
            m.json_params_matcher(
                {
                    'name': 'test',
                    'type': 'Local',
                    'dataFormat': 'IPv6',
                    'trendingDays': 0,
                    'trendWithRaw': 'false',
                    'ipRange': '::/0',
                    'nessusSchedule': {'type': 'never'},
                }
            )
        ],
    )
    responses.post(
        'https://nourl/rest/repository',
        json={'response': {}, 'error_code': 0},
        match=[
            m.json_params_matcher(
                {
                    'name': 'test',
                    'type': 'Local',
                    'dataFormat': 'universal',
                    'trendingDays': 0,
                    'trendWithRaw': 'false',
                    'ipRange': '0.0.0.0/0, ::/0',
                    'nessusSchedule': {'type': 'never'},
                }
            )
        ],
    )
    tsc.repositories.create(name='test', format='IPv4')
    tsc.repositories.create(name='test', format='IPv6')
    tsc.repositories.create(name='test', format='universal')
