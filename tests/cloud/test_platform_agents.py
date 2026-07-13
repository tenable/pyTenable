from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.agents import (
    Agent,
    AgentDetail,
    AgentFilter,
    AgentQueryParams,
)


@pytest.fixture
def agent_json() -> dict[str, Any]:
    return {
        "id": 9176838,
        "uuid": "655993d5-c131-46e8-a82f-957f6f894cac",
        "name": "GRD-LPTP",
        "platform": "WINDOWS",
        "distro": "win-x86-64",
        "ip": "192.0.2.57",
        "last_scanned": 1515620036,
        "plugin_feed_id": "201801081515",
        "core_build": "106",
        "core_version": "7.0.0",
        "linked_on": 1456775443,
        "last_connect": 1515674073,
        "status": "off",
        "groups": [
            {"name": "CodyAgents", "id": 8},
            {"name": "Agent Group A", "id": 3316},
        ],
        "supports_remote_logs": False,
        "network_uuid": "00000000-0000-0000-0000-000000000000",
        "network_name": "Default",
        "profile_uuid": "00000000-0000-0000-0000-000000000000",
        "profile_name": "Default",
        "supports_remote_settings": True,
        "health": 0,
        "health_state_name": "HEALTHY",
        "fredi_status": True,
    }


@pytest.fixture
def agent_details_json(agent_json) -> dict[str, Any]:
    return {
        **agent_json,
        "remote_settings": [
            {
                "name": "Nessus Agent Log Level",
                "setting": "backend_log_level",
                "type": "select",
                "description": "This controls the Nessus Agent backend logging level.",
                "backend_reload": True,
                "status": "current",
                "value": "verbose",
                "allowable_values": [
                    {"value": "verbose"},
                    {"value": "debug"},
                    {"value": "normal"},
                ],
                "default": "normal",
            }
        ],
        "restart_pending": False,
        "health_events": [
            {
                "identifier": 201,
                "state": 0,
                "state_time": 1722960875000,
                "details": "Plugin update was successful.",
                "muted": False,
                "state_name": "HEALTHY",
                "identifier_name": "PLUGIN_UPDATE",
            }
        ],
    }


@pytest.fixture
def agent(agent_json) -> Agent:
    return Agent.model_validate(agent_json)


@pytest.fixture
def agent_details(agent_details_json) -> AgentDetail:
    return AgentDetail.model_validate(agent_details_json)


def test_agent_filter_model():
    assert AgentFilter(field="name", operator="match", value="test").model_dump() == (
        "name:match:test"
    )
    assert AgentFilter.model_validate("name:match:test").model_dump() == (
        "name:match:test"
    )
    assert AgentFilter.model_validate(("name", "match", "test")).model_dump() == (
        "name:match:test"
    )


def test_agent_filter_fail():
    with pytest.raises(ValueError):
        AgentFilter.model_validate("name-match-test")


def test_agent_query_params():
    params = AgentQueryParams.model_validate(
        {
            "filters": [("name", "match", "test"), "platform:eq:WINDOWS"],
            "filter_type": "and",
            "limit": 100,
            "sort": "name:asc",
        }
    )
    dumped = params.model_dump(exclude_none=True)
    assert dumped == {
        "f": ["name:match:test", "platform:eq:WINDOWS"],
        "ft": "and",
        "limit": 100,
        "sort": "name:asc",
    }


def _pagination(total: int, limit: int, offset: int) -> dict[str, Any]:
    return {"total": total, "limit": limit, "offset": offset}


def test_agents_list(httpx_mock: HTTPXMock, agent_json, agent):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents?limit=50",
        json={
            "agents": [agent_json for _ in range(50)],
            "pagination": _pagination(total=120, limit=50, offset=0),
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents?limit=50&offset=50",
        json={
            "agents": [agent_json for _ in range(50)],
            "pagination": _pagination(total=120, limit=50, offset=50),
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents?limit=50&offset=100",
        json={
            "agents": [agent_json for _ in range(20)],
            "pagination": _pagination(total=120, limit=50, offset=100),
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    it = cloud.platform.agents.get()
    for item in it:
        assert item == agent
    assert it.count == 120
    assert it.total == 120


def test_agents_list_by_group(httpx_mock: HTTPXMock, agent_json, agent):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agent-groups/42/agents?limit=50",
        json={
            "agents": [agent_json for _ in range(3)],
            "pagination": _pagination(total=3, limit=50, offset=0),
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    it = cloud.platform.agents.get(group_id=42)
    for item in it:
        assert item == agent
    assert it.count == 3
    assert it.total == 3


def test_agents_list_with_filters(httpx_mock: HTTPXMock, agent_json):
    httpx_mock.add_response(
        url=(
            "https://cloud.tenable.com/scanners/null/agents"
            "?f=platform%3Aeq%3AWINDOWS&ft=and&limit=100&sort=name%3Aasc"
        ),
        json={
            "agents": [agent_json],
            "pagination": _pagination(total=1, limit=100, offset=0),
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    it = cloud.platform.agents.get(
        filters=[("platform", "eq", "WINDOWS")],
        filter_type="and",
        limit=100,
        sort="name:asc",
    )
    assert next(it) == AgentListItem.model_validate(agent_json)


def test_agents_get(httpx_mock: HTTPXMock, agent_details_json, agent_details):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/9176838",
        json=agent_details_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.details(9176838)
    assert resp == agent_details


def test_agents_rename(httpx_mock: HTTPXMock, agent_details_json):
    renamed = {**agent_details_json, "name": "NEW-NAME"}
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/9176838",
        method="patch",
        match_json={"name": "NEW-NAME"},
        json=renamed,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.rename(9176838, "NEW-NAME")
    assert resp == AgentDetails.model_validate(renamed)


def test_agents_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/9176838",
        method="delete",
        json={},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    cloud.platform.agents.delete(9176838)


@pytest.mark.asyncio
async def test_async_agents_list(httpx_mock: HTTPXMock, agent_json, agent):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents?limit=50",
        json={
            "agents": [agent_json for _ in range(50)],
            "pagination": _pagination(total=70, limit=50, offset=0),
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents?limit=50&offset=50",
        json={
            "agents": [agent_json for _ in range(20)],
            "pagination": _pagination(total=70, limit=50, offset=50),
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    it = await cloud.platform.agents.list()
    async for item in it:
        assert item == agent
    assert it.count == 70
    assert it.total == 70


@pytest.mark.asyncio
async def test_async_agents_list_by_group(httpx_mock: HTTPXMock, agent_json, agent):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agent-groups/7/agents?limit=50",
        json={
            "agents": [agent_json for _ in range(2)],
            "pagination": _pagination(total=2, limit=50, offset=0),
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    it = await cloud.platform.agents.list(group_id=7)
    async for item in it:
        assert item == agent
    assert it.count == 2


@pytest.mark.asyncio
async def test_async_agents_get(
    httpx_mock: HTTPXMock, agent_details_json, agent_details
):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/9176838",
        json=agent_details_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.get(9176838)
    assert resp == agent_details


@pytest.mark.asyncio
async def test_async_agents_rename(httpx_mock: HTTPXMock, agent_details_json):
    renamed = {**agent_details_json, "name": "NEW-NAME"}
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/9176838",
        method="patch",
        match_json={"name": "NEW-NAME"},
        json=renamed,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.rename(9176838, "NEW-NAME")
    assert resp == AgentDetails.model_validate(renamed)


@pytest.mark.asyncio
async def test_async_agents_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/9176838",
        method="delete",
        json={},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    await cloud.platform.agents.delete(9176838)
