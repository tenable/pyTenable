from datetime import datetime, timezone
from uuid import UUID

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.access_control.models import (
    AccessControlGroup,
    AccessControlGroupBase,
    AccessControlUser,
)


def test_group_model():
    obj = AccessControlGroup(
        permissions=16,
        name="Something",
        uuid=UUID("12345678-1234-1234-1234-123456789012"),
        container_uuid=UUID("12345678-1234-1234-1234-123456789012"),
        id=123,
    )
    assert obj == AccessControlGroup.model_validate(
        {
            "id": 123,
            "permissions": 16,
            "name": "Something",
            "uuid": "12345678-1234-1234-1234-123456789012",
            "container_uuid": "12345678-1234-1234-1234-123456789012",
        }
    )


def test_group_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups",
        method="post",
        match_json={"name": "Something"},
        json={
            "id": 123,
            "permissions": 16,
            "name": "Something",
            "uuid": "12345678-1234-1234-1234-123456789012",
            "container_uuid": "12345678-1234-1234-1234-123456789012",
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.groups.create(name="Something")
    assert resp == AccessControlGroup(
        id=123,
        uuid=UUID("12345678-1234-1234-1234-123456789012"),
        container_uuid=UUID("12345678-1234-1234-1234-123456789012"),
        name="Something",
        permissions=16,
    )


def test_group_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123",
        method="put",
        match_json={"name": "Updated"},
        json={
            "id": 123,
            "permissions": 16,
            "name": "Updated",
            "uuid": "12345678-1234-1234-1234-123456789012",
            "container_uuid": "12345678-1234-1234-1234-123456789012",
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.groups.update(group_id=123, name="Updated")
    assert resp == AccessControlGroup(
        id=123,
        uuid=UUID("12345678-1234-1234-1234-123456789012"),
        container_uuid=UUID("12345678-1234-1234-1234-123456789012"),
        name="Updated",
        permissions=16,
    )


def test_group_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://cloud.tenable.com/groups/123", method="delete")
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.access_control.groups.delete(group_id=123) is None


def test_group_get(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups",
        method="get",
        json={
            "groups": [
                {
                    "id": 123,
                    "name": "Updated",
                    "uuid": "12345678-1234-1234-1234-123456789012",
                    "container_uuid": "12345678-1234-1234-1234-123456789012",
                }
            ]
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.groups.get()
    assert resp == [
        AccessControlGroupBase(
            id=123,
            uuid=UUID("12345678-1234-1234-1234-123456789012"),
            container_uuid=UUID("12345678-1234-1234-1234-123456789012"),
            name="Updated",
        )
    ]


def test_group_get_users(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123/users",
        method="get",
        json={
            "users": [
                {
                    "uuid": "12345678-1234-1234-1234-123456789012",
                    "id": 345,
                    "type": "local",
                    "name": "John Smith",
                    "preferences": {},
                    "group_uuids": ["12345678-4321-4321-4321-123456789012"],
                    "permissions": 16,
                    "username": "someone@company.tld",
                    "email": "alias@company.tld",
                    "last_login_attempt": 1780290000000,
                    "lastlogin": 1780290000000,
                    "last_apikey_access": 1780290000000,
                    "login_fail_count": 1,
                    "login_fail_total": 10,
                    "undeletable": False,
                    "lockout": False,
                    "enabled": True,
                    "container_uuid": "87654321-4321-4321-4321-123456654321",
                }
            ]
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.groups.get_users(123)
    assert resp == [
        AccessControlUser(
            uuid=UUID("12345678-1234-1234-1234-123456789012"),
            preferences={},
            group_uuids=[UUID("12345678-4321-4321-4321-123456789012")],
            id=345,
            type="local",
            role="basic",
            name="John Smith",
            username="someone@company.tld",
            email="alias@company.tld",
            last_login_attempt=datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc),
            last_login=datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc),
            last_apikey_access=datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc),
            login_fail_count=1,
            login_fail_total=10,
            lockout=False,
            enabled=True,
            container_uuid=UUID("87654321-4321-4321-4321-123456654321"),
        )
    ]


def test_group_add_user(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123/users/345", method="post"
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.platform.access_control.groups.add_user(group_id=123, user_id=345) is None
    )


def test_group_rm_user(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123/users/345", method="delete"
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.platform.access_control.groups.remove_user(group_id=123, user_id=345)
        is None
    )


@pytest.mark.asyncio
async def test_async_group_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups",
        method="post",
        match_json={"name": "Something"},
        json={
            "id": 123,
            "permissions": 16,
            "name": "Something",
            "uuid": "12345678-1234-1234-1234-123456789012",
            "container_uuid": "87654321-4321-4321-4321-123456654321",
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.groups.create(name="Something")
    assert resp == AccessControlGroup(
        id=123,
        uuid=UUID("12345678-1234-1234-1234-123456789012"),
        container_uuid=UUID("87654321-4321-4321-4321-123456654321"),
        name="Something",
        permissions=16,
    )


@pytest.mark.asyncio
async def test_async_group_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123",
        method="put",
        match_json={"name": "Updated"},
        json={
            "id": 123,
            "permissions": 16,
            "name": "Updated",
            "uuid": "12345678-1234-1234-1234-123456789012",
            "container_uuid": "87654321-4321-4321-4321-123456654321",
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.groups.update(
        group_id=123, name="Updated"
    )
    assert resp == AccessControlGroup(
        id=123,
        uuid=UUID("12345678-1234-1234-1234-123456789012"),
        container_uuid=UUID("87654321-4321-4321-4321-123456654321"),
        name="Updated",
        permissions=16,
    )


@pytest.mark.asyncio
async def test_async_group_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url="https://cloud.tenable.com/groups/123", method="delete")
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.access_control.groups.delete(group_id=123) is None


@pytest.mark.asyncio
async def test_async_group_get(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups",
        method="get",
        json={
            "groups": [
                {
                    "id": 123,
                    "name": "Updated",
                    "uuid": "12345678-1234-1234-1234-123456789012",
                    "container_uuid": "87654321-4321-4321-4321-123456654321",
                }
            ]
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.groups.get()
    assert resp == [
        AccessControlGroupBase(
            id=123,
            uuid=UUID("12345678-1234-1234-1234-123456789012"),
            container_uuid=UUID("87654321-4321-4321-4321-123456654321"),
            name="Updated",
        )
    ]


@pytest.mark.asyncio
async def test_async_group_add_user(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123/users/345", method="post"
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.access_control.groups.add_user(group_id=123, user_id=345)
        is None
    )


@pytest.mark.asyncio
async def test_async_group_rm_user(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123/users/345", method="delete"
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.access_control.groups.remove_user(
            group_id=123, user_id=345
        )
        is None
    )


@pytest.mark.asyncio
async def test_async_group_get_users(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/groups/123/users",
        method="get",
        json={
            "users": [
                {
                    "uuid": "12345678-1234-1234-1234-123456789012",
                    "id": 345,
                    "type": "local",
                    "name": "John Smith",
                    "preferences": {},
                    "group_uuids": ["12345678-4321-4321-4321-123456789012"],
                    "permissions": 16,
                    "username": "someone@company.tld",
                    "email": "alias@company.tld",
                    "last_login_attempt": 1780290000000,
                    "lastlogin": 1780290000000,
                    "last_apikey_access": 1780290000000,
                    "login_fail_count": 1,
                    "login_fail_total": 10,
                    "undeletable": False,
                    "lockout": False,
                    "enabled": True,
                    "container_uuid": "87654321-4321-4321-4321-123456654321",
                }
            ]
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.groups.get_users(123)
    assert resp == [
        AccessControlUser(
            uuid=UUID("12345678-1234-1234-1234-123456789012"),
            preferences={},
            group_uuids=[UUID("12345678-4321-4321-4321-123456789012")],
            id=345,
            type="local",
            role="basic",
            name="John Smith",
            username="someone@company.tld",
            email="alias@company.tld",
            last_login_attempt=datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc),
            last_login=datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc),
            last_apikey_access=datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc),
            login_fail_count=1,
            login_fail_total=10,
            lockout=False,
            enabled=True,
            container_uuid=UUID("87654321-4321-4321-4321-123456654321"),
        )
    ]
