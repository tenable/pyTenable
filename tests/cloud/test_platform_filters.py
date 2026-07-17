from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.filters import (
    AgentFilters,
    AssetFilters,
    CredentialFilters,
    ReportFilters,
    ScanFilters,
    ScanHistoryFilters,
    VulnerabilityFilters,
)

BASE_URL = "https://cloud.tenable.com/filters"


def _base_filter_json() -> dict[str, Any]:
    return {
        "wildcard_fields": ["name"],
        "sort": {"max_sort_fields": 1, "sortable_fields": ["name"]},
        "filters": [],
    }


def _scan_filter_json() -> dict[str, Any]:
    return {
        "filters": [
            {"name": "name", "operators": ["match", "eq"], "type": "string"}
        ]
    }


def test_filters_agent(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/scans/agents", json=data)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.filters.agent()
    assert resp == AgentFilters.model_validate(data)


def test_filters_asset(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/workbenches/assets", json=data)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.filters.asset()
    assert resp == AssetFilters.model_validate(data)


def test_filters_credential(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/credentials", json=data)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.filters.credential()
    assert resp == CredentialFilters.model_validate(data)


def test_filters_report(httpx_mock: HTTPXMock):
    data = _scan_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/reports/export", json=data)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.filters.report()
    assert resp == ReportFilters.model_validate(data)


def test_filters_scan(httpx_mock: HTTPXMock):
    data = _scan_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/scans/reports", json=data)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.filters.scan()
    assert resp == ScanFilters.model_validate(data)


def test_filters_scan_history(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/scans/reports/history", json=data)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.filters.scan_history()
    assert resp == ScanHistoryFilters.model_validate(data)


def test_filters_vulnerability(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/workbenches/vulnerabilities", json=data)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.filters.vulnerability()
    assert resp == VulnerabilityFilters.model_validate(data)


@pytest.mark.asyncio
async def test_async_filters_agent(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/scans/agents", json=data)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.filters.agent()
    assert resp == AgentFilters.model_validate(data)


@pytest.mark.asyncio
async def test_async_filters_asset(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/workbenches/assets", json=data)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.filters.asset()
    assert resp == AssetFilters.model_validate(data)


@pytest.mark.asyncio
async def test_async_filters_credential(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/credentials", json=data)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.filters.credential()
    assert resp == CredentialFilters.model_validate(data)


@pytest.mark.asyncio
async def test_async_filters_report(httpx_mock: HTTPXMock):
    data = _scan_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/reports/export", json=data)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.filters.report()
    assert resp == ReportFilters.model_validate(data)


@pytest.mark.asyncio
async def test_async_filters_scan(httpx_mock: HTTPXMock):
    data = _scan_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/scans/reports", json=data)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.filters.scan()
    assert resp == ScanFilters.model_validate(data)


@pytest.mark.asyncio
async def test_async_filters_scan_history(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/scans/reports/history", json=data)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.filters.scan_history()
    assert resp == ScanHistoryFilters.model_validate(data)


@pytest.mark.asyncio
async def test_async_filters_vulnerability(httpx_mock: HTTPXMock):
    data = _base_filter_json()
    httpx_mock.add_response(url=f"{BASE_URL}/workbenches/vulnerabilities", json=data)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.filters.vulnerability()
    assert resp == VulnerabilityFilters.model_validate(data)
