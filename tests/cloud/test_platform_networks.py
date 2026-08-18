from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.networks import Network

NET_UUID = "42475f11-5e6b-4d6a-a53d-63fe494961df"
LIST_URL = "https://cloud.tenable.com/networks"
DETAIL_URL = f"{LIST_URL}/{NET_UUID}"

SCANNER_JSON = {
    "creation_date": 1521065518,
    "distro": "2.6.32-504.8.1.el6.x86_64",
    "engine_build": "201710101",
    "engine_version": "NNM 5.4.0",
    "group": False,
    "id": 215898,
    "key": "bd98a384ff0e91c8f94fa7f786f8827c1eb7b28dffcfb9895f9d85bd8f0a7d53",
    "last_connect": 1524524576,
    "last_modification_date": 1524523493,
    "linked": 1,
    "loaded_plugin_set": "201803271415",
    "name": "NNM-540",
    "num_scans": 0,
    "owner": "system",
    "owner_id": 1,
    "owner_name": "system",
    "owner_uuid": "ddbd3e11-3311-4682-9912-8e81805fd8a9",
    "platform": "LINUX",
    "pool": False,
    "report_frequency": 3600,
    "settings": {},
    "scan_count": 0,
    "source": "service",
    "status": "off",
    "timestamp": 1524523493,
    "type": "managed_pvs",
    "uuid": "946df0af-0597-4d1e-993d-36a5c25b0d36",
    "remote_uuid": "4e7b9e29-b128-4ae5-9108-b936b35c6f1a9b9a533780bda648",
    "supports_remote_logs": False,
}


def _pagination(total: int, limit: int, offset: int) -> dict[str, Any]:
    return {"total": total, "limit": limit, "offset": offset, "sort": []}


@pytest.fixture
def net_json() -> dict[str, Any]:
    return {
        "owner_uuid": "0e67b283-07a4-464c-a5e4-7b42576962fd",
        "created": 1557526802865,
        "modified": 1557526802865,
        "scanner_count": 0,
        "uuid": NET_UUID,
        "name": "Headquarters",
        "description": "Network devices at Columbia, MD location",
        "is_default": False,
        "created_by": "0f403df2-3b35-4339-9f74-1574805de203",
        "modified_by": "0f403df2-3b35-4339-9f74-1574805de203",
        "assets_ttl_days": 91,
        "created_in_seconds": 1557526802,
        "modified_in_seconds": 1557526802,
    }


@pytest.fixture
def net(net_json) -> Network:
    return Network.model_validate(net_json)


def test_networks_get(httpx_mock: HTTPXMock, net_json, net):
    httpx_mock.add_response(
        url=f"{LIST_URL}?limit=50",
        json={
            "networks": [net_json],
            "pagination": _pagination(total=1, limit=50, offset=0),
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    it = cloud.platform.networks.get()
    items = list(it)
    assert items == [net]
    assert it.total == 1


def test_networks_details(httpx_mock: HTTPXMock, net_json, net):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=net_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.networks.details(NET_UUID) == net


def test_networks_create(httpx_mock: HTTPXMock, net_json, net):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={
            "name": "Headquarters",
            "description": "Network devices at Columbia, MD location",
            "assets_ttl_days": 91,
        },
        json=net_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.networks.create(
        "Headquarters",
        description="Network devices at Columbia, MD location",
        assets_ttl_days=91,
    )
    assert resp == net


def test_networks_update(httpx_mock: HTTPXMock, net_json):
    updated = {**net_json, "name": "Renamed"}
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=net_json)
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={
            "name": "Renamed",
            "description": "Network devices at Columbia, MD location",
            "assets_ttl_days": 91,
        },
        json=updated,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.networks.update(NET_UUID, name="Renamed")
    assert resp == Network.model_validate(updated)


def test_networks_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.networks.delete(NET_UUID) is None


def test_networks_asset_count(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/counts/assets-not-seen-in/180",
        method="get",
        json={"numAssetsNotSeen": 200, "numAssetsTotal": 1000},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.networks.asset_count(NET_UUID, 180)
    assert resp.not_seen == 200
    assert resp.total == 1000


def test_networks_list_scanners(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scanners", method="get", json={"scanners": [SCANNER_JSON]}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.networks.list_scanners(NET_UUID)
    assert len(resp) == 1
    assert resp[0].name == "NNM-540"


def test_networks_assignable_scanners(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/assignable-scanners",
        method="get",
        json={"scanners": [SCANNER_JSON]},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.networks.assignable_scanners(NET_UUID)
    assert len(resp) == 1
    assert resp[0].name == "NNM-540"


def test_networks_assign_scanner(httpx_mock: HTTPXMock):
    scanner_uuid = "946df0af-0597-4d1e-993d-36a5c25b0d36"
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scanners/{scanner_uuid}", method="post", json={}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.networks.assign_scanner(NET_UUID, scanner_uuid) is None


def test_networks_assign_scanners(httpx_mock: HTTPXMock):
    scanner_uuid = "946df0af-0597-4d1e-993d-36a5c25b0d36"
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scanners",
        method="post",
        match_json={"scanner_uuids": [scanner_uuid]},
        json={},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.networks.assign_scanners(NET_UUID, [scanner_uuid]) is None


@pytest.mark.asyncio
async def test_async_networks_get(httpx_mock: HTTPXMock, net_json, net):
    httpx_mock.add_response(
        url=f"{LIST_URL}?limit=50",
        json={
            "networks": [net_json],
            "pagination": _pagination(total=1, limit=50, offset=0),
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    it = await cloud.platform.networks.get()
    items = [item async for item in it]
    assert items == [net]
    assert it.total == 1


@pytest.mark.asyncio
async def test_async_networks_details(httpx_mock: HTTPXMock, net_json, net):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=net_json)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.networks.details(NET_UUID) == net


@pytest.mark.asyncio
async def test_async_networks_create(httpx_mock: HTTPXMock, net_json, net):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={
            "name": "Headquarters",
            "description": "Network devices at Columbia, MD location",
            "assets_ttl_days": 91,
        },
        json=net_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.networks.create(
        "Headquarters",
        description="Network devices at Columbia, MD location",
        assets_ttl_days=91,
    )
    assert resp == net


@pytest.mark.asyncio
async def test_async_networks_update(httpx_mock: HTTPXMock, net_json):
    updated = {**net_json, "name": "Renamed"}
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=net_json)
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={
            "name": "Renamed",
            "description": "Network devices at Columbia, MD location",
            "assets_ttl_days": 91,
        },
        json=updated,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.networks.update(NET_UUID, name="Renamed")
    assert resp == Network.model_validate(updated)


@pytest.mark.asyncio
async def test_async_networks_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.networks.delete(NET_UUID) is None


@pytest.mark.asyncio
async def test_async_networks_asset_count(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/counts/assets-not-seen-in/180",
        method="get",
        json={"numAssetsNotSeen": 200, "numAssetsTotal": 1000},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.networks.asset_count(NET_UUID, 180)
    assert resp.not_seen == 200
    assert resp.total == 1000


@pytest.mark.asyncio
async def test_async_networks_list_scanners(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scanners", method="get", json={"scanners": [SCANNER_JSON]}
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.networks.list_scanners(NET_UUID)
    assert len(resp) == 1
    assert resp[0].name == "NNM-540"


@pytest.mark.asyncio
async def test_async_networks_assignable_scanners(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/assignable-scanners",
        method="get",
        json={"scanners": [SCANNER_JSON]},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.networks.assignable_scanners(NET_UUID)
    assert len(resp) == 1
    assert resp[0].name == "NNM-540"


@pytest.mark.asyncio
async def test_async_networks_assign_scanner(httpx_mock: HTTPXMock):
    scanner_uuid = "946df0af-0597-4d1e-993d-36a5c25b0d36"
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scanners/{scanner_uuid}", method="post", json={}
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.networks.assign_scanner(NET_UUID, scanner_uuid) is None


@pytest.mark.asyncio
async def test_async_networks_assign_scanners(httpx_mock: HTTPXMock):
    scanner_uuid = "946df0af-0597-4d1e-993d-36a5c25b0d36"
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scanners",
        method="post",
        match_json={"scanner_uuids": [scanner_uuid]},
        json={},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.networks.assign_scanners(NET_UUID, [scanner_uuid]) is None
    )
