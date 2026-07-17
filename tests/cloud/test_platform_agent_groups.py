from typing import Any
from uuid import UUID

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.agents import AgentGroup

GROUP_ID = 42
AGENT_ID = 7
AGENT_UUID = UUID("11111111-2222-3333-4444-555555555555")
BASE_URL = "https://cloud.tenable.com/scanners/null/agent-groups"
GROUP_URL = f"{BASE_URL}/{GROUP_ID}"


@pytest.fixture
def group_json() -> dict[str, Any]:
    return {
        "id": GROUP_ID,
        "uuid": "12345678-1234-1234-1234-123456789012",
        "name": "Test Group",
        "owner": "owner@example.com",
        "owner_name": "Owner Name",
        "owner_uuid": "87654321-4321-4321-4321-123456654321",
        "user_permissions": 64,
        "agents_count": 0,
        "agents": [],
        "creation_date": 1515620036,
        "last_modification_date": 1515620036,
    }


@pytest.fixture
def group(group_json) -> AgentGroup:
    return AgentGroup.model_validate(group_json)


def test_agent_group_create(httpx_mock: HTTPXMock, group_json, group):
    httpx_mock.add_response(
        url=BASE_URL,
        method="post",
        match_json={"name": "Test Group"},
        json=group_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.groups.create("Test Group") == group


def test_agent_group_update(httpx_mock: HTTPXMock, group_json):
    updated = {**group_json, "name": "Updated Group"}
    httpx_mock.add_response(
        url=GROUP_URL,
        method="put",
        match_json={"name": "Updated Group"},
        json=updated,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.groups.update(GROUP_ID, name="Updated Group")
    assert resp == AgentGroup.model_validate(updated)


def test_agent_group_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=GROUP_URL, method="delete")
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.groups.delete(GROUP_ID) is None


def test_agent_group_get(httpx_mock: HTTPXMock, group_json, group):
    httpx_mock.add_response(
        url=BASE_URL,
        method="get",
        json={"groups": [group_json]},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.groups.get() == [group]


def test_agent_group_details(httpx_mock: HTTPXMock, group_json, group):
    httpx_mock.add_response(url=GROUP_URL, method="get", json=group_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.groups.details(GROUP_ID) == group


def test_agent_group_add(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_ID}",
        method="put",
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.groups.add(GROUP_ID, AGENT_ID) is None


def test_agent_group_remove(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_ID}",
        method="delete",
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.agents.groups.remove(GROUP_ID, AGENT_ID) is None


@pytest.mark.asyncio
async def test_async_agent_group_create(httpx_mock: HTTPXMock, group_json, group):
    httpx_mock.add_response(
        url=BASE_URL,
        method="post",
        match_json={"name": "Test Group"},
        json=group_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.groups.create("Test Group") == group


@pytest.mark.asyncio
async def test_async_agent_group_update(httpx_mock: HTTPXMock, group_json):
    updated = {**group_json, "name": "Updated Group"}
    httpx_mock.add_response(
        url=GROUP_URL,
        method="put",
        match_json={"name": "Updated Group"},
        json=updated,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.groups.update(GROUP_ID, name="Updated Group")
    assert resp == AgentGroup.model_validate(updated)


@pytest.mark.asyncio
async def test_async_agent_group_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=GROUP_URL, method="delete")
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.groups.delete(GROUP_ID) is None


@pytest.mark.asyncio
async def test_async_agent_group_get(httpx_mock: HTTPXMock, group_json, group):
    httpx_mock.add_response(
        url=BASE_URL,
        method="get",
        json={"groups": [group_json]},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.groups.get() == [group]


@pytest.mark.asyncio
async def test_async_agent_group_details(httpx_mock: HTTPXMock, group_json, group):
    httpx_mock.add_response(url=GROUP_URL, method="get", json=group_json)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.groups.details(GROUP_ID) == group


@pytest.mark.asyncio
async def test_async_agent_group_add(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_ID}",
        method="put",
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.groups.add(GROUP_ID, AGENT_ID) is None


@pytest.mark.asyncio
async def test_async_agent_group_remove(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_ID}",
        method="delete",
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.agents.groups.remove(GROUP_ID, AGENT_ID) is None


def test_agent_group_model_add_agent(httpx_mock: HTTPXMock, group_json):
    httpx_mock.add_response(url=GROUP_URL, method="get", json=group_json)
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_UUID}",
        method="put",
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    group = cloud.platform.agents.groups.details(GROUP_ID)
    assert group.add_agent(AGENT_UUID) is None


def test_agent_group_model_remove_agent(httpx_mock: HTTPXMock, group_json):
    httpx_mock.add_response(url=GROUP_URL, method="get", json=group_json)
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_UUID}",
        method="delete",
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    group = cloud.platform.agents.groups.details(GROUP_ID)
    assert group.remove_agent(AGENT_UUID) is None


@pytest.mark.asyncio
async def test_async_agent_group_model_add_agent(httpx_mock: HTTPXMock, group_json):
    httpx_mock.add_response(url=GROUP_URL, method="get", json=group_json)
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_UUID}",
        method="put",
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    group = await cloud.platform.agents.groups.details(GROUP_ID)
    assert await group.async_add_agent(AGENT_UUID) is None


@pytest.mark.asyncio
async def test_async_agent_group_model_remove_agent(httpx_mock: HTTPXMock, group_json):
    httpx_mock.add_response(url=GROUP_URL, method="get", json=group_json)
    httpx_mock.add_response(
        url=f"{GROUP_URL}/agents/{AGENT_UUID}",
        method="delete",
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    group = await cloud.platform.agents.groups.details(GROUP_ID)
    assert await group.async_remove_agent(AGENT_UUID) is None
