from tenable.errors import *
from ..checker import check
import pytest, os

def test_organizations_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(name=1)

def test_organizations_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(description=1)

def test_organizations_constructor_address_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(address=1)

def test_organizations_constructor_city_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(city=1)

def test_organizations_constructor_state_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(state=1)

def test_organizations_constructor_country_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(country=1)

def test_organizations_constructor_phone_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(phone=1)

def test_organizations_constructor_lce_ids_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(lce_ids=1)

def test_organizations_constructor_lce_ids_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(lce_ids=['one',])

def test_organizations_constructor_zone_selection_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(zone_selection=1)

def test_organizations_constructor_zone_selection_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.organizations._constructor(zone_selection='something')

def test_organizations_constructor_restricted_ips_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(restricted_ips=1)

def test_organizations_constructor_restricted_ips_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(restricted_ips=[1])

def test_organizations_constructor_repos_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(repos=1)

def test_organizations_constructor_repos_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(repos=['one'])

def test_organizations_constructor_pub_sites_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(pub_sites=1)

def test_organizations_constructor_pub_sites_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(pub_sites=['one'])

def test_organizations_constructor_ldap_ids_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(ldap_ids=1)

def test_organizations_constructor_ldap_ids_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(ldap_ids=['one'])

def test_organizations_constructor_nessus_managers_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(nessus_managers=1)

def test_organizations_constructor_nessus_managers_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(nessus_managers=['one'])

def test_organizations_constructor_info_links_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(info_links=1)

def test_organizations_constructor_info_links_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(info_links=[1])

def test_organizations_constructor_info_links_item_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(info_links=[(1, 'http://site.com/%IP%')])

def test_organizations_constructor_info_links_item_link_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(info_links=[('name', 1)])

def test_organizations_constructor_vuln_score_low_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(vuln_score_low='one')

def test_organizations_constructor_vuln_score_medium_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(vuln_score_medium='one')

def test_organizations_constructor_vuln_score_high_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(vuln_score_high='one')

def test_organizations_constructor_vuln_score_critical_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations._constructor(vuln_score_critical='one')

def test_organizations_constructor_success(sc):
    o = sc.organizations._constructor(
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
    assert o == {
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
        'vulnScoreCritical': 40
    }

@pytest.fixture
def org(request, admin, vcr):
    with vcr.use_cassette('test_organizations_create_success'):
        o = admin.organizations.create('New Org')
    def teardown():
        try:
            with vcr.use_cassette('test_organizations_delete_success'):
                admin.organizations.delete(int(o['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return o

@pytest.mark.vcr()
def test_organizations_create_success(admin, org):
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
    for i in org['lces']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(org, 'repositories', list)
    for i in org['repositories']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
        check(i, 'type', str)
        check(i, 'dataFormat', str)
        check(i, 'groupAssign', str)
    check(org, 'zones', list)
    for i in org['zones']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(org, 'ldaps', list)
    for i in org['ldaps']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(org, 'nessusManagers', list)
    for i in org['nessusManagers']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(org, 'pubSites', list)
    for i in org['pubSites']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)

@pytest.mark.vcr()
def test_organizations_delete_success(admin, org):
    admin.organizations.delete(int(org['id']))

@pytest.mark.vcr()
def test_organizations_details_success(admin, org):
    o = admin.organizations.details(int(org['id']))
    assert isinstance(o, dict)
    check(o, 'id', str)
    check(o, 'name', str)
    check(o, 'description', str)
    check(o, 'email', str)
    check(o, 'address', str)
    check(o, 'city', str)
    check(o, 'state', str)
    check(o, 'country', str)
    check(o, 'phone', str)
    check(o, 'fax', str)
    check(o, 'ipInfoLinks', list)
    for i in o['ipInfoLinks']:
        check(i, 'name', str)
        check(i, 'link', str)
    check(o, 'zoneSelection', str)
    check(o, 'restrictedIPs', str)
    check(o, 'vulnScoreLow', str)
    check(o, 'vulnScoreMedium', str)
    check(o, 'vulnScoreHigh', str)
    check(o, 'vulnScoreCritical', str)
    check(o, 'createdTime', str)
    check(o, 'modifiedTime', str)
    check(o, 'userCount', str)
    check(o, 'lces', list)
    for i in o['lces']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'repositories', list)
    for i in o['repositories']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
        check(i, 'type', str)
        check(i, 'dataFormat', str)
        check(i, 'groupAssign', str)
    check(o, 'zones', list)
    for i in o['zones']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'ldaps', list)
    for i in o['ldaps']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'nessusManagers', list)
    for i in o['nessusManagers']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'pubSites', list)
    for i in o['pubSites']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)

@pytest.mark.vcr()
def test_organizations_edit_success(admin, org):
    o = admin.organizations.edit(int(org['id']), name='new org name')
    assert isinstance(o, dict)
    check(o, 'id', str)
    check(o, 'name', str)
    check(o, 'description', str)
    check(o, 'email', str)
    check(o, 'address', str)
    check(o, 'city', str)
    check(o, 'state', str)
    check(o, 'country', str)
    check(o, 'phone', str)
    check(o, 'fax', str)
    check(o, 'ipInfoLinks', list)
    for i in o['ipInfoLinks']:
        check(i, 'name', str)
        check(i, 'link', str)
    check(o, 'zoneSelection', str)
    check(o, 'restrictedIPs', str)
    check(o, 'vulnScoreLow', str)
    check(o, 'vulnScoreMedium', str)
    check(o, 'vulnScoreHigh', str)
    check(o, 'vulnScoreCritical', str)
    check(o, 'createdTime', str)
    check(o, 'modifiedTime', str)
    check(o, 'userCount', str)
    check(o, 'lces', list)
    for i in o['lces']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'repositories', list)
    for i in o['repositories']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
        check(i, 'type', str)
        check(i, 'dataFormat', str)
        check(i, 'groupAssign', str)
    check(o, 'zones', list)
    for i in o['zones']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'ldaps', list)
    for i in o['ldaps']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'nessusManagers', list)
    for i in o['nessusManagers']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
    check(o, 'pubSites', list)
    for i in o['pubSites']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)

@pytest.mark.vcr()
def test_organizations_accept_risk_rules_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.accept_risk_rules('one')

@pytest.mark.vcr()
def test_organizations_accept_risk_rules_repos_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.accept_risk_rules(1, repos=1)

@pytest.mark.vcr()
def test_organizations_accept_risk_rules_repos_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.accept_risk_rules(1, repos=['one'])

@pytest.mark.vcr()
def test_organizations_accept_risk_rules_plugin_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.accept_risk_rules(1, plugin='one')

@pytest.mark.vcr()
def test_organizations_accept_risk_rules_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.accept_risk_rules(1, port='one')

@pytest.mark.vcr()
def test_organizations_accept_risk_rules_success(admin, org):
    rules = admin.organizations.accept_risk_rules(int(org['id']))
    assert isinstance(rules, list)
    for r in rules:
        check(r, 'id', str)
        check(r, 'hostType', str)
        check(r, 'hostValue', str)
        check(r, 'port', str)
        check(r, 'protocol', str)
        check(r, 'expires', str)
        check(r, 'status', str)
        check(r, 'repository', dict)
        check(r['repository'], 'id', str)
        check(r['repository'], 'name', str)
        check(r['repository'], 'description', str)
        check(r, 'organization', dict)
        check(r['organization'], 'id', str)
        check(r['organization'], 'name', str)
        check(r['organization'], 'description', str)
        check(r, 'user', dict)
        check(r['user'], 'id', str)
        check(r['user'], 'username', str)
        check(r['user'], 'firstname', str)
        check(r['user'], 'lastname', str)
        check(r, 'plugin', dict)
        check(r['plugin'], 'id', str)
        check(r['plugin'], 'name', str)
        check(r['plugin'], 'description', str)

@pytest.mark.vcr()
def test_organizations_recast_risk_rules_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.recast_risk_rules('one')

@pytest.mark.vcr()
def test_organizations_recast_risk_rules_repos_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.recast_risk_rules(1, repos=1)

@pytest.mark.vcr()
def test_organizations_recast_risk_rules_repos_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.recast_risk_rules(1, repos=['one'])

@pytest.mark.vcr()
def test_organizations_recast_risk_rules_plugin_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.recast_risk_rules(1, plugin='one')

@pytest.mark.vcr()
def test_organizations_recast_risk_rules_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.organizations.recast_risk_rules(1, port='one')

@pytest.mark.vcr()
def test_organizations_recast_risk_rules_success(admin, org):
    rules = admin.organizations.recast_risk_rules(int(org['id']))
    assert isinstance(rules, list)
    for r in rules:
        check(r, 'id', str)
        check(r, 'hostType', str)
        check(r, 'hostValue', str)
        check(r, 'port', str)
        check(r, 'protocol', str)
        check(r, 'status', str)
        check(r, 'repository', dict)
        check(r['repository'], 'id', str)
        check(r['repository'], 'name', str)
        check(r['repository'], 'description', str)
        check(r, 'organization', dict)
        check(r['organization'], 'id', str)
        check(r['organization'], 'name', str)
        check(r['organization'], 'description', str)
        check(r, 'user', dict)
        check(r['user'], 'id', str)
        check(r['user'], 'username', str)
        check(r['user'], 'firstname', str)
        check(r['user'], 'lastname', str)
        check(r, 'plugin', dict)
        check(r['plugin'], 'id', str)
        check(r['plugin'], 'name', str)
        check(r['plugin'], 'description', str)