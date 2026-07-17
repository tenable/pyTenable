from typing import Any
from uuid import UUID

import pytest
from pydantic import TypeAdapter
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.platform.models.connectors import (
    AWSKeyedConnector,
    AWSKeyedConnectorParams,
    Connector,
    ConnectorSchedule,
    ConnectorTrail,
)

CONN_ID = "6d75a992-0727-4d84-aa5f-ebae0185868b"
LIST_URL = "https://cloud.tenable.com/settings/connectors"
DETAIL_URL = f"{LIST_URL}/{CONN_ID}"

TRAIL_JSON = {
    "arn": "arn:aws:cloudtrail:us-east-1:069647819620:trail/ExampleAWSTrail",
    "name": "ExampleAWSTrail",
    "region": {"name": "All", "friendly_name": "All"},
    "availability": "success",
}


def _pagination(total: int, limit: int, offset: int) -> dict[str, Any]:
    return {"total": total, "limit": limit, "offset": offset, "sort": []}


@pytest.fixture
def connector_json() -> dict[str, Any]:
    return {
        "type": "aws",
        "human_type": "AWS",
        "data_type": "assets",
        "name": "AWS Connector - Keyed",
        "status": "Scheduled",
        "status_message": "",
        "schedule": {"units": "days", "value": 1},
        "date_created": "2019-12-31T20:50:23.635Z",
        "date_modified": "2020-01-01T10:00:00.000Z",
        "id": CONN_ID,
        "container_uuid": "154a05bd-3f27-495a-a001-a659c24eb1a4",
        "expired": False,
        "incremental_mode": False,
        "params": {
            "access_key": "AJIAJLRNVRLZRDZLVBXR",
            "secret_key": "REDACTED",
            "trails": [TRAIL_JSON],
        },
        "network_uuid": "2825e3c9-16be-41f4-8b83-dfe534d10627",
    }


@pytest.fixture
def connector(connector_json) -> Connector:
    return TypeAdapter(Connector).validate_python(connector_json)


def _update_connector() -> AWSKeyedConnector:
    return AWSKeyedConnector(
        name="Renamed",
        network_uuid=UUID("2825e3c9-16be-41f4-8b83-dfe534d10627"),
        schedule=ConnectorSchedule(units="days", value=1),
        params=AWSKeyedConnectorParams(
            access_key="AJIAJLRNVRLZRDZLVBXR",
            secret_key="SECRET",
            trails=[ConnectorTrail.model_validate(TRAIL_JSON)],
        ),
    )


def _update_match_json() -> dict[str, Any]:
    return {
        "connector": {
            "name": "Renamed",
            "type": "aws",
            "network_uuid": "2825e3c9-16be-41f4-8b83-dfe534d10627",
            "schedule": {"units": "days", "value": 1},
            "params": {
                "access_key": "AJIAJLRNVRLZRDZLVBXR",
                "secret_key": "SECRET",
                "trails": [TRAIL_JSON],
            },
        }
    }


def _create_match_json() -> dict[str, Any]:
    return {
        "connector": {
            "name": "AWS Connector - Keyed",
            "type": "aws",
            "params": {
                "access_key": "AJIAJLRNVRLZRDZLVBXR",
                "secret_key": "SECRET",
            },
        }
    }


def _create_payload() -> AWSKeyedConnector:
    return AWSKeyedConnector(
        name="AWS Connector - Keyed",
        params=AWSKeyedConnectorParams(
            access_key="AJIAJLRNVRLZRDZLVBXR", secret_key="SECRET"
        ),
    )


def test_connectors_list(httpx_mock: HTTPXMock, connector_json, connector):
    httpx_mock.add_response(
        url=f"{LIST_URL}?limit=1000",
        json={
            "connectors": [connector_json],
            "pagination": _pagination(total=1, limit=1000, offset=0),
        },
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    it = cloud.platform.connectors.get()
    items = list(it)
    assert items == [connector]
    assert it.total == 1


def test_connectors_details(httpx_mock: HTTPXMock, connector_json, connector):
    httpx_mock.add_response(url=DETAIL_URL, json={"connector": connector_json})
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.details(CONN_ID)
    assert resp == connector


def test_connectors_create(httpx_mock: HTTPXMock, connector_json, connector):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json=_create_match_json(),
        json={"connector": connector_json},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.create(_create_payload())
    assert resp == connector


def test_connectors_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json=_update_match_json(),
        json={"id": CONN_ID},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.update(CONN_ID, connector=_update_connector())
    assert resp == UUID(CONN_ID)


def test_connectors_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.platform.connectors.delete(CONN_ID) is None


def test_connectors_import_data(httpx_mock: HTTPXMock, connector_json, connector):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/import", method="post", json={"connector": connector_json}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.import_data(CONN_ID)
    assert resp == connector


def test_connectors_list_aws_cloudtrails(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{LIST_URL}/aws/cloudtrails",
        method="post",
        match_json={"region": [{"name": "All"}], "credentials": {}},
        json={"trails": [TRAIL_JSON]},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.list_aws_cloudtrails(regions=["All"])
    assert resp == [ConnectorTrail.model_validate(TRAIL_JSON)]


def test_connectors_list_aws_cloudtrails_keyed(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{LIST_URL}/aws/cloudtrails",
        method="post",
        match_json={
            "region": [{"name": "All"}],
            "credentials": {"access_key": "AKID", "secret_key": "SECRET"},
        },
        json={"trails": [TRAIL_JSON]},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.list_aws_cloudtrails(
        regions=["All"], access_key="AKID", secret_key="SECRET"
    )
    assert resp == [ConnectorTrail.model_validate(TRAIL_JSON)]


def test_connectors_cloudformation_template(httpx_mock: HTTPXMock):
    body = {
        "template_content": "redacted",
        "tio_external_id": "bc738cae-114b-4cc1-9f15-17319a20e5a3",
        "tio_bucket_region": "us-east-1",
        "tio_site": "qa-develop",
        "kms_arn": (
            "arn:aws:kms:us-east-1:926186178802:key/b245e9d8-102d-4658-a602-a898fc782d92"
        ),
    }
    httpx_mock.add_response(
        url=f"{LIST_URL}/cloudformation-template",
        method="post",
        match_json={"connector_id": CONN_ID, "account_id": "012345678901"},
        json=body,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.cloudformation_template(
        CONN_ID, account_id="012345678901"
    )
    assert resp.template_content == "redacted"


def test_connectors_arm_template(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{LIST_URL}/azure-fa/{CONN_ID}/arm-template",
        json={"contentVersion": "1.0.0.0"},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    resp = cloud.platform.connectors.arm_template(CONN_ID)
    assert resp == {"contentVersion": "1.0.0.0"}


def test_connector_model_save(httpx_mock: HTTPXMock, connector_json, connector):
    httpx_mock.add_response(
        url=DETAIL_URL, method="get", json={"connector": connector_json}
    )
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json={
            "connector": {
                "name": "AWS Connector - Keyed",
                "type": "aws",
                "network_uuid": "2825e3c9-16be-41f4-8b83-dfe534d10627",
                "schedule": {"units": "days", "value": 1},
                "params": {
                    "access_key": "AJIAJLRNVRLZRDZLVBXR",
                    "secret_key": "REDACTED",
                    "trails": [TRAIL_JSON],
                },
            }
        },
        json={"id": CONN_ID},
    )
    httpx_mock.add_response(
        url=DETAIL_URL, method="get", json={"connector": connector_json}
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    conn = cloud.platform.connectors.details(CONN_ID)
    resp = conn.save()
    assert resp == connector


@pytest.mark.asyncio
async def test_async_connectors_list(httpx_mock: HTTPXMock, connector_json, connector):
    httpx_mock.add_response(
        url=f"{LIST_URL}?limit=1000",
        json={
            "connectors": [connector_json],
            "pagination": _pagination(total=1, limit=1000, offset=0),
        },
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    it = await cloud.platform.connectors.get()
    items = [item async for item in it]
    assert items == [connector]
    assert it.total == 1


@pytest.mark.asyncio
async def test_async_connectors_details(
    httpx_mock: HTTPXMock, connector_json, connector
):
    httpx_mock.add_response(url=DETAIL_URL, json={"connector": connector_json})
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.connectors.details(CONN_ID)
    assert resp == connector


@pytest.mark.asyncio
async def test_async_connectors_create(
    httpx_mock: HTTPXMock, connector_json, connector
):
    httpx_mock.add_response(
        url=LIST_URL,
        method="post",
        match_json=_create_match_json(),
        json={"connector": connector_json},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.connectors.create(_create_payload())
    assert resp == connector


@pytest.mark.asyncio
async def test_async_connectors_update(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=DETAIL_URL,
        method="put",
        match_json=_update_match_json(),
        json={"id": CONN_ID},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.connectors.update(
        CONN_ID, connector=_update_connector()
    )
    assert resp == UUID(CONN_ID)


@pytest.mark.asyncio
async def test_async_connectors_delete(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=DETAIL_URL, method="delete")
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.platform.connectors.delete(CONN_ID) is None


@pytest.mark.asyncio
async def test_async_connectors_import_data(
    httpx_mock: HTTPXMock, connector_json, connector
):
    httpx_mock.add_response(
        url=f"{DETAIL_URL}/import", method="post", json={"connector": connector_json}
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.connectors.import_data(CONN_ID)
    assert resp == connector


@pytest.mark.asyncio
async def test_async_connectors_list_aws_cloudtrails(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{LIST_URL}/aws/cloudtrails",
        method="post",
        match_json={"region": [{"name": "All"}], "credentials": {}},
        json={"trails": [TRAIL_JSON]},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.connectors.list_aws_cloudtrails(regions=["All"])
    assert resp == [ConnectorTrail.model_validate(TRAIL_JSON)]


@pytest.mark.asyncio
async def test_async_connectors_cloudformation_template(httpx_mock: HTTPXMock):
    body = {
        "template_content": "redacted",
        "tio_external_id": "bc738cae-114b-4cc1-9f15-17319a20e5a3",
        "tio_bucket_region": "us-east-1",
        "tio_site": "qa-develop",
        "kms_arn": (
            "arn:aws:kms:us-east-1:926186178802:key/b245e9d8-102d-4658-a602-a898fc782d92"
        ),
    }
    httpx_mock.add_response(
        url=f"{LIST_URL}/cloudformation-template",
        method="post",
        match_json={"connector_id": CONN_ID, "account_id": "012345678901"},
        json=body,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.connectors.cloudformation_template(
        CONN_ID, account_id="012345678901"
    )
    assert resp.template_content == "redacted"


@pytest.mark.asyncio
async def test_async_connectors_arm_template(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{LIST_URL}/azure-fa/{CONN_ID}/arm-template",
        json={"contentVersion": "1.0.0.0"},
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    resp = await cloud.platform.connectors.arm_template(CONN_ID)
    assert resp == {"contentVersion": "1.0.0.0"}
