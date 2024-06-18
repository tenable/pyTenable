import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_directory_list(api):
    '''
    tests the directory list api.
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/directories',
                  json=[{
                      "id": 0,
                      "name": "test_directory",
                      "ip": "172.26.36.1",
                      "type": "directory_type",
                      "ldapPort": 0,
                      "globalCatalogPort": 0,
                      "smbPort": 0,
                      "dns": "company",
                      "infrastructureId": 0,
                      "ldapCrawlingStatus": "none",
                      "sysvolCrawlingStatus": "none",
                      "honeyAccountAdObjectId": '0',
                      "honeyAccountDistinguishedName": "honey",
                      "honeyAccountConfigurationStatus": "none"
                  }]
                  )
    resp = api.directories.list()
    assert isinstance(resp, list)
    assert resp[0]['name'] == 'test_directory'
    assert resp[0]['ldap_crawling_status'] == 'none'
    assert resp[0]['sysvol_crawling_status'] == 'none'
    assert resp[0]['honey_account_ad_object_id'] == '0'
    assert resp[0]['honey_account_distinguished_name'] == 'honey'
    assert resp[0]['honey_account_configuration_status'] == 'none'


@responses.activate
def test_directory_create(api):
    '''
    tests the directory create api.
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/directories',
                  json=[{
                      "id": 0,
                      "name": "new_directory",
                      "ip": "127.0.0.2",
                      "type": "directory_type",
                      "ldapPort": 400,
                      "globalCatalogPort": 0,
                      "smbPort": 0,
                      "dns": "company",
                      "infrastructureId": 0,
                      "ldapCrawlingStatus": "none",
                      "sysvolCrawlingStatus": "none",
                      "honeyAccountAdObjectId": '0',
                      "honeyAccountDistinguishedName": "honey",
                      "honeyAccountConfigurationStatus": "none"
                  }]
                  )
    resp = api.directories.create(
        infrastructure_id=1,
        name='ExampleServer',
        ip='172.16.0.1',
        directory_type='type',
        dns='company.tld',
        ldap_port=400
    )
    assert isinstance(resp, list)
    assert resp[0]['ldap_port'] == 400
    assert resp[0]['name'] == 'new_directory'
    assert resp[0]['ldap_crawling_status'] == 'none'
    assert resp[0]['sysvol_crawling_status'] == 'none'
    assert resp[0]['honey_account_ad_object_id'] == '0'
    assert resp[0]['honey_account_distinguished_name'] == 'honey'
    assert resp[0]['honey_account_configuration_status'] == 'none'


@responses.activate
def test_directory_update(api):
    '''
    tests the directory update api.
    '''
    responses.add(responses.PATCH,
                  f'{RE_BASE}/infrastructures/1/directories/5',
                  json=
                  {
                      "id": 5,
                      "name": "new_directory_name",
                      "ip": "172.26.36.4",
                      "type": "directory_type",
                      "ldapPort": 400,
                      "globalCatalogPort": 0,
                      "smbPort": 0,
                      "dns": "string",
                      "infrastructureId": 0,
                      "ldapCrawlingStatus": "none",
                      "sysvolCrawlingStatus": "none",
                      "honeyAccountAdObjectId": '0',
                      "honeyAccountDistinguishedName": "honey",
                      "honeyAccountConfigurationStatus": "none",
                  }

                  )
    resp = api.directories.update(
        infrastructure_id=1,
        directory_id='5',
        name='new_directory_name'
    )
    assert isinstance(resp, dict)
    assert resp['name'] == 'new_directory_name'
    assert resp['infrastructure_id'] == 0
    assert resp['id'] == 5
    assert resp['ldap_crawling_status'] == 'none'
    assert resp['sysvol_crawling_status'] == 'none'
    assert resp['honey_account_ad_object_id'] == '0'
    assert resp['honey_account_distinguished_name'] == 'honey'
    assert resp['honey_account_configuration_status'] == 'none'


@responses.activate
def test_directory_details(api):
    '''
    tests the directory details api.
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/directories/10',
                  json={
                      "id": 10,
                      "name": "test_directory",
                      "ip": "12.63.58.24",
                      "type": "directory_type",
                      "ldapPort": 400,
                      "globalCatalogPort": 0,
                      "smbPort": 0,
                      "dns": "string",
                      "infrastructureId": 0,
                      "ldapCrawlingStatus": "none",
                      "sysvolCrawlingStatus": "none",
                      "honeyAccountAdObjectId": '0',
                      "honeyAccountDistinguishedName": "honey",
                      "honeyAccountConfigurationStatus": "none",
                  }
                  )
    resp = api.directories.details(directory_id='10')
    assert isinstance(resp, dict)
    assert resp['name'] == 'test_directory'
    assert resp['id'] == 10
    assert resp['ldap_crawling_status'] == 'none'
    assert resp['sysvol_crawling_status'] == 'none'
    assert resp['honey_account_ad_object_id'] == '0'
    assert resp['honey_account_distinguished_name'] == 'honey'
    assert resp['honey_account_configuration_status'] == 'none'


@responses.activate
def test_directory_delete(api):
    '''
    tests the  directory delete instance api.
    '''
    responses.add(responses.DELETE,
                  f'{RE_BASE}/infrastructures/1/directories/5',
                  json=None
                  )
    resp = api.directories.delete(infrastructure_id=1, directory_id=5)
    assert resp is None
