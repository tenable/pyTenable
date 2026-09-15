from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.scanners import Scanner, ScannerDirective

SCANNER_ID = 597670
BASE_URL = "https://cloud.tenable.com/scanners"
DETAIL_URL = f"{BASE_URL}/{SCANNER_ID}"
SCANNER_UUID = "b2c3d4e5-f6a7-8901-bcde-f12345678901"


@pytest.fixture
def scanner_json() -> dict[str, Any]:
    return {
        "creation_date": 1736849655,
        "distro": "es8-x86-64",
        "engine_version": "19.10.4",
        "group": False,
        "hostname": "scanner-01.example.com",
        "id": SCANNER_ID,
        "ip_addresses": ["192.0.2.10"],
        "key": "6dec14cb6d33bce4173b8bd0a022400e306629ddca7951bebe4252a6973c16ce",
        "last_connect": 1749805356,
        "last_modification_date": 1749721290,
        "linked": 1,
        "loaded_plugin_set": "202506110237",
        "name": "Production Scanner",
        "network_name": "Default",
        "num_scans": 3,
        "owner": "system",
        "owner_id": 1,
        "owner_name": "system",
        "owner_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "platform": "LINUX",
        "pool": False,
        "scan_count": 3,
        "shared": 1,
        "source": "service",
        "status": "on",
        "timestamp": 1749721290,
        "type": "remote",
        "ui_build": "28",
        "ui_version": "10.8.4",
        "user_permissions": 128,
        "uuid": SCANNER_UUID,
        "supports_remote_logs": False,
        "supports_webapp": False,
        "supports_remote_settings": True,
        "profile_uuid": "00000000-0000-0000-0000-000000000000",
        "profile_name": "Default",
    }


@pytest.fixture
def scanner(scanner_json) -> Scanner:
    return Scanner.model_validate(scanner_json)


def test_scanners_get(httpx_mock: HTTPXMock, scanner_json, scanner):
    httpx_mock.add_response(
        url=BASE_URL, method="get", json={"scanners": [scanner_json]}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.get()
    assert resp == [scanner]


def test_scanners_details(httpx_mock: HTTPXMock, scanner_json, scanner):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=scanner_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.scanners.details(SCANNER_ID) == scanner


def test_scanners_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={"name": "Renamed", "force_plugin_update": 1},
        json={"id": SCANNER_ID, "name": "Renamed"},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.update(
        SCANNER_ID, name="Renamed", force_plugin_update=True
    )
    assert resp.id == SCANNER_ID
    assert resp.name == "Renamed"


def test_scanners_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.scanners.delete(SCANNER_ID) is None


def test_scanners_key(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/key",
        method="get",
        json={
            "key": "615f4cbeda288998dffe534d36385a422cd4e27be34dcdd7738dc0a01b787f5f"
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.key(SCANNER_ID)
    assert resp == "615f4cbeda288998dffe534d36385a422cd4e27be34dcdd7738dc0a01b787f5f"


def test_scanners_set_link_state(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/link", method="put", match_json={"link": 0}, json={}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.scanners.set_link_state(SCANNER_ID, False) is None


def test_scanners_aws_targets(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/aws-targets",
        method="get",
        json={
            "targets": [
                {
                    "scanner_id": SCANNER_ID,
                    "instance_id": "i-1234567890abcdef0",
                    "private_ip": "192.0.2.10",
                    "public_ip": "203.0.113.10",
                    "state": "running",
                    "zone": "us-east-1a",
                    "type": "t2.small",
                    "name": "my-instance",
                }
            ]
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.aws_targets(SCANNER_ID)
    assert len(resp) == 1
    assert resp[0].instance_id == "i-1234567890abcdef0"


def test_scanners_scans(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scans",
        method="get",
        json={
            "scans": [
                {
                    "scan_id": 36,
                    "scanner_uuid": "00000000-0000-0000-0000-00000000000000000000000000001",
                    "name": "Basic Scan",
                    "status": "pending",
                    "id": "007d0e76-fcec-455d-a5e2-fac16772560c",
                    "user": "API Demo User",
                    "last_modification_date": 1545945321,
                    "start_time": 1545945321,
                    "network_id": "6be6cbfe-2c4b-4f3c-b959-127362d2dcce",
                }
            ]
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.scans(SCANNER_ID)
    assert len(resp) == 1
    assert resp[0].name == "Basic Scan"


def test_scanners_control_scan(httpx_mock: HTTPXMock):
    scan_uuid = "007d0e76-fcec-455d-a5e2-fac16772560c"
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scans/{scan_uuid}/control",
        method="post",
        match_json={"action": "stop"},
        json={},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.scanners.control_scan(SCANNER_ID, scan_uuid, "stop") is None


def test_scanners_get_config(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/config",
        method="get",
        json={"concurrent_update": {"enabled": True, "max_concurrent_update": 5}},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.get_config()
    assert resp.concurrent_update.enabled is True
    assert resp.concurrent_update.max_concurrent_update == 5


def test_scanners_update_config(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/config",
        method="get",
        json={"concurrent_update": {"enabled": True, "max_concurrent_update": 5}},
    )
    httpx_mock.add_response(
        url=f"{BASE_URL}/config",
        method="put",
        match_json={
            "concurrent_update": {"enabled": False, "max_concurrent_update": 10}
        },
        json={"concurrent_update": {"enabled": False, "max_concurrent_update": 10}},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.update_config(
        concurrent_update_enabled=False, concurrent_update_max_scanners=10
    )
    assert resp.concurrent_update.enabled is False
    assert resp.concurrent_update.max_concurrent_update == 10


def test_scanners_request_status(httpx_mock: HTTPXMock):
    request_id = "e0ab9f07-dd4e-4891-9eed-01b47db5ead6"
    httpx_mock.add_response(
        url=f"{BASE_URL}/request-status/{request_id}",
        method="get",
        json={
            "container_uuid": "c050dec4-78a7-4d9a-9905-ab9cb3757766",
            "type": "service-scanner-bulk-operation",
            "id": request_id,
            "status": "completed",
            "created": 1738350594,
            "modified": 1738350594,
            "expiration": 1738352394,
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.scanners.request_status(request_id)
    assert resp.status == "completed"


def test_scanners_send_directive(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/{SCANNER_UUID}/directives",
        method="post",
        match_json={"type": "restart", "options": {"hard": True}},
        json={
            "container_uuid": "4496ea88-1d4d-43e8-b373-973b0870fd7d",
            "uuid": "61cadb4c-a245-40d3-a77f-6a9001e8def4",
            "sensor_uuid": "51f6a2bf-c2ea-478d-bffd-0a81cfe4529a",
            "owner_uuid": "2e9cecda-3821-4032-a093-ddd0cbd8b9b9",
            "type": "restart",
            "status": "pending",
            "created": 1652937372838,
            "modified": 1652937372838,
            "results_blob_size": 0,
            "ttl": 604800,
            "id": "61cadb4c-a245-40d3-a77f-6a9001e8def4",
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    directive = ScannerDirective.model_validate(
        {"type": "restart", "options": {"hard": True}}
    )
    resp = cloud.platform.scanners.send_directive(SCANNER_UUID, directive)
    assert resp.status == "pending"


def test_scanners_send_bulk_directive(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/bulk/directives",
        method="post",
        match_json={
            "all_scanners": "true",
            "directive": {"type": "restart", "options": {"hard": True}},
        },
        json=[
            {
                "container_uuid": "5496ea88-1d4d-43e8-b373-973b0870fd7d",
                "uuid": "ca9a4400-b443-4f9f-92e5-bcc78eaf1480",
                "sensor_uuid": "52f6a2bf-c2ea-478d-bffd-0a81cfe4529a",
                "owner_uuid": "2b9cecda-3821-4032-a093-ddd0cbd8b9b9",
                "type": "restart",
                "status": "pending",
                "created": 1658774368372,
                "modified": 1658774368372,
                "results_blob_size": 0,
                "id": "cd9a4400-b443-4f9f-92e5-bcc78eaf1480",
                "ttl": 604800,
            }
        ],
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    directive = ScannerDirective.model_validate(
        {"type": "restart", "options": {"hard": True}}
    )
    resp = cloud.platform.scanners.send_bulk_directive(directive, all_scanners=True)
    assert len(resp) == 1
    assert resp[0].status == "pending"


@pytest.mark.asyncio
async def test_async_scanners_get(httpx_mock: HTTPXMock, scanner_json, scanner):
    httpx_mock.add_response(
        url=BASE_URL, method="get", json={"scanners": [scanner_json]}
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.get()
    assert resp == [scanner]


@pytest.mark.asyncio
async def test_async_scanners_details(httpx_mock: HTTPXMock, scanner_json, scanner):
    httpx_mock.add_response(url=DETAIL_URL, method="get", json=scanner_json)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.scanners.details(SCANNER_ID) == scanner


@pytest.mark.asyncio
async def test_async_scanners_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={"name": "Renamed", "force_plugin_update": 1},
        json={"id": SCANNER_ID, "name": "Renamed"},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.update(
        SCANNER_ID, name="Renamed", force_plugin_update=True
    )
    assert resp.id == SCANNER_ID
    assert resp.name == "Renamed"


@pytest.mark.asyncio
async def test_async_scanners_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.scanners.delete(SCANNER_ID) is None


@pytest.mark.asyncio
async def test_async_scanners_key(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/key",
        method="get",
        json={
            "key": "615f4cbeda288998dffe534d36385a422cd4e27be34dcdd7738dc0a01b787f5f"
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.key(SCANNER_ID)
    assert resp == "615f4cbeda288998dffe534d36385a422cd4e27be34dcdd7738dc0a01b787f5f"


@pytest.mark.asyncio
async def test_async_scanners_set_link_state(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/link", method="put", match_json={"link": 0}, json={}
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.scanners.set_link_state(SCANNER_ID, False) is None


@pytest.mark.asyncio
async def test_async_scanners_aws_targets(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/aws-targets",
        method="get",
        json={
            "targets": [
                {
                    "scanner_id": SCANNER_ID,
                    "instance_id": "i-1234567890abcdef0",
                    "private_ip": "192.0.2.10",
                    "public_ip": "203.0.113.10",
                    "state": "running",
                    "zone": "us-east-1a",
                    "type": "t2.small",
                    "name": "my-instance",
                }
            ]
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.aws_targets(SCANNER_ID)
    assert len(resp) == 1
    assert resp[0].instance_id == "i-1234567890abcdef0"


@pytest.mark.asyncio
async def test_async_scanners_scans(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scans",
        method="get",
        json={
            "scans": [
                {
                    "scan_id": 36,
                    "scanner_uuid": "00000000-0000-0000-0000-00000000000000000000000000001",
                    "name": "Basic Scan",
                    "status": "pending",
                    "id": "007d0e76-fcec-455d-a5e2-fac16772560c",
                    "user": "API Demo User",
                    "last_modification_date": 1545945321,
                    "start_time": 1545945321,
                    "network_id": "6be6cbfe-2c4b-4f3c-b959-127362d2dcce",
                }
            ]
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.scans(SCANNER_ID)
    assert len(resp) == 1
    assert resp[0].name == "Basic Scan"


@pytest.mark.asyncio
async def test_async_scanners_control_scan(httpx_mock: HTTPXMock):
    scan_uuid = "007d0e76-fcec-455d-a5e2-fac16772560c"
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/scans/{scan_uuid}/control",
        method="post",
        match_json={"action": "stop"},
        json={},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        await cloud.platform.scanners.control_scan(SCANNER_ID, scan_uuid, "stop")
        is None
    )


@pytest.mark.asyncio
async def test_async_scanners_get_config(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/config",
        method="get",
        json={"concurrent_update": {"enabled": True, "max_concurrent_update": 5}},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.get_config()
    assert resp.concurrent_update.enabled is True
    assert resp.concurrent_update.max_concurrent_update == 5


@pytest.mark.asyncio
async def test_async_scanners_update_config(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/config",
        method="get",
        json={"concurrent_update": {"enabled": True, "max_concurrent_update": 5}},
    )
    httpx_mock.add_response(
        url=f"{BASE_URL}/config",
        method="put",
        match_json={
            "concurrent_update": {"enabled": False, "max_concurrent_update": 10}
        },
        json={"concurrent_update": {"enabled": False, "max_concurrent_update": 10}},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.update_config(
        concurrent_update_enabled=False, concurrent_update_max_scanners=10
    )
    assert resp.concurrent_update.enabled is False
    assert resp.concurrent_update.max_concurrent_update == 10


@pytest.mark.asyncio
async def test_async_scanners_request_status(httpx_mock: HTTPXMock):
    request_id = "e0ab9f07-dd4e-4891-9eed-01b47db5ead6"
    httpx_mock.add_response(
        url=f"{BASE_URL}/request-status/{request_id}",
        method="get",
        json={
            "container_uuid": "c050dec4-78a7-4d9a-9905-ab9cb3757766",
            "type": "service-scanner-bulk-operation",
            "id": request_id,
            "status": "completed",
            "created": 1738350594,
            "modified": 1738350594,
            "expiration": 1738352394,
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.scanners.request_status(request_id)
    assert resp.status == "completed"


@pytest.mark.asyncio
async def test_async_scanners_send_directive(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/{SCANNER_UUID}/directives",
        method="post",
        match_json={"type": "restart", "options": {"hard": True}},
        json={
            "container_uuid": "4496ea88-1d4d-43e8-b373-973b0870fd7d",
            "uuid": "61cadb4c-a245-40d3-a77f-6a9001e8def4",
            "sensor_uuid": "51f6a2bf-c2ea-478d-bffd-0a81cfe4529a",
            "owner_uuid": "2e9cecda-3821-4032-a093-ddd0cbd8b9b9",
            "type": "restart",
            "status": "pending",
            "created": 1652937372838,
            "modified": 1652937372838,
            "results_blob_size": 0,
            "ttl": 604800,
            "id": "61cadb4c-a245-40d3-a77f-6a9001e8def4",
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    directive = ScannerDirective.model_validate(
        {"type": "restart", "options": {"hard": True}}
    )
    resp = await cloud.platform.scanners.send_directive(SCANNER_UUID, directive)
    assert resp.status == "pending"


@pytest.mark.asyncio
async def test_async_scanners_send_bulk_directive(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/bulk/directives",
        method="post",
        match_json={
            "all_scanners": "true",
            "directive": {"type": "restart", "options": {"hard": True}},
        },
        json=[
            {
                "container_uuid": "5496ea88-1d4d-43e8-b373-973b0870fd7d",
                "uuid": "ca9a4400-b443-4f9f-92e5-bcc78eaf1480",
                "sensor_uuid": "52f6a2bf-c2ea-478d-bffd-0a81cfe4529a",
                "owner_uuid": "2b9cecda-3821-4032-a093-ddd0cbd8b9b9",
                "type": "restart",
                "status": "pending",
                "created": 1658774368372,
                "modified": 1658774368372,
                "results_blob_size": 0,
                "id": "cd9a4400-b443-4f9f-92e5-bcc78eaf1480",
                "ttl": 604800,
            }
        ],
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    directive = ScannerDirective.model_validate(
        {"type": "restart", "options": {"hard": True}}
    )
    resp = await cloud.platform.scanners.send_bulk_directive(
        directive, all_scanners=True
    )
    assert len(resp) == 1
    assert resp[0].status == "pending"
