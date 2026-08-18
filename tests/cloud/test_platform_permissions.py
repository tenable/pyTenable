import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.permissions import ACL, ACLRequest

OBJECT_TYPE = "scan"
OBJECT_ID = 1000107
DETAIL_URL = f"https://cloud.tenable.com/permissions/{OBJECT_TYPE}/{OBJECT_ID}"

ACLS_JSON = [
    {
        "type": "user",
        "id": 1,
        "uuid": "1035e55d-a984-4b1c-acc7-fd2d472126f1",
        "name": "system",
        "display_name": "system",
        "permissions": 128,
        "owner": 1,
    },
    {"type": "default", "permissions": 16},
]


def test_permissions_get(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json={"acls": ACLS_JSON})
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.permissions.get(OBJECT_TYPE, OBJECT_ID)
    assert resp == [ACL.model_validate(item) for item in ACLS_JSON]
    assert resp[0].permissions == "owner"
    assert resp[1].permissions == "can_use"


def test_permissions_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={"acls": [{"type": "default", "permissions": 32}]},
        json={},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    acls = [ACLRequest(type="default", permissions="can_execute")]
    assert cloud.platform.permissions.update(OBJECT_TYPE, OBJECT_ID, acls) is None


@pytest.mark.asyncio
async def test_async_permissions_get(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json={"acls": ACLS_JSON})
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.permissions.get(OBJECT_TYPE, OBJECT_ID)
    assert resp == [ACL.model_validate(item) for item in ACLS_JSON]
    assert resp[0].permissions == "owner"
    assert resp[1].permissions == "can_use"


@pytest.mark.asyncio
async def test_async_permissions_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={"acls": [{"type": "default", "permissions": 32}]},
        json={},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    acls = [ACLRequest(type="default", permissions="can_execute")]
    assert await cloud.platform.permissions.update(OBJECT_TYPE, OBJECT_ID, acls) is None
