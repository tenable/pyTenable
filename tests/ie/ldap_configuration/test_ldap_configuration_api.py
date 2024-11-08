import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_ldap_configuration_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/ldap-configuration',
                  json={
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
                  )
    resp = api.ldap_configuration.details()
    assert isinstance(resp, dict)
    assert resp['enabled'] is True
    assert resp['url'] == 'customer.tenable.ad'
    assert resp['search_user_dn'] == 'customer.tenable.ad'
    assert resp['search_user_password'] is None
    assert resp['user_search_base'] == 'tenable.ad'
    assert resp['user_search_filter'] == '.ad'
    assert resp['allowed_groups'][0]['name'] == 'groups name'
    assert resp['allowed_groups'][0]['default_role_ids'] == [1, 2]
    assert resp['allowed_groups'][0]['default_profile_id'] == 1
    assert resp['enable_sasl_binding'] is True


@responses.activate
def test_ldap_configuration_update(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/ldap-configuration',
                  json={
                      'enabled': True,
                      'url': 'customer.tenable.ad',
                      'searchUserDN': 'customer.tenable.ad',
                      'searchUserPassword': None,
                      'userSearchBase': 'tenable.ad',
                      'userSearchFilter': '.ad',
                      'allowedGroups': [{
                          'name': 'EDITED',
                          'defaultRoleIds': [1, 2],
                          'defaultProfileId': 1
                      }]
                  }
                  )
    resp = api.ldap_configuration.update(enabled=True,
                                          url='customer.tenable.ad',
                                          search_user_dn='customer.tenable.ad',
                                          search_user_password=None,
                                          user_search_base='tenable.ad',
                                          user_search_filter='.ad',
                                          allowed_groups=[{
                                              'name': 'EDITED',
                                              'default_role_ids': [1, 2],
                                              'default_profile_id': 1
                                          }]
                                         )
    assert isinstance(resp, dict)
    assert resp['enabled'] is True
    assert resp['url'] == 'customer.tenable.ad'
    assert resp['search_user_dn'] == 'customer.tenable.ad'
    assert resp['search_user_password'] is None
    assert resp['user_search_base'] == 'tenable.ad'
    assert resp['user_search_filter'] == '.ad'
    assert resp['allowed_groups'][0]['name'] == 'EDITED'
    assert resp['allowed_groups'][0]['default_role_ids'] == [1, 2]
    assert resp['allowed_groups'][0]['default_profile_id'] == 1
