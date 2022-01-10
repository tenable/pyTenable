"""
Testing the Groups endpoints
"""
import pytest
import responses
from responses import matchers

GROUPS_BASE_URL = r"https://cloud.tenable.com/api/v3/groups"
BASE_URL = r"https://cloud.tenable.com"
GROUP_ID = "b27778c1-af10-4218-a1a4-c2c36b236e05"
USER_ID = "e9f23194-adb7-4c02-8632-615c694c787e"


@responses.activate
def test_add_user(api):
    responses.add(
        responses.POST,
        f"{GROUPS_BASE_URL}/{GROUP_ID}/users/{USER_ID}"
    )

    responses.add(
        responses.GET,
        f"{GROUPS_BASE_URL}/{GROUP_ID}/users",
        json={
            "users": [
                {
                    "id": "e9f23194-adb7-4c02-8632-615c694c787e",
                    "username": "jyoti.patel@crestdatasys.com",
                    "email": "jyoti.patel@crestdatasys.com",
                    "name": "jyoti.patel@crestdatasys.com",
                    "type": "local",
                    "permissions": 64,
                    "login_fail_count": 0,
                    "login_fail_total": 0,
                    "last_apikey_access": 1636464654829,
                    "enabled": True,
                    "lockout": 0,
                    "lastlogin": 1635924062814,
                },
                {
                    "id": "d3402235-7fa2-49e1-9a8f-15e97707c929",
                    "username": "tomeara@crestdatasys.com",
                    "email": "tomeara@crestdatasys.com",
                    "name": "tomeara@crestdatasys.com",
                    "type": "local",
                    "permissions": 64,
                    "login_fail_count": 0,
                    "login_fail_total": 0,
                    "enabled": True,
                    "lockout": 0,
                },
            ]
        },
    )

    resp = api.v3.groups.add_user(GROUP_ID, USER_ID)
    user_ids = [user['id'] for user in resp]

    assert USER_ID in user_ids


@responses.activate
def test_create(api):
    group_name = "Test Group"
    responses.add(
        responses.POST,
        f"{GROUPS_BASE_URL}",
        match=[matchers.json_params_matcher({"name": group_name})],
        json={
            "id": GROUP_ID,
            "name": group_name,
        },
    )
    resp = api.v3.groups.create(group_name)
    assert resp["name"] == group_name
    assert resp["id"] == GROUP_ID


@responses.activate
def test_delete(api):
    responses.add(responses.DELETE, f"{GROUPS_BASE_URL}/{GROUP_ID}")
    assert None is api.v3.groups.delete(GROUP_ID)


@responses.activate
def test_delete_user(api):
    responses.add(
        responses.DELETE,
        f"{GROUPS_BASE_URL}/{GROUP_ID}/users/{USER_ID}"
    )
    assert None is api.v3.groups.delete_user(GROUP_ID, USER_ID)


@responses.activate
def test_edit(api):
    updated_group_name = "Updated Test Group"

    responses.add(
        responses.PUT,
        f"{GROUPS_BASE_URL}/{GROUP_ID}",
        match=[matchers.json_params_matcher({"name": updated_group_name})],
        json={"id": GROUP_ID, "name": updated_group_name, "user_count": 0},
    )

    resp = api.v3.groups.edit(GROUP_ID, updated_group_name)
    assert resp["id"] == GROUP_ID
    assert resp["name"] == updated_group_name


@responses.activate
def test_list_users(api):

    responses.add(
        responses.GET,
        f"{GROUPS_BASE_URL}/{GROUP_ID}/users",
        json={
            "users": [
                {
                    "id": "e9f23194-adb7-4c02-8632-615c694c787e",
                    "username": "jyoti.patel@crestdatasys.com",
                    "email": "jyoti.patel@crestdatasys.com",
                    "name": "jyoti.patel@crestdatasys.com",
                    "type": "local",
                    "permissions": 64,
                    "login_fail_count": 0,
                    "login_fail_total": 0,
                    "last_apikey_access": 1636464654829,
                    "enabled": True,
                    "lockout": 0,
                    "lastlogin": 1635924062814,
                },
                {
                    "id": "d3402235-7fa2-49e1-9a8f-15e97707c929",
                    "username": "tomeara@crestdatasys.com",
                    "email": "tomeara@crestdatasys.com",
                    "name": "tomeara@crestdatasys.com",
                    "type": "local",
                    "permissions": 64,
                    "login_fail_count": 0,
                    "login_fail_total": 0,
                    "enabled": True,
                    "lockout": 0,
                },
            ]
        },
    )

    resp = api.v3.groups.list_users(GROUP_ID)
    assert resp[0]["id"] == "e9f23194-adb7-4c02-8632-615c694c787e"
    assert resp[0]["enabled"]
    assert resp[0]["name"] == "jyoti.patel@crestdatasys.com"


@pytest.mark.skip("API method NotImplemented in v3")
def test_search(api): # noqa
    """
    Test the search function
    """
    pass
