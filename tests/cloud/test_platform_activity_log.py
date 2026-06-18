from typing import Any

import pytest
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.activity_log import (
    ActivityLogEvent,
    ActivityLogFilter,
    ActivityLogQueryParams,
    ActivityLogSort,
)


@pytest.fixture
def ejson() -> dict[str, Any]:
    return {
        "id": "a4e9177aa45c48c9d46a2f24c5f97b24",
        "action": "user.authenticate.password",
        "crud": "u",
        "is_failure": True,
        "received": "2018-12-31T23:09:40Z",
        "description": None,
        "actor": {
            "id": "da1499fd-afdb-4fb9-bfb6-9defec2f0f09",
            "name": "user2@example.com",
        },
        "is_anonymous": None,
        "target": {
            "id": "da1499fd-afdb-4fb9-bfb6-9defec2f0f09",
            "name": "user2@example.com",
            "type": "User",
        },
        "fields": [
            {"key": "message", "value": "Invalid credentials."},
            {"key": "sessionToken", "value": "-"},
            {"key": "X-Forwarded-For", "value": "192.0.2.57, 192.0.2.57"},
            {
                "key": "X-Request-Uuid",
                "value": "71a6630e83148694260ad838ddff5dce:dd19f39e7ec84ba80dec:8d7f958f8c3b770767af",
            },
        ],
    }


@pytest.fixture
def event(ejson) -> ActivityLogEvent:
    return ActivityLogEvent.model_validate(ejson)


def test_activity_log_filter_model():
    assert (
        ActivityLogFilter(field="something", operator="eq", value="value").model_dump()
        == "something.eq:value"
    )
    assert (
        ActivityLogFilter.model_validate("something.eq:value").model_dump()
        == "something.eq:value"
    )
    assert (
        ActivityLogFilter.model_validate(("something", "eq", "value")).model_dump()
        == "something.eq:value"
    )


def test_activity_log_filter_fail():
    with pytest.raises(ValueError):
        ActivityLogFilter.model_validate("field.eq-something")

    with pytest.raises(ValueError):
        ActivityLogFilter.model_validate("field-eq:something")


def test_activity_log_sort_model():
    assert ActivityLogSort(field="field", direction="asc").model_dump() == "field:asc"
    assert ActivityLogSort.model_validate("field:asc").model_dump() == "field:asc"
    assert ActivityLogSort.model_validate(("field", "asc")).model_dump() == "field:asc"


def test_activity_log_sort_fail():
    with pytest.raises(ValueError):
        ActivityLogSort.model_validate("field-asc")


def test_activity_log_params():
    assert ActivityLogQueryParams(
        filters=["field.eq:value", ("field2", "gt", "value")],
        filter_type="and",
        limit=200,
    ).model_dump() == {
        "f": ["field.eq:value", "field2.gt:value"],
        "ft": "and",
        "limit": 200,
        "next": None,
        "sort": None,
    }


def test_activity_log(httpx_mock: HTTPXMock, ejson, event):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/audit-log/v1/events?limit=500",
        json={
            "events": [ejson for _ in range(500)],
            "pagination": {
                "offset": 0,
                "limit": 500,
                "count": 500,
                "total": 1100,
                "next": "A",
            },
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/audit-log/v1/events?limit=500&next=A",
        json={
            "events": [ejson for _ in range(500)],
            "pagination": {
                "offset": 500,
                "limit": 500,
                "count": 500,
                "total": 1100,
                "next": "B",
            },
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/audit-log/v1/events?limit=500&next=B",
        json={
            "events": [ejson for _ in range(100)],
            "pagination": {
                "offset": 1000,
                "limit": 500,
                "count": 100,
                "total": 1100,
            },
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    iter = cloud.platform.activity_log.get()
    for i in iter:
        assert i == event
    assert iter.count == 1100
    assert iter.total == 1100


@pytest.mark.asyncio
async def test_async_activity_log(httpx_mock: HTTPXMock, ejson, event):
    httpx_mock.add_response(
        url="https://cloud.tenable.com/audit-log/v1/events?limit=500",
        json={
            "events": [ejson for _ in range(500)],
            "pagination": {
                "offset": 0,
                "limit": 500,
                "count": 500,
                "total": 1100,
                "next": "A",
            },
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/audit-log/v1/events?limit=500&next=A",
        json={
            "events": [ejson for _ in range(500)],
            "pagination": {
                "offset": 500,
                "limit": 500,
                "count": 500,
                "total": 1100,
                "next": "B",
            },
        },
    )
    httpx_mock.add_response(
        url="https://cloud.tenable.com/audit-log/v1/events?limit=500&next=B",
        json={
            "events": [ejson for _ in range(100)],
            "pagination": {
                "offset": 1000,
                "limit": 500,
                "count": 100,
                "total": 1100,
            },
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    iter = await cloud.platform.activity_log.get()
    async for i in iter:
        assert i == event
    assert iter.count == 1100
    assert iter.total == 1100
