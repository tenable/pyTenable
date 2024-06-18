import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_profiles_list(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles',
                  json=[{
                      'id': 1,
                      'name': 'profile name',
                      'deleted': False,
                      'directories': [1, 2],
                      'dirty': True,
                      'hasEverBeenCommitted': True
                  }]
                  )
    resp = api.profiles.list()
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['name'] == 'profile name'
    assert resp[0]['deleted'] is False
    assert resp[0]['directories'] == [1, 2]
    assert resp[0]['dirty'] is True
    assert resp[0]['has_ever_been_committed'] is True


@responses.activate
def test_profiles_create(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles',
                  json=[{
                      'id': 1,
                      'name': 'profile name',
                      'deleted': False,
                      'directories': [1, 2],
                      'dirty': True,
                      'hasEverBeenCommitted': True
                  }]
                  )
    resp = api.profiles.create(name='profile name',
                               directories=[1, 2])
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['name'] == 'profile name'
    assert resp[0]['deleted'] is False
    assert resp[0]['directories'] == [1, 2]
    assert resp[0]['dirty'] is True
    assert resp[0]['has_ever_been_committed'] is True


@responses.activate
def test_profiles_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1',
                  json={
                      'id': 1,
                      'name': 'profile name',
                      'deleted': False,
                      'directories': [1, 2],
                      'dirty': True,
                      'hasEverBeenCommitted': True
                  }
                  )
    resp = api.profiles.details(profile_id='1')
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['name'] == 'profile name'
    assert resp['deleted'] is False
    assert resp['directories'] == [1, 2]
    assert resp['dirty'] is True
    assert resp['has_ever_been_committed'] is True


@responses.activate
def test_profiles_update(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/profiles/1',
                  json={
                      'id': 1,
                      'name': 'profile name',
                      'deleted': False,
                      'directories': [1, 2],
                      'dirty': True,
                      'hasEverBeenCommitted': True
                  }
                  )
    resp = api.profiles.update(profile_id='1',
                               name='profile name',
                               deleted=True,
                               directories=[1, 2])
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['name'] == 'profile name'
    assert resp['deleted'] is False
    assert resp['directories'] == [1, 2]
    assert resp['dirty'] is True
    assert resp['has_ever_been_committed'] is True


@responses.activate
def test_profiles_delete(api):
    responses.add(responses.DELETE,
                  f'{RE_BASE}/profiles/1',
                  json=None
                  )
    resp = api.profiles.delete(profile_id='1')
    assert resp is None


@responses.activate
def test_profiles_copy_profile(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/from/1',
                  json={
                      'id': 1,
                      'name': 'copied profile',
                      'deleted': False,
                      'directories': [1, 2],
                      'dirty': True,
                      'hasEverBeenCommitted': True
                  }
                  )
    resp = api.profiles.copy_profile(from_id='1',
                                     name='copied profile',
                                     directories=[1, 2])
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['name'] == 'copied profile'
    assert resp['deleted'] is False
    assert resp['directories'] == [1, 2]
    assert resp['dirty'] is True
    assert resp['has_ever_been_committed'] is True


@responses.activate
def test_profiles_commit(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/commit',
                  json=None
                  )
    resp = api.profiles.commit(profile_id='1')
    assert resp is None


@responses.activate
def test_profiles_unstage(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/unstage',
                  json=None
                  )
    resp = api.profiles.unstage(profile_id='1')
    assert resp is None
