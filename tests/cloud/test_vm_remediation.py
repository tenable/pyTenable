from datetime import date, datetime, timezone
from typing import Any

import pytest
from pydantic import ValidationError
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.vm.models.remediation import (
    RemediationDueDate,
    RemediationGoal,
    RemediationGoalRequest,
    RemediationProject,
    RemediationProjectRequest,
    RemediationSearchRequest,
    RemediationSort,
)
from tenable.errors import TenableCloudAPIError

BASE_URL = "https://cloud.tenable.com/remediation"
GOAL_URL = f"{BASE_URL}/goal"
PROJECT_UUID = "7c41e8a9-3b62-4d05-9f18-2ae6b407d3c1"
GOAL_UUID = "e2a95c73-8d14-4f60-b3a7-16c8d5029e4b"
FINDING_FILTERS = {
    "and": [
        {"id": "severity", "label": "Severity", "operator": "eq", "value": "critical"}
    ]
}
FINDING_FILTERS_STR = (
    '{"and": [{"id": "severity", "label": "Severity", "operator": "eq", '
    '"value": "critical"}]}'
)


@pytest.fixture
def project_json() -> dict[str, Any]:
    return {
        "projectuuid": PROJECT_UUID,
        "containeruuid": "4b8f1d62-05c9-47a3-8e21-9df3a6c15870",
        "useruuid": "a1d73b58-6e2f-4c91-b047-38e5c9a26f14",
        "name": "Critical patching",
        "description": "Remediate critical findings on the production assets.",
        "type": "Static",
        "status": "OPEN",
        "progress": "0",
        "startdate": 1695647147,
        "projectduedate": {"name": "withinNumberOfDays", "value": "30"},
        "assignee": ["user@example.com"],
        "assetfilters": "all",
        "findingfilters": (
            '{"and":[{"id":"severity","label":"Severity","operator":"eq",'
            '"value":"critical"}]}'
        ),
        "create_tstamp": 1695647369307,
        "update_tstamp": 1697462682738,
    }


@pytest.fixture
def goal_json() -> dict[str, Any]:
    return {
        "goaluuid": GOAL_UUID,
        "containeruuid": "4b8f1d62-05c9-47a3-8e21-9df3a6c15870",
        "useruuid": "a1d73b58-6e2f-4c91-b047-38e5c9a26f14",
        "name": "Reduce critical findings",
        "description": "Remediate 80 percent of critical findings.",
        "type": "Static",
        "status": "ACTIVE",
        "progress": '{"fixed": 4, "open": 1}',
        "startdate": 1741192999,
        "duedate": 1741193119,
        "goalduedate": {"name": "byFixedDate", "value": "2026-03-27T00:00:00Z"},
        "goalresult": "Does not meet",
        "minimumpercentage": "80",
        "conditions": "[]",
        "dashboards": [],
        "assetfilters": "all",
        "findingfilters": '{"and":[]}',
        "create_tstamp": 1741193059787,
        "update_tstamp": 1741193059787,
    }


def test_project_model(project_json):
    project = RemediationProject.model_validate(project_json)
    assert str(project.id) == PROJECT_UUID
    assert project.start_date == datetime(2023, 9, 25, 13, 5, 47, tzinfo=timezone.utc)
    assert project.created_at == datetime(
        2023, 9, 25, 13, 9, 29, 307000, tzinfo=timezone.utc
    )
    assert project.finding_filters == FINDING_FILTERS
    assert project.asset_filters == "all"
    assert project.due_date == RemediationDueDate(name="withinNumberOfDays", value="30")
    assert project.assignees == ["user@example.com"]


def test_goal_model(goal_json):
    goal = RemediationGoal.model_validate(goal_json)
    assert str(goal.id) == GOAL_UUID
    assert goal.due_at == datetime(2025, 3, 5, 16, 45, 19, tzinfo=timezone.utc)
    assert goal.progress == {"fixed": 4, "open": 1}
    assert goal.minimum_percentage == 80
    assert goal.conditions == []
    assert goal.goal_result == "Does not meet"


@pytest.mark.parametrize(
    "value,expected",
    [
        (30, {"name": "withinNumberOfDays", "value": "30"}),
        (date(2026, 3, 27), {"name": "byFixedDate", "value": "2026-03-27T00:00:00Z"}),
        (
            datetime(2026, 3, 27, 12, tzinfo=timezone.utc),
            {"name": "byFixedDate", "value": "2026-03-27T12:00:00Z"},
        ),
        ("ongoing", {"name": "ongoing"}),
        (
            {"name": "withinNumberOfDays", "value": 14},
            {"name": "withinNumberOfDays", "value": "14"},
        ),
        (
            RemediationDueDate(name="byFixedDate", value="2026-01-01T00:00:00Z"),
            {"name": "byFixedDate", "value": "2026-01-01T00:00:00Z"},
        ),
    ],
)
def test_due_date_model(value, expected):
    assert (
        RemediationDueDate.model_validate(value).model_dump(exclude_none=True)
        == expected
    )


def test_due_date_model_fail():
    with pytest.raises(ValidationError):
        RemediationDueDate.model_validate(True)
    with pytest.raises(ValidationError):
        RemediationDueDate.model_validate("someday")


def test_sort_model():
    assert RemediationSort.model_validate("name:asc").model_dump() == {
        "property": "name",
        "order": "asc",
    }
    assert RemediationSort.model_validate(("status", "desc")).model_dump() == {
        "property": "status",
        "order": "desc",
    }
    assert RemediationSort.model_validate(
        {"property": "name", "order": "desc"}
    ) == RemediationSort(property="name", order="desc")
    with pytest.raises(ValidationError):
        RemediationSort.model_validate("name-asc")
    with pytest.raises(ValidationError):
        RemediationSort.model_validate("name:up")


def test_search_request_model():
    query = RemediationSearchRequest.model_validate(
        {
            "filter": {"status": "ACTIVE"},
            "sort": ["name:asc"],
            "fields": ["name", "status"],
            "findings_type": "vm",
            "limit": 50,
        }
    )
    assert query.model_dump(mode="json", exclude_none=True) == {
        "filter": {"status": "ACTIVE"},
        "sort": [{"property": "name", "order": "asc"}],
        "fields": "name,status",
        "findingsType": "vm",
        "limit": 50,
    }
    with pytest.raises(ValidationError):
        RemediationSearchRequest(limit=0)


def test_project_request_model():
    req = RemediationProjectRequest.model_validate(
        {
            "name": "Critical patching",
            "start_date": 1695647147,
            "asset_filters": "all",
            "finding_filters": FINDING_FILTERS,
            "due_date": 30,
            "assignees": ["user@example.com"],
        }
    )
    assert req.model_dump(mode="json", exclude_none=True) == {
        "name": "Critical patching",
        "startdate": 1695647147,
        "assetfilters": "all",
        "findingfilters": FINDING_FILTERS_STR,
        "projectduedate": {"name": "withinNumberOfDays", "value": "30"},
        "assignee": ["user@example.com"],
    }
    with pytest.raises(ValidationError):
        RemediationProjectRequest.model_validate({"name": "x", "due_date": "ongoing"})


def test_goal_request_model():
    req = RemediationGoalRequest.model_validate(
        {"name": "Goal", "minimum_percentage": 80, "conditions": []}
    )
    assert req.model_dump(mode="json", exclude_none=True) == {
        "name": "Goal",
        "minimumpercentage": "80",
        "conditions": "[]",
    }
    with pytest.raises(ValidationError):
        RemediationGoalRequest.model_validate({"name": "x", "minimum_percentage": 101})


def test_projects_get(httpx_mock: HTTPXMock, project_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/search",
        method="POST",
        match_json={"limit": 2, "sort": [{"property": "name", "order": "asc"}]},
        json={
            "remediations": [project_json, project_json],
            "pagination": {"next": "A", "total": 3},
        },
    )
    httpx_mock.add_response(
        url=f"{BASE_URL}/search",
        method="POST",
        match_json={
            "limit": 2,
            "sort": [{"property": "name", "order": "asc"}],
            "next": "A",
        },
        json={"remediations": [project_json], "pagination": {"total": 3}},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    projects = cloud.vm.remediation.projects(sort=["name:asc"], limit=2)
    expected = RemediationProject.model_validate(project_json)
    for project in projects:
        assert project == expected
    assert projects.count == 3
    assert projects.total == 3
    assert projects.num_pages == 2


def test_projects_get_no_total(httpx_mock: HTTPXMock, project_json):
    # Without a total or a next token, the iterator must stop after the first page.
    httpx_mock.add_response(
        url=f"{BASE_URL}/search",
        method="POST",
        match_json={"limit": 100},
        json={"remediations": [project_json], "pagination": {}},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert len(list(cloud.vm.remediation.projects())) == 1


def test_projects_details(httpx_mock: HTTPXMock, project_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/{PROJECT_UUID}?findingsType=vm", json=[project_json]
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    project = cloud.vm.remediation.project_detail(PROJECT_UUID, findings_type="vm")
    assert project == RemediationProject.model_validate(project_json)


def test_projects_details_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=f"{BASE_URL}/{PROJECT_UUID}", status_code=404)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    with pytest.raises(TenableCloudAPIError):
        cloud.vm.remediation.project_detail(PROJECT_UUID)


def test_projects_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=BASE_URL,
        method="POST",
        status_code=201,
        match_json={
            "name": "Critical patching",
            "type": "Static",
            "status": "OPEN",
            "startdate": 1695647147,
            "assetfilters": "all",
            "findingfilters": FINDING_FILTERS_STR,
            "projectduedate": {"name": "withinNumberOfDays", "value": "30"},
            "assignee": ["user@example.com"],
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert (
        cloud.vm.remediation.project_create(
            "Critical patching",
            type="Static",
            status="OPEN",
            start_date=datetime.fromtimestamp(1695647147, tz=timezone.utc),
            asset_filters="all",
            finding_filters=FINDING_FILTERS,
            due_date=30,
            assignees=["user@example.com"],
        )
        is None
    )


def test_projects_create_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=BASE_URL, method="POST", status_code=400)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    with pytest.raises(TenableCloudAPIError):
        cloud.vm.remediation.project_create("Critical patching")


def test_projects_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{BASE_URL}/{PROJECT_UUID}",
        method="PUT",
        match_json={"name": "Critical patching", "status": "SUSPENDED"},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    cloud.vm.remediation.project_update(
        PROJECT_UUID, "Critical patching", status="SUSPENDED"
    )


def test_projects_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=BASE_URL,
        method="PATCH",
        match_json={"operation": "remove", "projectuuids": [PROJECT_UUID]},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    cloud.vm.remediation.project_delete(PROJECT_UUID)
    with pytest.raises(ValidationError):
        cloud.vm.remediation.project_delete()


def test_goals_get(httpx_mock: HTTPXMock, goal_json):
    httpx_mock.add_response(
        url=f"{GOAL_URL}/search",
        method="POST",
        match_json={"limit": 1, "filter": {"status": "ACTIVE"}},
        json={"goals": [goal_json], "pagination": {"next": "A", "total": 2}},
    )
    httpx_mock.add_response(
        url=f"{GOAL_URL}/search",
        method="POST",
        match_json={"limit": 1, "filter": {"status": "ACTIVE"}, "next": "A"},
        json={"goals": [goal_json], "pagination": {"total": 2}},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    goals = cloud.vm.remediation.goals(filters={"status": "ACTIVE"}, limit=1)
    expected = RemediationGoal.model_validate(goal_json)
    assert list(goals) == [expected, expected]
    assert goals.total == 2


def test_goals_details(httpx_mock: HTTPXMock, goal_json):
    httpx_mock.add_response(url=f"{GOAL_URL}/{GOAL_UUID}", json=[goal_json])
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    goal = cloud.vm.remediation.goal_detail(GOAL_UUID)
    assert goal == RemediationGoal.model_validate(goal_json)


def test_goals_create(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=GOAL_URL,
        method="POST",
        status_code=201,
        match_json={
            "name": "Reduce critical findings",
            "assetfilters": "all",
            "goalduedate": {"name": "byFixedDate", "value": "2026-03-27T00:00:00Z"},
            "minimumpercentage": "80",
            "conditions": "[]",
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    cloud.vm.remediation.goal_create(
        "Reduce critical findings",
        asset_filters="all",
        due_date=date(2026, 3, 27),
        minimum_percentage=80,
        conditions=[],
    )


def test_goals_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{GOAL_URL}/{GOAL_UUID}",
        method="PUT",
        match_json={
            "name": "Reduce critical findings",
            "goalduedate": {"name": "ongoing"},
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    cloud.vm.remediation.goal_update(
        GOAL_UUID, "Reduce critical findings", due_date="ongoing"
    )


def test_goals_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=GOAL_URL,
        method="PATCH",
        match_json={"operation": "remove", "goaluuids": [GOAL_UUID, PROJECT_UUID]},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    cloud.vm.remediation.goal_delete(GOAL_UUID, PROJECT_UUID)


@pytest.mark.asyncio
async def test_async_projects(httpx_mock: HTTPXMock, project_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/search",
        method="POST",
        match_json={"limit": 1},
        json={"remediations": [project_json], "pagination": {"next": "A", "total": 2}},
    )
    httpx_mock.add_response(
        url=f"{BASE_URL}/search",
        method="POST",
        match_json={"limit": 1, "next": "A"},
        json={"remediations": [project_json], "pagination": {"total": 2}},
    )
    httpx_mock.add_response(url=f"{BASE_URL}/{PROJECT_UUID}", json=[project_json])
    httpx_mock.add_response(
        url=BASE_URL,
        method="POST",
        status_code=201,
        match_json={"name": "Project"},
    )
    httpx_mock.add_response(
        url=f"{BASE_URL}/{PROJECT_UUID}", method="PUT", match_json={"name": "Project"}
    )
    httpx_mock.add_response(
        url=BASE_URL,
        method="PATCH",
        match_json={"operation": "remove", "projectuuids": [PROJECT_UUID]},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    expected = RemediationProject.model_validate(project_json)
    projects = await cloud.vm.remediation.projects(limit=1)
    assert [p async for p in projects] == [expected, expected]
    assert projects.num_pages == 2
    assert await cloud.vm.remediation.project_detail(PROJECT_UUID) == expected
    await cloud.vm.remediation.project_create("Project")
    await cloud.vm.remediation.project_update(PROJECT_UUID, "Project")
    await cloud.vm.remediation.project_delete(PROJECT_UUID)


@pytest.mark.asyncio
async def test_async_projects_no_total(httpx_mock: HTTPXMock, project_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/search",
        method="POST",
        json={"remediations": [project_json], "pagination": {}},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert len([p async for p in await cloud.vm.remediation.projects()]) == 1


@pytest.mark.asyncio
async def test_async_goals(httpx_mock: HTTPXMock, goal_json):
    httpx_mock.add_response(
        url=f"{GOAL_URL}/search",
        method="POST",
        match_json={"limit": 100},
        json={"goals": [goal_json], "pagination": {"total": 1}},
    )
    httpx_mock.add_response(url=f"{GOAL_URL}/{GOAL_UUID}", json=[goal_json])
    httpx_mock.add_response(
        url=GOAL_URL,
        method="POST",
        status_code=201,
        match_json={"name": "Goal", "goalduedate": {"name": "ongoing"}},
    )
    httpx_mock.add_response(
        url=f"{GOAL_URL}/{GOAL_UUID}", method="PUT", match_json={"name": "Goal"}
    )
    httpx_mock.add_response(
        url=GOAL_URL,
        method="PATCH",
        match_json={"operation": "remove", "goaluuids": [GOAL_UUID]},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    expected = RemediationGoal.model_validate(goal_json)
    assert [g async for g in await cloud.vm.remediation.goals()] == [expected]
    assert await cloud.vm.remediation.goal_detail(GOAL_UUID) == expected
    await cloud.vm.remediation.goal_create("Goal", due_date="ongoing")
    await cloud.vm.remediation.goal_update(GOAL_UUID, "Goal")
    await cloud.vm.remediation.goal_delete(GOAL_UUID)
