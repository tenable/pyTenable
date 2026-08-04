from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.exclusions import Exclusion, ExclusionSchedule

EXCL_ID = 1000107
EXCL_UUID = "84a77c2f-b4db-4bd5-9bd3-d3cb078875aa"
LIST_URL = "https://cloud.tenable.com/exclusions"
DETAIL_URL = f"{LIST_URL}/{EXCL_ID}"


def _pagination(total: int, limit: int, offset: int) -> dict[str, Any]:
    return {"total": total, "limit": limit, "offset": offset, "sort": None}


@pytest.fixture
def excl_json() -> dict[str, Any]:
    return {
        "uuid": EXCL_UUID,
        "members": "host.domain.com,192.0.2.1,192.0.2.1-192.0.2.255",
        "name": "My-Exclusion-2",
        "description": "My description.",
        "id": EXCL_ID,
        "schedule": {
            "enabled": True,
            "starttime": "2023-09-01 00:00:00",
            "endtime": "2023-09-02 00:00:00",
            "rrules": {"freq": "MONTHLY", "bymonthday": 4},
            "timezone": "America/Chicago",
        },
        "creation_date": 1745959227,
        "last_modification_date": 1745959227,
        "network_id": "00000000-0000-0000-0000-000000000000",
    }


@pytest.fixture
def excl(excl_json) -> Exclusion:
    return Exclusion.model_validate(excl_json)


def test_exclusions_get(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=f"{LIST_URL}?limit=200",
        json={
            "exclusions": [excl_json],
            "pagination": _pagination(total=1, limit=200, offset=0),
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    it = cloud.platform.exclusions.get()
    items = list(it)
    assert items == [excl]
    assert it.total == 1


def test_exclusions_details(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=excl_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.exclusions.details(EXCL_ID) == excl


def test_exclusions_create(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={
            "name": "My-Exclusion-2",
            "members": "192.0.2.1,192.0.2.1-192.0.2.255",
        },
        json=excl_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.exclusions.create(
        "My-Exclusion-2", ["192.0.2.1", "192.0.2.1-192.0.2.255"]
    )
    assert resp == excl


def test_exclusions_create_with_schedule(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={
            "name": "My-Exclusion-2",
            "members": "192.0.2.1",
            "description": "My description.",
            "schedule": {
                "enabled": True,
                "starttime": "2023-09-01T00:00:00",
                "endtime": "2023-09-02T00:00:00",
                "rrules": {"freq": "MONTHLY", "bymonthday": 4},
                "timezone": "America/Chicago",
            },
            "network_id": "00000000-0000-0000-0000-000000000000",
        },
        json=excl_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.exclusions.create(
        "My-Exclusion-2",
        ["192.0.2.1"],
        description="My description.",
        schedule=ExclusionSchedule.model_validate(excl_json["schedule"]),
        network_id="00000000-0000-0000-0000-000000000000",
    )
    assert resp == excl


def test_exclusions_update(httpx_mock: HTTPXMock, excl_json):
    updated = {**excl_json, "name": "Renamed"}
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=excl_json)
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={
            "name": "Renamed",
            "members": "host.domain.com,192.0.2.1,192.0.2.1-192.0.2.255",
            "description": "My description.",
            "schedule": {
                "enabled": True,
                "starttime": "2023-09-01T00:00:00",
                "endtime": "2023-09-02T00:00:00",
                "rrules": {"freq": "MONTHLY", "bymonthday": 4},
                "timezone": "America/Chicago",
            },
            "network_id": "00000000-0000-0000-0000-000000000000",
        },
        json=updated,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.exclusions.update(EXCL_ID, name="Renamed")
    assert resp == Exclusion.model_validate(updated)


def test_exclusions_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.exclusions.delete(EXCL_ID) is None


def test_exclusions_import(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(url=f"{LIST_URL}/import", method="post", json=[excl_json])
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.exclusions.import_exclusions(b"name,members\n")
    assert resp == [excl]


@pytest.mark.asyncio
async def test_async_exclusions_get(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=f"{LIST_URL}?limit=200",
        json={
            "exclusions": [excl_json],
            "pagination": _pagination(total=1, limit=200, offset=0),
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    it = await cloud.platform.exclusions.get()
    items = [item async for item in it]
    assert items == [excl]
    assert it.total == 1


@pytest.mark.asyncio
async def test_async_exclusions_details(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=excl_json)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.exclusions.details(EXCL_ID) == excl


@pytest.mark.asyncio
async def test_async_exclusions_create(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={
            "name": "My-Exclusion-2",
            "members": "192.0.2.1,192.0.2.1-192.0.2.255",
        },
        json=excl_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.exclusions.create(
        "My-Exclusion-2", ["192.0.2.1", "192.0.2.1-192.0.2.255"]
    )
    assert resp == excl


@pytest.mark.asyncio
async def test_async_exclusions_update(httpx_mock: HTTPXMock, excl_json):
    updated = {**excl_json, "name": "Renamed"}
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=excl_json)
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={
            "name": "Renamed",
            "members": "host.domain.com,192.0.2.1,192.0.2.1-192.0.2.255",
            "description": "My description.",
            "schedule": {
                "enabled": True,
                "starttime": "2023-09-01T00:00:00",
                "endtime": "2023-09-02T00:00:00",
                "rrules": {"freq": "MONTHLY", "bymonthday": 4},
                "timezone": "America/Chicago",
            },
            "network_id": "00000000-0000-0000-0000-000000000000",
        },
        json=updated,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.exclusions.update(EXCL_ID, name="Renamed")
    assert resp == Exclusion.model_validate(updated)


@pytest.mark.asyncio
async def test_async_exclusions_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.exclusions.delete(EXCL_ID) is None


@pytest.mark.asyncio
async def test_async_exclusions_import(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(url=f"{LIST_URL}/import", method="post", json=[excl_json])
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.exclusions.import_exclusions(b"name,members\n")
    assert resp == [excl]
