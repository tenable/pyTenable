from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.agents import AgentExclusion

EXCL_ID = 123
EXCL_URL = f"https://cloud.tenable.com/scanners/null/agents/exclusions/{EXCL_ID}"
LIST_URL = "https://cloud.tenable.com/scanners/null/agents/exclusions"


@pytest.fixture
def excl_json() -> dict[str, Any]:
    return {
        "uuid": "12345678-1234-1234-1234-123456789012",
        "id": EXCL_ID,
        "name": "Test Exclusion",
        "description": "A test exclusion",
        "creation_date": 1515620036,
        "last_modification_date": 1515620036,
        "core_updates_blocked": False,
        "schedule": {"enabled": False},
    }


@pytest.fixture
def excl(excl_json) -> AgentExclusion:
    return AgentExclusion.model_validate(excl_json)


def test_exclusion_create(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={"name": "Test Exclusion", "description": "A test exclusion"},
        json=excl_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.exclusions.create(
        name="Test Exclusion", description="A test exclusion"
    )
    assert resp == excl


def test_exclusion_create_no_description(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={"name": "Test Exclusion"},
        json=excl_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.exclusions.create(name="Test Exclusion")
    assert resp == excl


def test_exclusion_get(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="get",
        json={"exclusions": [excl_json]},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.exclusions.get()
    assert resp == [excl]


def test_exclusion_details(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(url=EXCL_URL, method="get", json=excl_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.exclusions.details(EXCL_ID) == excl


def test_exclusion_update(httpx_mock: HTTPXMock, excl_json):
    updated = {**excl_json, "name": "Updated"}
    httpx_mock.add_response(url=EXCL_URL, method="get", json=excl_json)
    httpx_mock.add_response(
        url=EXCL_URL,
        method="put",
        match_json={
            "name": "Updated",
            "description": "A test exclusion",
            "schedule": {"enabled": False},
        },
        json=updated,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.exclusions.update(EXCL_ID, name="Updated")
    assert resp == AgentExclusion.model_validate(updated)


def test_exclusion_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=EXCL_URL, method="delete")
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.exclusions.delete(EXCL_ID) is None


@pytest.mark.asyncio
async def test_async_exclusion_create(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json={"name": "Test Exclusion", "description": "A test exclusion"},
        json=excl_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.exclusions.create(
        name="Test Exclusion", description="A test exclusion"
    )
    assert resp == excl


@pytest.mark.asyncio
async def test_async_exclusion_get(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(
        url=LIST_URL,
        method="get",
        json={"exclusions": [excl_json]},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.exclusions.get()
    assert resp == [excl]


@pytest.mark.asyncio
async def test_async_exclusion_details(httpx_mock: HTTPXMock, excl_json, excl):
    httpx_mock.add_response(url=EXCL_URL, method="get", json=excl_json)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.exclusions.details(EXCL_ID) == excl


@pytest.mark.asyncio
async def test_async_exclusion_update(httpx_mock: HTTPXMock, excl_json):
    updated = {**excl_json, "name": "Updated"}
    httpx_mock.add_response(url=EXCL_URL, method="get", json=excl_json)
    httpx_mock.add_response(
        url=EXCL_URL,
        method="put",
        match_json={
            "name": "Updated",
            "description": "A test exclusion",
            "schedule": {"enabled": False},
        },
        json=updated,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.exclusions.update(EXCL_ID, name="Updated")
    assert resp == AgentExclusion.model_validate(updated)


@pytest.mark.asyncio
async def test_async_exclusion_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=EXCL_URL, method="delete")
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.exclusions.delete(EXCL_ID) is None
