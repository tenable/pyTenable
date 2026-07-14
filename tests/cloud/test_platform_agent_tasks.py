from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.agents import (
    AgentDirective,
    AgentTask,
    DirectiveOptions,
    DirectiveSettingItem,
)

TASK_UUID = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
GROUP_ID = 42
NETWORK_UUID = "11111111-2222-3333-4444-555555555555"
PROFILE_UUID = "66666666-7777-8888-9999-aaaaaaaaaaaa"


@pytest.fixture
def task_json() -> dict[str, Any]:
    return {
        "task_id": TASK_UUID,
        "container_uuid": "00000000-0000-0000-0000-000000000001",
        "status": "NEW",
        "message": "Task created",
        "start_time": 1700000000000,
        "end_time": 1700000001000,
        "last_update_time": 1700000000500,
        "total_work_units": 100,
        "total_work_units_completed": 0,
        "completion_percentage": 0,
    }


@pytest.fixture
def task(task_json) -> AgentTask:
    return AgentTask.model_validate(task_json)


# ---------- task_status ----------


def test_task_status(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/scanners/null/agents/_bulk/{TASK_UUID}",
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.task_status(TASK_UUID)
    assert resp == task


def test_group_task_status(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/{TASK_UUID}"
        ),
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.group_task_status(GROUP_ID, TASK_UUID)
    assert resp == task


# ---------- add_to_group ----------


def test_add_to_group(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/add"
        ),
        method="post",
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.add_to_group(GROUP_ID)
    assert resp == task


def test_add_to_group_with_items(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/add"
        ),
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
            "items": [1, 2, 3],
            "not_items": [4],
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.add_to_group(
        GROUP_ID, items=[1, 2, 3], not_items=[4]
    )
    assert resp == task


# ---------- remove_from_group ----------


def test_remove_from_group(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/remove"
        ),
        method="post",
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.remove_from_group(GROUP_ID)
    assert resp == task


# ---------- add_to_network ----------


def test_add_to_network(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/addToNetwork",
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
            "network_uuid": NETWORK_UUID,
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.add_to_network(NETWORK_UUID)
    assert resp == task


# ---------- remove_from_network ----------


def test_remove_from_network(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/removeFromNetwork",
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
            "network_uuid": NETWORK_UUID,
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.remove_from_network(NETWORK_UUID)
    assert resp == task


# ---------- assign_to_profile ----------


def test_assign_to_profile(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/assignToProfile",
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
            "profile_uuid": PROFILE_UUID,
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.assign_to_profile(PROFILE_UUID)
    assert resp == task


def test_remove_from_profile(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/assignToProfile",
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.assign_to_profile()
    assert resp == task


# ---------- send_directive ----------


def test_send_directive_restart(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/directive",
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
            "directive": {
                "type": "restart",
                "options": {"hard": True, "idle": False},
            },
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    directive = AgentDirective(
        type="restart", options=DirectiveOptions(hard=True, idle=False)
    )
    resp = cloud.platform.agents.tasks.send_directive(directive)
    assert resp == task


def test_send_directive_settings(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/directive",
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
            "directive": {
                "type": "settings",
                "options": {
                    "settings": [{"setting": "backend_log_level", "value": "debug"}]
                },
            },
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    directive = AgentDirective(
        type="settings",
        options=DirectiveOptions(
            settings=[DirectiveSettingItem(setting="backend_log_level", value="debug")]
        ),
    )
    resp = cloud.platform.agents.tasks.send_directive(directive)
    assert resp == task


# ---------- send_group_directive ----------


def test_send_group_directive(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/directive"
        ),
        method="post",
        match_json={
            "criteria": {"all_agents": True, "filter_type": "and"},
            "directive": {"type": "restart"},
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    directive = AgentDirective(type="restart")
    resp = cloud.platform.agents.tasks.send_group_directive(GROUP_ID, directive)
    assert resp == task


# ---------- unlink_many ----------


def test_unlink_many(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/unlink",
        method="post",
        match_json={"criteria": {"all_agents": True, "filter_type": "and"}},
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.unlink_many()
    assert resp == task


def test_unlink_many_with_filters(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/unlink",
        method="post",
        match_json={
            "criteria": {
                "all_agents": True,
                "filters": ["platform:eq:WINDOWS"],
                "filter_type": "and",
            }
        },
        json=task_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.agents.tasks.unlink_many(
        filters=[("platform", "eq", "WINDOWS")]
    )
    assert resp == task


# ---------- async variants ----------


@pytest.mark.asyncio
async def test_async_task_status(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=f"https://cloud.tenable.com/scanners/null/agents/_bulk/{TASK_UUID}",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.task_status(TASK_UUID)
    assert resp == task


@pytest.mark.asyncio
async def test_async_group_task_status(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/{TASK_UUID}"
        ),
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.group_task_status(GROUP_ID, TASK_UUID)
    assert resp == task


@pytest.mark.asyncio
async def test_async_add_to_group(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/add"
        ),
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.add_to_group(GROUP_ID)
    assert resp == task


@pytest.mark.asyncio
async def test_async_remove_from_group(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/remove"
        ),
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.remove_from_group(GROUP_ID)
    assert resp == task


@pytest.mark.asyncio
async def test_async_add_to_network(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/addToNetwork",
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.add_to_network(NETWORK_UUID)
    assert resp == task


@pytest.mark.asyncio
async def test_async_remove_from_network(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/removeFromNetwork",
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.remove_from_network(NETWORK_UUID)
    assert resp == task


@pytest.mark.asyncio
async def test_async_assign_to_profile(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/assignToProfile",
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.assign_to_profile(PROFILE_UUID)
    assert resp == task


@pytest.mark.asyncio
async def test_async_send_directive(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/directive",
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    directive = AgentDirective(
        type="restart", options=DirectiveOptions(hard=True, idle=False)
    )
    resp = await cloud.platform.agents.tasks.send_directive(directive)
    assert resp == task


@pytest.mark.asyncio
async def test_async_send_group_directive(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url=(
            f"https://cloud.tenable.com/scanners/null/agent-groups"
            f"/{GROUP_ID}/agents/_bulk/directive"
        ),
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    directive = AgentDirective(type="restart")
    resp = await cloud.platform.agents.tasks.send_group_directive(GROUP_ID, directive)
    assert resp == task


@pytest.mark.asyncio
async def test_async_unlink_many(httpx_mock: HTTPXMock, task_json, task):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/scanners/null/agents/_bulk/unlink",
        method="post",
        json=task_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.agents.tasks.unlink_many()
    assert resp == task
