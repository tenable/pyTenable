import pytest
import responses


GROUP = {
    'id': 1,
    'name': 'Example Group',
    'permissions': 16,
    'user_count': 10
}


@responses.activate
def test_groups_add_user(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/groups/1/users/1'
                  )
    nessus.groups.add_user(1, 1)


@responses.activate
def test_groups_create(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/groups',
                  json=GROUP
                  )
    resp = nessus.groups.create('Example Group')
    assert resp == GROUP


@responses.activate
def test_groups_delete(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/groups/1'
                  )
    nessus.groups.delete(1)


@responses.activate
def test_groups_delete_many(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/groups'
                  )
    nessus.groups.delete_many([1, 2, 3])


@responses.activate
def test_groups_delete_user(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/groups/1/users/1'
                  )
    nessus.groups.remove_user(1, 1)


@responses.activate
def test_groups_edit(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/groups/1',
                  json=GROUP
                  )
    resp = nessus.groups.edit(1, name='New Name')
    assert resp == GROUP


@responses.activate
def test_groups_list(nessus):
    responses.add(responses.GET,   
                  'https://localhost:8834/groups',
                  json={'groups': [GROUP for _ in range(10)]}
                  )
    resp = nessus.groups.list()
    assert isinstance(resp, list)
    for item in resp:
        assert item == GROUP


@responses.activate
def test_groups_list_users(nessus):
    user_mock={
        'id': 1,
        'username': 'example',
        'name': 'Example User',
        'email': 'example@company.com',
        'permission': 64,
        'lastlogin': 1234567890,
        'type': 'local',
        'login_fail_count': 0,
        'login_fail_total': 0,
        'last_login_attempt': 1234567890
    }
    responses.add(responses.GET,
                  'https://localhost:8834/groups/1/users',
                  json={'users': [user_mock for _ in range(10)]}
                  )
    resp = nessus.groups.list_users(1)
    assert isinstance(resp, list)
    for item in resp:
        assert item == user_mock