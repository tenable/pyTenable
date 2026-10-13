"""
test file for testing various scenarios in security center organizations
functionality
"""

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError
from ..checker import check


def test_organizations_constructor_name_typeerror(tsc):
    """
    test organizations constructor for name type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(name=1)


def test_organizations_constructor_description_typeerror(tsc):
    """
    test organizations constructor for description type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(description=1)


def test_organizations_constructor_address_typeerror(tsc):
    """
    test organizations constructor for address type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(address=1)


def test_organizations_constructor_city_typeerror(tsc):
    """
    test organizations constructor for city type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(city=1)


def test_organizations_constructor_state_typeerror(tsc):
    """
    test organizations constructor for state type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(state=1)


def test_organizations_constructor_country_typeerror(tsc):
    """
    test organizations constructor for country type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(country=1)


def test_organizations_constructor_phone_typeerror(tsc):
    """
    test organizations constructor for phone type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(phone=1)


def test_organizations_constructor_lce_ids_typeerror(tsc):
    """
    test organizations constructor for lce ids type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(lce_ids=1)


def test_organizations_constructor_lce_ids_item_typeerror(tsc):
    """
    test organizations constructor for 'lce ids item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(
            lce_ids=[
                'one',
            ]
        )


def test_organizations_constructor_zone_selection_typeerror(tsc):
    """
    test organizations constructor for 'zone selection' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(zone_selection=1)


def test_organizations_constructor_zone_selection_unexpectedvalueerror(tsc):
    """
    test organizations constructor for 'zone selection' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.organizations._constructor(zone_selection='something')


def test_organizations_constructor_restricted_ips_typeerror(tsc):
    """
    test organizations constructor for 'restricted ips' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(restricted_ips=1)


def test_organizations_constructor_restricted_ips_item_typeerror(tsc):
    """
    test organizations constructor for 'restricted ips item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(restricted_ips=[1])


def test_organizations_constructor_repos_typeerror(tsc):
    """
    test organizations constructor for 'repos' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(repos=1)


def test_organizations_constructor_repos_item_typeerror(tsc):
    """
    test organizations constructor for 'repos item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(repos=['one'])


def test_organizations_constructor_pub_sites_typeerror(tsc):
    """
    test organizations constructor for 'pub sites' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(pub_sites=1)


def test_organizations_constructor_pub_sites_item_typeerror(tsc):
    """
    test organizations constructor for 'pub sites item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(pub_sites=['one'])


def test_organizations_constructor_ldap_ids_typeerror(tsc):
    """
    test organizations constructor for 'ldap ids' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(ldap_ids=1)


def test_organizations_constructor_ldap_ids_item_typeerror(tsc):
    """
    test organizations constructor for 'ldap ids item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(ldap_ids=['one'])


def test_organizations_constructor_nessus_managers_typeerror(tsc):
    """
    test organizations constructor for 'nessus managers' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(nessus_managers=1)


def test_organizations_constructor_nessus_managers_item_typeerror(tsc):
    """
    test organizations constructor for 'nessus managers item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(nessus_managers=['one'])


def test_organizations_constructor_info_links_typeerror(tsc):
    """
    test organizations constructor for 'info links' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(info_links=1)


def test_organizations_constructor_info_links_item_typeerror(tsc):
    """
    test organizations constructor for 'info links item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(info_links=[1])


def test_organizations_constructor_info_links_item_name_typeerror(tsc):
    """
    test organizations constructor for 'info links item name' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(info_links=[(1, 'http://site.com/%IP%')])


def test_organizations_constructor_info_links_item_link_typeerror(tsc):
    """
    test organizations constructor for 'info links item link' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(info_links=[('name', 1)])


def test_organizations_constructor_vuln_score_low_typeerror(tsc):
    """
    test organizations constructor for 'vulnerability score low' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(vuln_score_low='one')


def test_organizations_constructor_vuln_score_medium_typeerror(tsc):
    """
    test organizations constructor for 'vulnerability score medium' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(vuln_score_medium='one')


def test_organizations_constructor_vuln_score_high_typeerror(tsc):
    """
    test organizations constructor for 'vulnerability score high' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(vuln_score_high='one')


def test_organizations_constructor_vuln_score_critical_typeerror(tsc):
    """
    test organizations constructor for 'vulnerability score critical' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations._constructor(vuln_score_critical='one')


def test_organizations_constructor_success(tsc):
    """
    test organizations constructor for success
    """
    organization = tsc.organizations._constructor(
        name='name',
        description='description',
        address='123 main street',
        city='anytown',
        state='IL',
        country='USA',
        phone='999.888.7766',
        lce_ids=[1, 2, 3],
        zone_selection='auto_only',
        restricted_ips=['127.0.0.1', '127.0.0.0/8'],
        repos=[1, 2, 3],
        pub_sites=[1, 2, 3],
        ldap_ids=[1, 2, 3],
        nessus_managers=[1, 2, 3],
        info_links=[('link', 'http://url/%IP%')],
        vuln_score_low=1,
        vuln_score_medium=5,
        vuln_score_high=10,
        vuln_score_critical=40,
    )
    assert organization == {
        'name': 'name',
        'description': 'description',
        'address': '123 main street',
        'city': 'anytown',
        'state': 'IL',
        'country': 'USA',
        'phone': '999.888.7766',
        'lces': [{'id': 1}, {'id': 2}, {'id': 3}],
        'zoneSelection': 'auto_only',
        'restrictedIPs': '127.0.0.1,127.0.0.0/8',
        'repositories': [{'id': 1}, {'id': 2}, {'id': 3}],
        'pubSites': [{'id': 1}, {'id': 2}, {'id': 3}],
        'ldaps': [{'id': 1}, {'id': 2}, {'id': 3}],
        'nessusManagers': [{'id': 1}, {'id': 2}, {'id': 3}],
        'ipInfoLinks': [{'name': 'link', 'link': 'http://url/%IP%'}],
        'vulnScoreLow': 1,
        'vulnScoreMedium': 5,
        'vulnScoreHigh': 10,
        'vulnScoreCritical': 40,
    }


@pytest.fixture
def org():
    """
    test fixture for organization
    """
    return {
        'id': '2',
        'name': 'New Org',
        'description': '',
        'email': '',
        'address': '',
        'city': '',
        'state': '',
        'country': '',
        'phone': '',
        'fax': '',
        'ipInfoLinks': [],
        'zoneSelection': 'auto_only',
        'restrictedIPs': '',
        'vulnScoreLow': '1',
        'vulnScoreMedium': '3',
        'vulnScoreHigh': '10',
        'vulnScoreCritical': '40',
        'createdTime': '1557322695',
        'modifiedTime': '1557322695',
        'userCount': '0',
        'lces': [],
        'repositories': [],
        'zones': [],
        'nessusManagers': [],
        'pubSites': [],
        'ldaps': [],
    }


@responses.activate
def test_organizations_create_success(tsc):
    """
    test organizations create for success
    """
    responses.post(
        'https://nourl/rest/organization',
        json={
            'type': 'regular',
            'response': {
                'id': '2',
                'name': 'New Org',
                'description': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'ipInfoLinks': [],
                'zoneSelection': 'auto_only',
                'restrictedIPs': '',
                'vulnScoreLow': '1',
                'vulnScoreMedium': '3',
                'vulnScoreHigh': '10',
                'vulnScoreCritical': '40',
                'createdTime': '1557322695',
                'modifiedTime': '1557322695',
                'userCount': '0',
                'lces': [],
                'repositories': [],
                'zones': [],
                'nessusManagers': [],
                'pubSites': [],
                'ldaps': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322695,
        },
    )
    org = tsc.organizations.create('New Org')
    assert isinstance(org, dict)
    check(org, 'id', str)
    check(org, 'name', str)
    check(org, 'description', str)
    check(org, 'email', str)
    check(org, 'address', str)
    check(org, 'city', str)
    check(org, 'state', str)
    check(org, 'country', str)
    check(org, 'phone', str)
    check(org, 'fax', str)
    check(org, 'ipInfoLinks', list)
    for i in org['ipInfoLinks']:
        check(i, 'name', str)
        check(i, 'link', str)
    check(org, 'zoneSelection', str)
    check(org, 'restrictedIPs', str)
    check(org, 'vulnScoreLow', str)
    check(org, 'vulnScoreMedium', str)
    check(org, 'vulnScoreHigh', str)
    check(org, 'vulnScoreCritical', str)
    check(org, 'createdTime', str)
    check(org, 'modifiedTime', str)
    check(org, 'userCount', str)
    check(org, 'lces', list)
    for lces in org['lces']:
        check(lces, 'id', str)
        check(lces, 'name', str)
        check(lces, 'description', str)
    check(org, 'repositories', list)
    for repository in org['repositories']:
        check(repository, 'id', str)
        check(repository, 'name', str)
        check(repository, 'description', str)
        check(repository, 'type', str)
        check(repository, 'dataFormat', str)
        check(repository, 'groupAssign', str)
    check(org, 'zones', list)
    for zone in org['zones']:
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)
    check(org, 'ldaps', list)
    for ldaps in org['ldaps']:
        check(ldaps, 'id', str)
        check(ldaps, 'name', str)
        check(ldaps, 'description', str)
    check(org, 'nessusManagers', list)
    for manager in org['nessusManagers']:
        check(manager, 'id', str)
        check(manager, 'name', str)
        check(manager, 'description', str)
    check(org, 'pubSites', list)
    for pub_sites in org['pubSites']:
        check(pub_sites, 'id', str)
        check(pub_sites, 'name', str)
        check(pub_sites, 'description', str)


@responses.activate
def test_organizations_delete_success(tsc, org):
    """
    test organizations delete for success
    """
    responses.delete(
        'https://nourl/rest/organization/2',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322697,
        },
    )
    tsc.organizations.delete(int(org['id']))


@responses.activate
def test_organizations_list_success(tsc):
    """
    test organizations list for success
    """
    responses.get(
        'https://nourl/rest/organization',
        json={
            'type': 'regular',
            'response': [
                {'id': '3', 'name': 'New Org', 'description': ''},
                {'id': '4', 'name': 'New Org', 'description': ''},
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322935,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    organizations = tsc.organizations.list(fields=['id', 'name', 'description'])
    assert isinstance(organizations, list)
    for organization in organizations:
        check(organization, 'id', str)
        check(organization, 'name', str)
        check(organization, 'description', str)


@responses.activate
def test_organizations_managers_list_success(tsc):
    """
    test organization managers list for success
    """
    responses.get(
        'https://nourl/rest/organization/1/securityManager',
        json={
            'type': 'regular',
            'response': [
                {'id': '3', 'name': 'Sec Manager3', 'description': ''},
                {'id': '4', 'name': 'Sec Manager4', 'description': ''},
            ],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322935,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    managers = tsc.organizations.managers_list(
        org_id=1, fields=['id', 'name', 'description']
    )
    assert isinstance(managers, list)
    for manager in managers:
        check(manager, 'id', str)
        check(manager, 'name', str)
        check(manager, 'description', str)


@responses.activate
def test_organizations_manager_details_success(tsc):
    """
    test organizations manager details for success
    """
    responses.get(
        'https://nourl/rest/organization/1/securityManager/1',
        json={
            'type': 'regular',
            'response': {'id': '1', 'name': 'Sec Manager1', 'description': ''},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322935,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    manager = tsc.organizations.manager_details(
        org_id=1, user_id=1, fields=['id', 'name', 'description']
    )
    assert isinstance(manager, dict)
    check(manager, 'id', str)
    check(manager, 'name', str)
    check(manager, 'description', str)


@responses.activate
def test_organizations_manager_create_edit_delete_success(tsc):
    """
    test organizations manager create, edit and delete for success
    """
    responses.post(
        'https://nourl/rest/organization/1/securityManager',
        json={
            'type': 'regular',
            'response': {
                'id': '1',
                'name': 'New Sec Manager',
                'description': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'ipInfoLinks': [],
                'zoneSelection': 'auto_only',
                'restrictedIPs': '',
                'vulnScoreLow': '1',
                'vulnScoreMedium': '3',
                'vulnScoreHigh': '10',
                'vulnScoreCritical': '40',
                'createdTime': '1557322695',
                'modifiedTime': '1557322695',
                'userCount': '0',
                'lces': [],
                'repositories': [],
                'zones': [],
                'nessusManagers': [],
                'pubSites': [],
                'ldaps': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322695,
        },
    )
    responses.patch(
        'https://nourl/rest/organization/1/securityManager/1',
        json={
            'type': 'regular',
            'response': {
                'id': '1',
                'name': 'new mgr name',
                'description': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'ipInfoLinks': [],
                'zoneSelection': 'auto_only',
                'restrictedIPs': '',
                'vulnScoreLow': '1',
                'vulnScoreMedium': '3',
                'vulnScoreHigh': '10',
                'vulnScoreCritical': '40',
                'createdTime': '1557322695',
                'modifiedTime': '1557322695',
                'userCount': '0',
                'lces': [],
                'repositories': [],
                'zones': [],
                'nessusManagers': [],
                'pubSites': [],
                'ldaps': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322695,
        },
    )
    responses.delete(
        'https://nourl/rest/organization/1/securityManager/1',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322697,
        },
    )
    manager = tsc.organizations.manager_create(
        org_id=1, username='username', password='password', role=1
    )
    assert isinstance(manager, dict)
    check(manager, 'id', str)
    check(manager, 'name', str)
    check(manager, 'description', str)

    manager = tsc.organizations.manager_edit(
        user_id=int(manager['id']), org_id=1, name='new mgr name'
    )
    assert isinstance(manager, dict)
    check(manager, 'id', str)
    check(manager, 'name', str)
    check(manager, 'description', str)

    tsc.organizations.manager_delete(org_id=1, user_id=1, migrate_to=1)


@responses.activate
def test_organizations_details_success(tsc, org):
    """
    test organizations details for success
    """
    responses.get(
        'https://nourl/rest/organization/2',
        json={
            'type': 'regular',
            'response': {
                'id': '3',
                'name': 'New Org',
                'description': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'ipInfoLinks': [],
                'zoneSelection': 'auto_only',
                'restrictedIPs': '',
                'vulnScoreLow': '1',
                'vulnScoreMedium': '3',
                'vulnScoreHigh': '10',
                'vulnScoreCritical': '40',
                'createdTime': '1557322933',
                'modifiedTime': '1557322933',
                'userCount': '0',
                'lces': [],
                'repositories': [],
                'zones': [],
                'nessusManagers': [],
                'pubSites': [],
                'ldaps': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322935,
        },
    )
    organization = tsc.organizations.details(int(org['id']))
    assert isinstance(organization, dict)
    check(organization, 'id', str)
    check(organization, 'name', str)
    check(organization, 'description', str)
    check(organization, 'email', str)
    check(organization, 'address', str)
    check(organization, 'city', str)
    check(organization, 'state', str)
    check(organization, 'country', str)
    check(organization, 'phone', str)
    check(organization, 'fax', str)
    check(organization, 'ipInfoLinks', list)
    for ip_info in organization['ipInfoLinks']:
        check(ip_info, 'name', str)
        check(ip_info, 'link', str)
    check(organization, 'zoneSelection', str)
    check(organization, 'restrictedIPs', str)
    check(organization, 'vulnScoreLow', str)
    check(organization, 'vulnScoreMedium', str)
    check(organization, 'vulnScoreHigh', str)
    check(organization, 'vulnScoreCritical', str)
    check(organization, 'createdTime', str)
    check(organization, 'modifiedTime', str)
    check(organization, 'userCount', str)
    check(organization, 'lces', list)
    for lces in organization['lces']:
        check(lces, 'id', str)
        check(lces, 'name', str)
        check(lces, 'description', str)
    check(organization, 'repositories', list)
    for repository in organization['repositories']:
        check(repository, 'id', str)
        check(repository, 'name', str)
        check(repository, 'description', str)
        check(repository, 'type', str)
        check(repository, 'dataFormat', str)
        check(repository, 'groupAssign', str)
    check(organization, 'zones', list)
    for zone in organization['zones']:
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)
    check(organization, 'ldaps', list)
    for ldap in organization['ldaps']:
        check(ldap, 'id', str)
        check(ldap, 'name', str)
        check(ldap, 'description', str)
    check(organization, 'nessusManagers', list)
    for manager in organization['nessusManagers']:
        check(manager, 'id', str)
        check(manager, 'name', str)
        check(manager, 'description', str)
    check(organization, 'pubSites', list)
    for pub_site in organization['pubSites']:
        check(pub_site, 'id', str)
        check(pub_site, 'name', str)
        check(pub_site, 'description', str)


@responses.activate
def test_organizations_details_success_for_fields(tsc, org):
    """
    test organizations details success for fields
    """
    responses.get(
        'https://nourl/rest/organization/2',
        json={
            'type': 'regular',
            'response': {'id': '3', 'name': 'New Org', 'description': ''},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322935,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name,description'})],
    )
    organization = tsc.organizations.details(
        int(org['id']), fields=['id', 'name', 'description']
    )
    assert isinstance(organization, dict)
    check(organization, 'id', str)
    check(organization, 'name', str)
    check(organization, 'description', str)


@responses.activate
def test_organizations_edit_success(tsc, org):
    """
    test organizations edit for success
    """
    responses.patch(
        'https://nourl/rest/organization/2',
        json={
            'type': 'regular',
            'response': {
                'id': '4',
                'name': 'new org name',
                'description': '',
                'email': '',
                'address': '',
                'city': '',
                'state': '',
                'country': '',
                'phone': '',
                'fax': '',
                'ipInfoLinks': [],
                'zoneSelection': 'auto_only',
                'restrictedIPs': '',
                'vulnScoreLow': '1',
                'vulnScoreMedium': '3',
                'vulnScoreHigh': '10',
                'vulnScoreCritical': '40',
                'createdTime': '1557322978',
                'modifiedTime': '1557322980',
                'userCount': '0',
                'lces': [],
                'repositories': [],
                'zones': [],
                'nessusManagers': [],
                'pubSites': [],
                'ldaps': [],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557322980,
        },
    )
    organization = tsc.organizations.edit(int(org['id']), name='new org name')
    assert isinstance(organization, dict)
    check(organization, 'id', str)
    check(organization, 'name', str)
    check(organization, 'description', str)
    check(organization, 'email', str)
    check(organization, 'address', str)
    check(organization, 'city', str)
    check(organization, 'state', str)
    check(organization, 'country', str)
    check(organization, 'phone', str)
    check(organization, 'fax', str)
    check(organization, 'ipInfoLinks', list)
    for ip_info in organization['ipInfoLinks']:
        check(ip_info, 'name', str)
        check(ip_info, 'link', str)
    check(organization, 'zoneSelection', str)
    check(organization, 'restrictedIPs', str)
    check(organization, 'vulnScoreLow', str)
    check(organization, 'vulnScoreMedium', str)
    check(organization, 'vulnScoreHigh', str)
    check(organization, 'vulnScoreCritical', str)
    check(organization, 'createdTime', str)
    check(organization, 'modifiedTime', str)
    check(organization, 'userCount', str)
    check(organization, 'lces', list)
    for lces in organization['lces']:
        check(lces, 'id', str)
        check(lces, 'name', str)
        check(lces, 'description', str)
    check(organization, 'repositories', list)
    for repository in organization['repositories']:
        check(repository, 'id', str)
        check(repository, 'name', str)
        check(repository, 'description', str)
        check(repository, 'type', str)
        check(repository, 'dataFormat', str)
        check(repository, 'groupAssign', str)
    check(organization, 'zones', list)
    for zone in organization['zones']:
        check(zone, 'id', str)
        check(zone, 'name', str)
        check(zone, 'description', str)
    check(organization, 'ldaps', list)
    for ldap in organization['ldaps']:
        check(ldap, 'id', str)
        check(ldap, 'name', str)
        check(ldap, 'description', str)
    check(organization, 'nessusManagers', list)
    for manager in organization['nessusManagers']:
        check(manager, 'id', str)
        check(manager, 'name', str)
        check(manager, 'description', str)
    check(organization, 'pubSites', list)
    for pub_site in organization['pubSites']:
        check(pub_site, 'id', str)
        check(pub_site, 'name', str)
        check(pub_site, 'description', str)


def test_organizations_accept_risk_rules_id_typeerror(tsc):
    """
    test organizations accept risk rules for id type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.accept_risk_rules('one')


def test_organizations_accept_risk_rules_repos_typeerror(tsc):
    """
    test organizations accept risk rules for repo type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.accept_risk_rules(1, repos=1)


def test_organizations_accept_risk_rules_repos_item_typeerror(tsc):
    """
    test organizations accept risk rules for 'repos item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.accept_risk_rules(1, repos=['one'])


def test_organizations_accept_risk_rules_plugin_typeerror(tsc):
    """
    test organizations accept risk rules for plugin type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.accept_risk_rules(1, plugin='one')


def test_organizations_accept_risk_rules_port_typeerror(tsc):
    """
    test organizations accept risk rules for port type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.accept_risk_rules(1, port='one')


@responses.activate
def test_organizations_accept_risk_rules_success(tsc, org):
    """
    test organizations accept risk rules for success
    """
    responses.get(
        'https://nourl/rest/organization/2/acceptRiskRule',
        json={
            'type': 'regular',
            'response': [],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557324762,
        },
    )
    rules = tsc.organizations.accept_risk_rules(int(org['id']))
    assert isinstance(rules, list)
    for rule in rules:
        check(rule, 'id', str)
        check(rule, 'hostType', str)
        check(rule, 'hostValue', str)
        check(rule, 'port', str)
        check(rule, 'protocol', str)
        check(rule, 'expires', str)
        check(rule, 'status', str)
        check(rule, 'repository', dict)
        check(rule['repository'], 'id', str)
        check(rule['repository'], 'name', str)
        check(rule['repository'], 'description', str)
        check(rule, 'organization', dict)
        check(rule['organization'], 'id', str)
        check(rule['organization'], 'name', str)
        check(rule['organization'], 'description', str)
        check(rule, 'user', dict)
        check(rule['user'], 'id', str)
        check(rule['user'], 'username', str)
        check(rule['user'], 'firstname', str)
        check(rule['user'], 'lastname', str)
        check(rule, 'plugin', dict)
        check(rule['plugin'], 'id', str)
        check(rule['plugin'], 'name', str)
        check(rule['plugin'], 'description', str)


def test_organizations_recast_risk_rules_id_typeerror(tsc):
    """
    test organizations recast risk rules for id type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.recast_risk_rules('one')


def test_organizations_recast_risk_rules_repos_typeerror(tsc):
    """
    test organizations recast risk rules for repos type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.recast_risk_rules(1, repos=1)


def test_organizations_recast_risk_rules_repos_item_typeerror(tsc):
    """
    test organizations recast risk rules for 'repos item' type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.recast_risk_rules(1, repos=['one'])


def test_organizations_recast_risk_rules_plugin_typeerror(tsc):
    """
    test organizations recast risk rules for plugin type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.recast_risk_rules(1, plugin='one')


def test_organizations_recast_risk_rules_port_typeerror(tsc):
    """
    test organizations recast risk rules for port type error
    """
    with pytest.raises(TypeError):
        tsc.organizations.recast_risk_rules(1, port='one')


@responses.activate
def test_organizations_recast_risk_rules_success(tsc, org):
    """
    test organizations recast risk rules for success
    """
    responses.get(
        'https://nourl/rest/organization/2/recastRiskRule',
        json={
            'type': 'regular',
            'response': [],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1557324775,
        },
    )
    rules = tsc.organizations.recast_risk_rules(int(org['id']))
    assert isinstance(rules, list)
    for rule in rules:
        check(rule, 'id', str)
        check(rule, 'hostType', str)
        check(rule, 'hostValue', str)
        check(rule, 'port', str)
        check(rule, 'protocol', str)
        check(rule, 'status', str)
        check(rule, 'repository', dict)
        check(rule['repository'], 'id', str)
        check(rule['repository'], 'name', str)
        check(rule['repository'], 'description', str)
        check(rule, 'organization', dict)
        check(rule['organization'], 'id', str)
        check(rule['organization'], 'name', str)
        check(rule['organization'], 'description', str)
        check(rule, 'user', dict)
        check(rule['user'], 'id', str)
        check(rule['user'], 'username', str)
        check(rule['user'], 'firstname', str)
        check(rule['user'], 'lastname', str)
        check(rule, 'plugin', dict)
        check(rule['plugin'], 'id', str)
        check(rule['plugin'], 'name', str)
        check(rule['plugin'], 'description', str)
