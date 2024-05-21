import pytest
import responses

USER = {
    'id': 1,
    'username': 'example',
    'name': 'Example User',
    'email': 'example@company.com',
    'permissions': 64,
    'lastlogin': 123456789,
    'type': 'local',
    'login_fail_count': 0,
    'login_fail_total': 1,
    'last_login_attempt': 123456789
}


@responses.activate
def test_user_create(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/users',
                  json=USER
                  )
    resp = nessus.users.create(username='example',
                               password='s3cr3tsqu1rr3l',
                               permissions=64,
                               name='Example User',
                               email='example@company.com'
                               )
    assert resp == USER


@responses.activate
def test_users_delete(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/users/1',
                  )
    nessus.users.delete(1)


@responses.activate
def test_users_delete_many(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/users'
                  )
    nessus.users.delete_many([1, 2, 3])


@responses.activate
def test_users_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/users/1',
                  json=USER
                  )
    resp = nessus.users.details(1)
    assert resp == USER


@responses.activate
def test_users_edit(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/users/1',
                  json=USER
                  )
    resp = nessus.users.edit(1, permissions=64, name='Updated User')
    assert resp == USER


@responses.activate
def test_users_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/users',
                  json={'users': [USER for _ in range(20)]}
                  )
    resp = nessus.users.list()
    assert isinstance(resp, list)
    for item in resp:
        assert item == USER


@responses.activate
def test_users_chpasswd(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/users/1/chpasswd'
                  )
    nessus.users.chpasswd(1, 'n3wp@ssw0rd')


@responses.activate
def test_users_api_keys(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/users/1/keys',
                  json={
                      'accessKey': '1234567890abcdef1234567890',
                      'secretKey': '1234567890abcdef1234567890'
                  })
    resp = nessus.users.api_keys(1)
    assert resp['accessKey'] == '1234567890abcdef1234567890'
    assert resp['secretKey'] == '1234567890abcdef1234567890'