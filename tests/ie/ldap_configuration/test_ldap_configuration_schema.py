'''
Testing the ldap configuration schemas
'''
import pytest
from tenable.ie.ldap_configuration.schema import LDAPConfigurationSchema


@pytest.fixture()
def ldap_configuration_schema():
    return {
        'enabled': True,
        'url': 'customer.tenable.ad',
        'search_user_dn': 'customer.tenable.ad',
        'search_user_password': None,
        'user_search_base': 'tenable.ad',
        'user_search_filter': '.ad',
        'allowed_groups': [{
            'name': 'groups name',
            'default_role_ids': [1, 2],
            'default_profile_id': 1
        }]
    }


def test_ldap_configuration_schema(ldap_configuration_schema):
    '''
    test ldap configuration schema
    '''
    test_resp = {
        'enabled': True,
        'url': 'customer.tenable.ad',
        'searchUserDN': 'customer.tenable.ad',
        'searchUserPassword': None,
        'userSearchBase': 'tenable.ad',
        'userSearchFilter': '.ad',
        'enable_sasl_binding': True,
        'allowedGroups': [{
            'name': 'groups name',
            'defaultRoleIds': [1, 2],
            'defaultProfileId': 1
        }]
    }
    schema = LDAPConfigurationSchema()
    req = schema.dump(schema.load(ldap_configuration_schema))
    assert test_resp['enabled'] == req['enabled']
    assert test_resp['url'] == req['url']
    assert test_resp['searchUserDN'] == req['searchUserDN']
    assert test_resp['searchUserPassword'] == req['searchUserPassword']
    assert test_resp['userSearchBase'] == req['userSearchBase']
    assert test_resp['userSearchFilter'] == req['userSearchFilter']
    assert test_resp['allowedGroups'][0]['name'] == \
           req['allowedGroups'][0]['name']
    assert test_resp['allowedGroups'][0]['defaultRoleIds'] == \
           req['allowedGroups'][0]['defaultRoleIds']
    assert test_resp['allowedGroups'][0]['defaultProfileId'] == \
           req['allowedGroups'][0]['defaultProfileId']
