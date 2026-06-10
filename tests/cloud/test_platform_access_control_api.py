import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.access_control.models import AllowedIPAddresses


def test_allowed_ip_address_model():
    m = AllowedIPAddresses.model_validate(
        {
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        }
    )
    assert m.ipv4 == ["192.168.0.1", "127.0.0.1"]
    assert m.ipv6 == []
    assert m.model_dump(mode="json") == {
        "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
        "allowed_ipv6_addresses": "",
    }


def test_get_allowed_ip_addresses(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/access-control/v1/api-security-settings",
        method="get",
        json={
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.api.get_allowed_ips()
    assert resp == AllowedIPAddresses.model_validate(
        {
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        }
    )
    assert resp.ipv4 == ["192.168.0.1", "127.0.0.1"]
    assert resp.ipv6 == []


def test_update_allowed_ips(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/access-control/v1/api-security-settings",
        method="put",
        match_json={
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.access_control.api.update_allowed_ips(
        ipv4=["192.168.0.1", "127.0.0.1"]
    )
    assert resp is None


@pytest.mark.asyncio
async def test_async_get_allowed_ip_addresses(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/access-control/v1/api-security-settings",
        method="get",
        json={
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.api.get_allowed_ips()
    assert resp == AllowedIPAddresses.model_validate(
        {
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        }
    )
    assert resp.ipv4 == ["192.168.0.1", "127.0.0.1"]
    assert resp.ipv6 == []


@pytest.mark.asyncio
async def test_async_update_allowed_ips(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/access-control/v1/api-security-settings",
        method="put",
        match_json={
            "allowed_ipv4_addresses": "192.168.0.1,127.0.0.1",
            "allowed_ipv6_addresses": "",
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.access_control.api.update_allowed_ips(
        ipv4=["192.168.0.1", "127.0.0.1"]
    )
    assert resp is None
