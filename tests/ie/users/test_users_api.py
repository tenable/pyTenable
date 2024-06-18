import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_users_list(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/users',
                  json=[{
                      'id': 1,
                      'surname': 'surname',
                      'name': 'name',
                      'email': 'test@domain.com',
                      'lockedOut': True,
                      'department': 'AD',
                      'biography': 'some biography',
                      'active': True,
                      'picture': [1, 2],
                      'roles': [1, 2],
                      'identifier': 'some identifier',
                      'provider': 'tenable',
                      'eulaVersion': 1
                  }]
                  )
    resp = api.users.list()
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['name'] == 'name'
    assert resp[0]['surname'] == 'surname'


@responses.activate
def test_users_create(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/users',
                  json=[{
                      'id': 1,
                      'surname': 'surname',
                      'name': 'name',
                      'email': 'test@domain.com',
                      'lockedOut': True,
                      'department': 'AD',
                      'biography': 'some biography',
                      'active': True,
                      'picture': [1, 2],
                      'roles': [1, 2],
                      'identifier': 'some identifier',
                      'provider': 'tenable',
                      'eulaVersion': 1
                  }]
                  )
    resp = api.users.create(name='name',
                            email='test@domain.com',
                            password='password',
                            active=True)
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['name'] == 'name'
    assert resp[0]['active'] is True


@responses.activate
def test_users_info(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/users/whoami',
                  json={
                      'id': 1,
                      'surname': 'surname',
                      'name': 'name',
                      'email': 'test@domain.com',
                      'lockedOut': True,
                      'department': 'AD',
                      'roles': [{
                          'id': 1,
                          'name': 'Admin',
                          'description': 'full access',
                          'permissions': [{
                              'entityName': 'entityName',
                              'action': 'action',
                              'entityIds': [1, 2],
                              'dynamicId': 'some id'
                          }]
                      }],
                      'biography': 'some biography',
                      'active': True,
                      'picture': [1, 2],
                      'identifier': 'some identifier',
                      'provider': 'tenable',
                      'eulaVersion': 1
                  }
                  )
    resp = api.users.info()
    assert isinstance(resp, dict)
    assert resp['name'] == 'name'
    assert resp['active'] is True
    assert resp['roles'][0]['id'] == 1
    assert resp['roles'][0]['name'] == 'Admin'
    assert resp['roles'][0]['description'] == 'full access'
    assert resp['roles'][0]['permissions'][0]['entity_name'] == 'entityName'
    assert resp['roles'][0]['permissions'][0]['action'] == 'action'
    assert resp['roles'][0]['permissions'][0]['entity_ids'] == [1, 2]
    assert resp['roles'][0]['permissions'][0]['dynamic_id'] == 'some id'


@responses.activate
def test_users_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/users/1',
                  json={
                      'id': 1,
                      'surname': 'surname',
                      'name': 'name',
                      'email': 'test@domain.com',
                      'lockedOut': True,
                      'department': 'AD',
                      'biography': 'some biography',
                      'active': True,
                      'picture': [1, 2],
                      'roles': [1, 2],
                      'identifier': 'some identifier',
                      'provider': 'tenable',
                      'eulaVersion': 1
                  }
                  )
    resp = api.users.details('1')
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['name'] == 'name'
    assert resp['surname'] == 'surname'


@responses.activate
def test_users_update(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/users/1',
                  json={
                      'id': 1,
                      'surname': 'surname',
                      'name': 'name',
                      'email': 'test@domain.com',
                      'lockedOut': True,
                      'department': 'AD',
                      'biography': 'some biography',
                      'active': False,
                      'picture': [1, 2],
                      'roles': [1, 2],
                      'identifier': 'some identifier',
                      'provider': 'tenable',
                      'eulaVersion': 1
                  }
                  )
    resp = api.users.update('1',
                            name='name',
                            email='test@domain.com',
                            password='password',
                            surname='surname',
                            department='AD',
                            biography='some biography',
                            active=False,
                            picture=[1, 2])
    assert isinstance(resp, dict)
    assert resp['name'] == 'name'
    assert resp['active'] is False


@responses.activate
def test_users_delete(api):
    responses.add(responses.DELETE,
                  f'{RE_BASE}/users/1',
                  json=None
                  )
    resp = api.users.delete(1)
    assert resp is None


@responses.activate
def test_users_create_password(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/users/forgotten-password',
                  json=None)
    resp = api.users.create_password('test@domain.com')
    assert resp is None


@responses.activate
def test_users_retrieve_password(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/users/retrieve-password',
                  json=None)
    resp = api.users.retrieve_password(token='token',
                                       new_password='new password')
    assert resp is None


@responses.activate
def test_users_change_password(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/users/password',
                  json=None)
    resp = api.users.change_password(old_password='old password',
                                     new_password='new password')
    assert resp is None


@responses.activate
def test_users_update_user_role(api):
    responses.add(responses.PUT,
                  f'{RE_BASE}/users/1/roles',
                  json={
                      'roles': [1, 2]
                  })
    resp = api.users.update_user_roles('1', roles=[1, 2])
    assert isinstance(resp, dict)
    assert resp['roles'] == [1, 2]
