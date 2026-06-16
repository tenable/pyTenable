from datetime import datetime, timezone
from uuid import UUID

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.access_control.models import (
    AccessControlPermission,
    AccessControlPermObj,
    AccessControlSubject,
    UserGroupPermissions,
)

DT_OBJ = datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc)
DT_TS = 1780290000000
UUID_UUID = UUID("12345678-1234-1234-1234-123456789012")
UUID_STR = "12345678-1234-1234-1234-123456789012"


def test_permission_model():
    model = AccessControlPermission(
        name="Something",
        actions=["CanView"],
        subjects=[
            AccessControlSubject(
                name="subj",
                type="User",
                uuid=UUID("87654321-4321-4321-4321-123456654321"),
            )
        ],
        objects=[
            AccessControlPermObj(
                name="perm",
                type="AllAssets",
                uuid=UUID("12345678-4321-4321-4321-123456789012"),
            )
        ],
        uuid=UUID_UUID,
        created_at=DT_OBJ,
        created_by="user",
        updated_at=DT_OBJ,
        updated_by="me",
    )
    assert model == AccessControlPermission.model_validate(
        {
            "permission_uuid": UUID_STR,
            "name": "Something",
            "created_at": DT_TS,
            "created_by": "user",
            "updated_at": DT_TS,
            "updated_by": "me",
            "actions": ["CanView"],
            "subjects": [
                {
                    "name": "subj",
                    "type": "User",
                    "uuid": "87654321-4321-4321-4321-123456654321",
                }
            ],
            "objects": [
                {
                    "name": "perm",
                    "type": "AllAssets",
                    "uuid": "12345678-4321-4321-4321-123456789012",
                }
            ],
        }
    )


def test_permission_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions",
        method="post",
        match_json={
            "name": "example",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.create(
        name="example",
        actions=["CanView", "CanScan"],
        objects=[{"type": "AllAssets"}],
        subjects=[{"type": "User", "name": "John Smith", "uuid": UUID_STR}],
    )
    assert resp == AccessControlPermission(
        name="example",
        uuid=UUID_UUID,
        created_at=DT_OBJ,
        created_by="user@company.tld",
        actions=["CanView", "CanScan"],
        objects=[AccessControlPermObj(type="AllAssets")],
        subjects=[AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)],
    )


def test_permission_get(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions",
        method="get",
        json={
            "permissions": [
                {
                    "name": "example",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "user@company.tld",
                    "actions": ["CanView", "CanScan"],
                    "objects": [{"type": "AllAssets"}],
                    "subjects": [
                        {"name": "John Smith", "type": "User", "uuid": UUID_STR}
                    ],
                }
            ]
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.get()
    assert resp == [
        AccessControlPermission(
            name="example",
            uuid=UUID_UUID,
            created_at=DT_OBJ,
            created_by="user@company.tld",
            actions=["CanView", "CanScan"],
            objects=[AccessControlPermObj(type="AllAssets")],
            subjects=[
                AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)
            ],
        )
    ]


def test_permissions_details(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.details(
        UUID("12345678-1234-1234-1234-123456789012")
    )
    assert resp == AccessControlPermission(
        name="example",
        uuid=UUID_UUID,
        created_at=DT_OBJ,
        created_by="user@company.tld",
        actions=["CanView", "CanScan"],
        objects=[AccessControlPermObj(type="AllAssets")],
        subjects=[AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)],
    )


def test_permissions_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="put",
        match_json={
            "name": "Updated",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.update(
        permission_uuid=UUID_UUID, name="Updated"
    )
    assert resp == AccessControlPermission(
        name="example",
        uuid=UUID_UUID,
        created_at=DT_OBJ,
        created_by="user@company.tld",
        actions=["CanView", "CanScan"],
        objects=[AccessControlPermObj(type="AllAssets")],
        subjects=[AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)],
    )


def test_permissions_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="delete",
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.delete(UUID_UUID)
    assert resp is None


def test_get_self_permissions(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/users/me",
        method="get",
        json={
            "permissions_granted": [
                {
                    "name": "example granted",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanUse"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
            "permissions_available": [
                {
                    "name": "example avail",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanScan"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.get_self_permissions()
    assert resp == UserGroupPermissions(
        granted=[
            AccessControlPermission(
                name="example granted",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanUse"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
        available=[
            AccessControlPermission(
                name="example avail",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanScan"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
    )


def test_get_user_permissions(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/users/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "permissions_granted": [
                {
                    "name": "example granted",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanUse"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
            "permissions_available": [
                {
                    "name": "example avail",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanScan"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.get_user_permissions(UUID_UUID)
    assert resp == UserGroupPermissions(
        granted=[
            AccessControlPermission(
                name="example granted",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanUse"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
        available=[
            AccessControlPermission(
                name="example avail",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanScan"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
    )


def test_get_group_permissions(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/user-groups/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "permissions_granted": [
                {
                    "name": "example granted",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanUse"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
            "permissions_available": [
                {
                    "name": "example avail",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanScan"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.permissions.get_group_permissions(UUID_UUID)
    assert resp == UserGroupPermissions(
        granted=[
            AccessControlPermission(
                name="example granted",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanUse"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
        available=[
            AccessControlPermission(
                name="example avail",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanScan"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
    )


@pytest.mark.asyncio
async def test_async_permission_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions",
        method="post",
        match_json={
            "name": "example",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.create(
        name="example",
        actions=["CanView", "CanScan"],
        objects=[{"type": "AllAssets"}],
        subjects=[{"type": "User", "name": "John Smith", "uuid": UUID_STR}],
    )
    assert resp == AccessControlPermission(
        name="example",
        uuid=UUID_UUID,
        created_at=DT_OBJ,
        created_by="user@company.tld",
        actions=["CanView", "CanScan"],
        objects=[AccessControlPermObj(type="AllAssets")],
        subjects=[AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)],
    )


@pytest.mark.asyncio
async def test_async_permission_get(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions",
        method="get",
        json={
            "permissions": [
                {
                    "name": "example",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "user@company.tld",
                    "actions": ["CanView", "CanScan"],
                    "objects": [{"type": "AllAssets"}],
                    "subjects": [
                        {"name": "John Smith", "type": "User", "uuid": UUID_STR}
                    ],
                }
            ]
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.get()
    assert resp == [
        AccessControlPermission(
            name="example",
            uuid=UUID_UUID,
            created_at=DT_OBJ,
            created_by="user@company.tld",
            actions=["CanView", "CanScan"],
            objects=[AccessControlPermObj(type="AllAssets")],
            subjects=[
                AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)
            ],
        )
    ]


@pytest.mark.asyncio
async def test_async_permissions_details(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.details(
        UUID("12345678-1234-1234-1234-123456789012")
    )
    assert resp == AccessControlPermission(
        name="example",
        uuid=UUID_UUID,
        created_at=DT_OBJ,
        created_by="user@company.tld",
        actions=["CanView", "CanScan"],
        objects=[AccessControlPermObj(type="AllAssets")],
        subjects=[AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)],
    )


@pytest.mark.asyncio
async def test_async_permissions_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="put",
        match_json={
            "name": "Updated",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
        json={
            "name": "example",
            "permission_uuid": UUID_STR,
            "created_at": DT_TS,
            "created_by": "user@company.tld",
            "actions": ["CanView", "CanScan"],
            "objects": [{"type": "AllAssets"}],
            "subjects": [{"name": "John Smith", "type": "User", "uuid": UUID_STR}],
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.update(
        permission_uuid=UUID_UUID, name="Updated"
    )
    assert resp == AccessControlPermission(
        name="example",
        uuid=UUID_UUID,
        created_at=DT_OBJ,
        created_by="user@company.tld",
        actions=["CanView", "CanScan"],
        objects=[AccessControlPermObj(type="AllAssets")],
        subjects=[AccessControlSubject(name="John Smith", type="User", uuid=UUID_UUID)],
    )


@pytest.mark.asyncio
async def test_async_permissions_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/12345678-1234-1234-1234-123456789012",
        method="delete",
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.delete(UUID_UUID)
    assert resp is None


@pytest.mark.asyncio
async def test_async_get_self_permissions(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/users/me",
        method="get",
        json={
            "permissions_granted": [
                {
                    "name": "example granted",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanUse"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
            "permissions_available": [
                {
                    "name": "example avail",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanScan"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.get_self_permissions()
    assert resp == UserGroupPermissions(
        granted=[
            AccessControlPermission(
                name="example granted",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanUse"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
        available=[
            AccessControlPermission(
                name="example avail",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanScan"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
    )


@pytest.mark.asyncio
async def test_async_get_user_permissions(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/users/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "permissions_granted": [
                {
                    "name": "example granted",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanUse"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
            "permissions_available": [
                {
                    "name": "example avail",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanScan"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.get_user_permissions(
        UUID_UUID
    )
    assert resp == UserGroupPermissions(
        granted=[
            AccessControlPermission(
                name="example granted",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanUse"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
        available=[
            AccessControlPermission(
                name="example avail",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanScan"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
    )


@pytest.mark.asyncio
async def test_async_get_group_permissions(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/api/v3/access-control/permissions/user-groups/12345678-1234-1234-1234-123456789012",
        method="get",
        json={
            "permissions_granted": [
                {
                    "name": "example granted",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanUse"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
            "permissions_available": [
                {
                    "name": "example avail",
                    "permission_uuid": UUID_STR,
                    "created_at": DT_TS,
                    "created_by": "example@company.tld",
                    "actions": ["CanScan"],
                    "objects": [{"name": "example", "type": "Tag", "uuid": UUID_STR}],
                    "subjects": [{"name": "example", "type": "User", "uuid": UUID_STR}],
                }
            ],
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.permissions.get_group_permissions(
        UUID_UUID
    )
    assert resp == UserGroupPermissions(
        granted=[
            AccessControlPermission(
                name="example granted",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanUse"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
        available=[
            AccessControlPermission(
                name="example avail",
                uuid=UUID_UUID,
                created_at=DT_OBJ,
                created_by="example@company.tld",
                actions=["CanScan"],
                objects=[
                    AccessControlPermObj(name="example", type="Tag", uuid=UUID_UUID)
                ],
                subjects=[
                    AccessControlSubject(name="example", type="User", uuid=UUID_UUID)
                ],
            )
        ],
    )
