from copy import copy
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.access_control.models import (
    AccessControlApiKeys,
    AccessControlUser,
    AccessControlUserAuthorizations,
)

DT_OBJ = datetime(2026, 6, 1, hour=5, tzinfo=timezone.utc)
DT_TS = 1780290000000
UUID_UUID = UUID("12345678-1234-1234-1234-123456789012")
UUID_STR = "12345678-1234-1234-1234-123456789012"


@pytest.fixture
def user_json() -> dict[str, Any]:
    return {
        "uuid": UUID_STR,
        "id": 123,
        "type": "local",
        "name": "John Smith",
        "email": "something@company.com",
        "username": "user@company.com",
        "enabled": True,
        "permissions": 32,
        "last_login_attempt": DT_TS,
        "last_apikey_access": DT_TS,
        "lastlogin": DT_TS,
        "login_fail_count": 1,
        "login_fail_total": 10,
        "lockout": False,
        "group_uuids": [UUID_STR],
        "preferences": {"something": "funny"},
        "container_uuid": UUID_STR,
    }


@pytest.fixture
def user_obj(user_json) -> AccessControlUser:
    return AccessControlUser.model_validate(user_json)


def test_users_create(httpx_mock: HTTPXMock, user_json, user_obj):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/users",
        method="post",
        match_json={
            "username": "user@company.com",
            "password": "password123",
            "permissions": 32,
            "name": "John Smith",
            "email": "something@company.com",
        },
        json=user_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == cloud.platform.access_control.users.create(
        username="user@company.com",
        password="password123",
        name="John Smith",
        email="something@company.com",
        role="standard",
    )


def test_users_update(httpx_mock: HTTPXMock, user_json, user_obj):
    updated = copy(user_json)
    updated["enabled"] = False
    updated["name"] = "Disabled"
    user_obj.name = "Disabled"
    user_obj.enabled = False

    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}", method="get", json=user_json
    )
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}",
        method="put",
        match_json={
            "permissions": 32,
            "name": "Disabled",
            "email": "something@company.com",
            "enabled": False,
        },
        json=updated,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == cloud.platform.access_control.users.update(
        user_id=UUID_STR, enabled=False, name="Disabled"
    )


def test_users_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}", method="delete"
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.access_control.users.delete(UUID_UUID) is None


def test_users_details(httpx_mock: HTTPXMock, user_obj, user_json):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}", method="get", json=user_json
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == cloud.platform.access_control.users.details(UUID_UUID)


def test_users_get(httpx_mock: HTTPXMock, user_obj, user_json):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/users", method="get", json={"users": [user_json]}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert [user_obj] == cloud.platform.access_control.users.get()


def test_users_chpasswd(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/chpasswd",
        method="put",
        match_json={"password": "new-password", "temporary": True},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.platform.access_control.users.change_password(
            UUID_STR, password="new-password", temporary=True
        )
        is None
    )


def test_users_enabled(httpx_mock: HTTPXMock, user_json, user_obj):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/enabled",
        method="put",
        match_json={"enabled": True},
        json=user_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == cloud.platform.access_control.users.enabled(UUID_STR, True)


def test_users_api_keys(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/keys",
        method="put",
        json={"accessKey": "123", "secretKey": "987"},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.users.generate_api_keys(UUID_STR)
    assert resp == AccessControlApiKeys(access_key="123", secret_key="987")


def test_users_two_factor(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/two-factor",
        method="put",
        match_json={
            "sms_phone": "+1999-888-7766",
            "sms_enabled": True,
            "email_enabled": True,
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.platform.access_control.users.configure_two_factor(
            UUID_UUID, sms_phone="+1999-888-7766", sms_enabled=True, email_enabled=True
        )
        is None
    )


def test_user_sms_verify(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/two-factor/send-verification",
        method="post",
        match_json={"sms_phone": "+1999-888-7766"},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.platform.access_control.users.send_sms_verification(
            UUID_UUID, sms_phone="+1999-888-7766"
        )
        is None
    )


def test_user_sms_validate(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/two-factor/verify-code",
        method="post",
        match_json={"verification_code": "ABC123"},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.platform.access_control.users.validate_sms_verification(
            UUID_UUID, code="ABC123"
        )
        is None
    )


def test_user_get_authorizations(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/authorizations",
        method="get",
        json={
            "account_uuid": UUID_STR,
            "api_permitted": True,
            "password_permitted": True,
            "saml_permitted": True,
            "user_uuid": UUID_STR,
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.users.get_authorizations(UUID_UUID)
    assert resp == AccessControlUserAuthorizations(
        api=True, password=True, saml=True, account_uuid=UUID_UUID, user_uuid=UUID_UUID
    )


def test_user_update_authorizations(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/authorizations",
        method="get",
        json={
            "account_uuid": UUID_STR,
            "api_permitted": True,
            "password_permitted": True,
            "saml_permitted": True,
            "user_uuid": UUID_STR,
        },
    )
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/authorizations",
        method="put",
        match_json={
            "api_permitted": False,
            "password_permitted": True,
            "saml_permitted": False,
            "mfa_enrollment_required": False,
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.platform.access_control.users.update_authorizations(
            UUID_UUID, api=False, saml=False, mfa=False
        )
        is None
    )


@pytest.mark.asyncio
async def test_async_users_create(httpx_mock: HTTPXMock, user_json, user_obj):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/users",
        method="post",
        match_json={
            "username": "user@company.com",
            "password": "password123",
            "permissions": 32,
            "name": "John Smith",
            "email": "something@company.com",
        },
        json=user_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == await cloud.platform.access_control.users.create(
        username="user@company.com",
        password="password123",
        name="John Smith",
        email="something@company.com",
        role="standard",
    )


@pytest.mark.asyncio
async def test_async_users_update(httpx_mock: HTTPXMock, user_json, user_obj):
    updated = copy(user_json)
    updated["enabled"] = False
    updated["name"] = "Disabled"
    user_obj.name = "Disabled"
    user_obj.enabled = False

    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}", method="get", json=user_json
    )
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}",
        method="put",
        match_json={
            "permissions": 32,
            "name": "Disabled",
            "email": "something@company.com",
            "enabled": False,
        },
        json=updated,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == await cloud.platform.access_control.users.update(
        user_id=UUID_STR, enabled=False, name="Disabled"
    )


@pytest.mark.asyncio
async def test_async_users_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}", method="delete"
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.access_control.users.delete(UUID_UUID) is None


@pytest.mark.asyncio
async def test_async_users_details(httpx_mock: HTTPXMock, user_obj, user_json):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}", method="get", json=user_json
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == await cloud.platform.access_control.users.details(UUID_UUID)


@pytest.mark.asyncio
async def test_async_users_get(httpx_mock: HTTPXMock, user_obj, user_json):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/users", method="get", json={"users": [user_json]}
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert [user_obj] == await cloud.platform.access_control.users.get()


@pytest.mark.asyncio
async def test_async_users_chpasswd(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/chpasswd",
        method="put",
        match_json={"password": "new-password", "temporary": True},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.access_control.users.change_password(
            UUID_STR, password="new-password", temporary=True
        )
        is None
    )


@pytest.mark.asyncio
async def test_async_users_enabled(httpx_mock: HTTPXMock, user_json, user_obj):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/enabled",
        method="put",
        match_json={"enabled": True},
        json=user_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert user_obj == await cloud.platform.access_control.users.enabled(UUID_STR, True)


@pytest.mark.asyncio
async def test_async_users_api_keys(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/keys",
        method="put",
        json={"accessKey": "123", "secretKey": "987"},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.users.generate_api_keys(UUID_STR)
    assert resp == AccessControlApiKeys(access_key="123", secret_key="987")


@pytest.mark.asyncio
async def test_async_users_two_factor(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/two-factor",
        method="put",
        match_json={
            "sms_phone": "+1999-888-7766",
            "sms_enabled": True,
            "email_enabled": True,
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.access_control.users.configure_two_factor(
            UUID_UUID, sms_phone="+1999-888-7766", sms_enabled=True, email_enabled=True
        )
        is None
    )


@pytest.mark.asyncio
async def test_async_user_sms_verify(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/two-factor/send-verification",
        method="post",
        match_json={"sms_phone": "+1999-888-7766"},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.access_control.users.send_sms_verification(
            UUID_UUID, sms_phone="+1999-888-7766"
        )
        is None
    )


@pytest.mark.asyncio
async def test_async_user_sms_validate(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/two-factor/verify-code",
        method="post",
        match_json={"verification_code": "ABC123"},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.access_control.users.validate_sms_verification(
            UUID_UUID, code="ABC123"
        )
        is None
    )


@pytest.mark.asyncio
async def test_async_user_get_authorizations(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/authorizations",
        method="get",
        json={
            "account_uuid": UUID_STR,
            "api_permitted": True,
            "password_permitted": True,
            "saml_permitted": True,
            "user_uuid": UUID_STR,
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.users.get_authorizations(UUID_UUID)
    assert resp == AccessControlUserAuthorizations(
        api=True, password=True, saml=True, account_uuid=UUID_UUID, user_uuid=UUID_UUID
    )


@pytest.mark.asyncio
async def test_async_user_update_authorizations(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/authorizations",
        method="get",
        json={
            "account_uuid": UUID_STR,
            "api_permitted": True,
            "password_permitted": True,
            "saml_permitted": True,
            "user_uuid": UUID_STR,
        },
    )
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/users/{UUID_STR}/authorizations",
        method="put",
        match_json={
            "api_permitted": False,
            "password_permitted": True,
            "saml_permitted": False,
            "mfa_enrollment_required": False,
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.access_control.users.update_authorizations(
            UUID_UUID, api=False, saml=False, mfa=False
        )
        is None
    )
