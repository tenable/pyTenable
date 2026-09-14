import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.server import ServerProperties, ServerStatus

STATUS_URL = "https://cloud.tenable.com/server/status"
PROPERTIES_URL = "https://cloud.tenable.com/server/properties"

STATUS_JSON = {"code": 200, "status": "ready"}

PROPERTIES_JSON = {
    "limitEnabled": False,
    "region": "US East",
    "loaded_plugin_set": "201812271241",
    "server_uuid": "b6a6d233-9f14-4ce9-b4cf-7440e027cf5c27789b39c292efc6",
    "update": {"href": None, "new_version": 0, "restart": 0},
    "expiration": 1551160800,
    "nessus_ui_version": "11.0.52",
    "nessus_type": "Nessus Cloud",
    "notifications": [],
    "expiration_time": 60,
    "license": {
        "enterprise_pause": False,
        "expiration_date": 1551160800,
        "ips": 1024,
        "agents": 512,
        "users": 10,
        "scanners": 2,
        "evaluation": False,
        "scanners_used": 0,
        "agents_used": 0,
    },
    "enterprise": True,
    "analytics": {
        "key": "8fbd8613-075b-4dff-99c9-ea5decc0b7cf",
        "enabled": True,
        "site_id": "us-2b",
    },
    "msp": True,
    "server_build": "C20023",
    "force_ui_reload": True,
    "capabilities": {
        "multi_user": "full",
        "multi_scanner": True,
        "report_email_config": True,
    },
    "plugin_set": "201812271241",
    "idle_timeout": 30,
    "nessus_ui_build": "161",
    "scanner_boottime": 1545191736,
    "container_db_version": "10.43.0",
    "login_banner": None,
    "server_version": "6.9.1",
}


def test_server_status(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=STATUS_URL, method="get", json=STATUS_JSON)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    status = cloud.platform.server.status()
    assert status == ServerStatus.model_validate(STATUS_JSON)


@pytest.mark.asyncio
async def test_async_server_status(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=STATUS_URL, method="get", json=STATUS_JSON)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    status = await cloud.platform.server.status()
    assert status == ServerStatus.model_validate(STATUS_JSON)


def test_server_properties(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=PROPERTIES_URL, method="get", json=PROPERTIES_JSON)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    props = cloud.platform.server.properties()
    assert props == ServerProperties.model_validate(PROPERTIES_JSON)


@pytest.mark.asyncio
async def test_async_server_properties(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=PROPERTIES_URL, method="get", json=PROPERTIES_JSON)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    props = await cloud.platform.server.properties()
    assert props == ServerProperties.model_validate(PROPERTIES_JSON)
