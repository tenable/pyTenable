import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_roles_list(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/roles',
                  json=[{
                      'id': 1,
                      'name': 'Admin',
                      'description': 'full access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [1, 2],
                          'dynamicId': 'some id'
                      }]
                  }, {
                      'id': 2,
                      'name': 'Basic',
                      'description': 'basic access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [3, 4],
                          'dynamicId': 'some other id'
                      }]
                  }]
                  )
    resp = api.roles.list()
    assert isinstance(resp, list)
    assert len(resp) == 2
    assert resp[0]['name'] == 'Admin'
    assert resp[0]['description'] == 'full access'
    assert resp[0]['permissions'][0]['entity_name'] == 'entityName'
    assert resp[0]['permissions'][0]['action'] == 'action'
    assert resp[0]['permissions'][0]['entity_ids'] == [1, 2]
    assert resp[0]['permissions'][0]['dynamic_id'] == 'some id'
    assert resp[1]['name'] == 'Basic'
    assert resp[1]['description'] == 'basic access'
    assert resp[1]['permissions'][0]['entity_name'] == 'entityName'
    assert resp[1]['permissions'][0]['action'] == 'action'
    assert resp[1]['permissions'][0]['entity_ids'] == [3, 4]
    assert resp[1]['permissions'][0]['dynamic_id'] == 'some other id'


@responses.activate
def test_roles_create(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/roles',
                  json=[{
                      'id': 1,
                      'name': 'Admin',
                      'description': 'full access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [1, 2],
                          'dynamicId': 'some id'
                      }]
                  }]
                  )
    resp = api.roles.create(name='Admin',
                            description='full access')
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['name'] == 'Admin'
    assert resp[0]['description'] == 'full access'
    assert resp[0]['permissions'][0]['entity_name'] == 'entityName'
    assert resp[0]['permissions'][0]['action'] == 'action'
    assert resp[0]['permissions'][0]['entity_ids'] == [1, 2]
    assert resp[0]['permissions'][0]['dynamic_id'] == 'some id'


@responses.activate
def test_roles_default_role(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/roles/user-creation-defaults',
                  json=[{
                      'id': 1,
                      'name': 'Admin',
                      'description': 'full access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [1, 2],
                          'dynamicId': 'some id'
                      }]
                  }]
                  )
    resp = api.roles.default_roles()
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['name'] == 'Admin'
    assert resp[0]['description'] == 'full access'
    assert resp[0]['permissions'][0]['entity_name'] == 'entityName'
    assert resp[0]['permissions'][0]['action'] == 'action'
    assert resp[0]['permissions'][0]['entity_ids'] == [1, 2]
    assert resp[0]['permissions'][0]['dynamic_id'] == 'some id'


@responses.activate
def test_roles_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/roles/1',
                  json={
                      'id': 1,
                      'name': 'Admin',
                      'description': 'full access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [1, 2],
                          'dynamicId': 'some id'
                      }]
                  }
                  )
    resp = api.roles.details('1')
    assert isinstance(resp, dict)
    assert resp['name'] == 'Admin'
    assert resp['description'] == 'full access'
    assert resp['permissions'][0]['entity_name'] == 'entityName'
    assert resp['permissions'][0]['action'] == 'action'
    assert resp['permissions'][0]['entity_ids'] == [1, 2]
    assert resp['permissions'][0]['dynamic_id'] == 'some id'


@responses.activate
def test_roles_update(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/roles/1',
                  json={
                      'id': 1,
                      'name': 'EDITED',
                      'description': 'full access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [1, 2],
                          'dynamicId': 'some id'
                      }]
                  }
                  )
    resp = api.roles.update('1', name='EDITED')
    assert isinstance(resp, dict)
    assert resp['name'] == 'EDITED'
    assert resp['description'] == 'full access'
    assert resp['permissions'][0]['entity_name'] == 'entityName'
    assert resp['permissions'][0]['action'] == 'action'
    assert resp['permissions'][0]['entity_ids'] == [1, 2]
    assert resp['permissions'][0]['dynamic_id'] == 'some id'


@responses.activate
def test_roles_delete(api):
    responses.add(responses.DELETE,
                  f'{RE_BASE}/roles/1',
                  json=None)
    resp = api.roles.delete('1')
    assert resp is None


@responses.activate
def test_roles_copy_role(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/roles/from/1',
                  json={
                      'id': 1,
                      'name': 'EDITED',
                      'description': 'full access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [1, 2],
                          'dynamicId': 'some id'
                      }]
                  }
                  )
    resp = api.roles.copy_role(from_id='1', name='EDITED')
    assert isinstance(resp, dict)
    assert resp['name'] == 'EDITED'
    assert resp['description'] == 'full access'
    assert resp['permissions'][0]['entity_name'] == 'entityName'
    assert resp['permissions'][0]['action'] == 'action'
    assert resp['permissions'][0]['entity_ids'] == [1, 2]
    assert resp['permissions'][0]['dynamic_id'] == 'some id'


@responses.activate
def test_roles_replace_role_permissions(api):
    responses.add(responses.PUT,
                  f'{RE_BASE}/roles/1/permissions',
                  json={
                      'id': 1,
                      'name': 'Admin',
                      'description': 'full access',
                      'permissions': [{
                          'entityName': 'entityName',
                          'action': 'action',
                          'entityIds': [1, 2],
                          'dynamicId': 'some id'
                      }]
                  }
                  )
    resp = api.roles.replace_role_permissions('1',
                                              permissions=[{
                                                  'entity_name': 'entityName',
                                                  'action': 'action',
                                                  'entity_ids': [1, 2],
                                                  'dynamic_id': 'some id'
                                              }])
    assert isinstance(resp, dict)
    assert resp['name'] == 'Admin'
    assert resp['description'] == 'full access'
    assert resp['permissions'][0]['entity_name'] == 'entityName'
    assert resp['permissions'][0]['action'] == 'action'
    assert resp['permissions'][0]['entity_ids'] == [1, 2]
    assert resp['permissions'][0]['dynamic_id'] == 'some id'
