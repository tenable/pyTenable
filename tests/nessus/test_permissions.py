import pytest
import responses


PERMISSION = {
    'owner': 1,
    'type': 'default',
    'permissions': 64,
    'id': 1,
    'name': 'username'
}


@responses.activate
def test_permissions_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/permissions/scanner/1',
                  json=[PERMISSION for _ in range(3)]
                  )
    resp = nessus.permissions.details('scanner', 1)
    assert isinstance(resp, list)
    for item in resp:
        assert item == PERMISSION


@responses.activate
def test_permissions_edit(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/permissions/scanner/1'
                  )
    nessus.permissions.edit('scanner', 1, acls=[
        PERMISSION, PERMISSION, PERMISSION])