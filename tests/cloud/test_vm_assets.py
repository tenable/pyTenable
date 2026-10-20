from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import pytest
from pydantic import ValidationError
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.vm.models.assets import (
    Asset,
    AssetAcrIdentifier,
    AssetAcrUpdate,
    AssetImportJob,
    AssetQueryFilter,
    AssetSummary,
)
from tenable.errors import TenableCloudAPIError

BASE_URL = "https://cloud.tenable.com"
ASSET_UUID = "236224b4-e3e7-4761-ad47-e32daaebec6b"
JOB_UUID = "3c824793-73d8-4c2e-bfc3-c2f78afa3bbf"
DEFAULT_NET = "00000000-0000-0000-0000-000000000000"
CUSTOM_NET = "4dee97b4-592b-4b5b-a8a9-d7a605a3723a"
BULK_RESP = {"response": {"data": {"asset_count": 512}}}


@pytest.fixture
def summary_json() -> dict[str, Any]:
    return {
        "id": "436224b4-e3e7-4761-ad47-e32daaebec6b",
        "has_agent": True,
        "last_seen": "2025-04-30T12:45:41.039Z",
        "last_scan_target": "192.0.2.151",
        "sources": [
            {
                "name": "NESSUS_SCAN",
                "first_seen": "2025-04-18T10:31:22.214Z",
                "last_seen": "2025-04-18T13:39:54.799Z",
            },
            {
                "name": "ExternalAttackSurfaceMap",
                "first_seen": "2024-05-30T07:40:27.030Z",
                "last_seen": "2025-05-25T07:31:16.777Z",
            },
        ],
        "acr_score": 5,
        "acr_drivers": [
            {"driver_name": "device_type", "driver_value": ["general_purpose"]},
        ],
        "exposure_score": 686,
        "scan_frequency": None,
        "ipv4": ["192.0.2.151"],
        "ipv6": ["2001:db8:1a7e:90bb:e562:7e41:3c98:86b0"],
        "fqdn": ["lab.example.com"],
        "mac_address": ["10:50:56:a6:90:fb"],
        "netbios_name": [],
        "operating_system": ["Oracle Linux Server 8.7"],
        "hostname": ["ol-euk-8.4.support.lab.tenablesecurity.com"],
        "agent_name": ["example-name"],
        "aws_ec2_name": [],
        "security_protection_level": None,
        "security_protections": [],
        "exposure_confidence_value": None,
    }


@pytest.fixture
def asset_json() -> dict[str, Any]:
    return {
        "name": "example-asset",
        "id": ASSET_UUID,
        "has_agent": True,
        "created_at": "2025-04-18T10:31:22.214Z",
        "updated_at": "2025-07-02T00:53:32.864Z",
        "terminated_at": None,
        "deleted_at": None,
        "aes_score_v3": 757,
        "acr_score_v3": 6,
        "first_seen": "2025-04-18T10:31:22.000Z",
        "last_seen": "2025-04-30T12:45:41.039Z",
        "last_scan_target": "192.0.2.79",
        "last_authentication_attempt_date": "2025-04-18T13:39:54.799Z",
        "last_authentication_success_date": "2025-04-18T13:39:54.799Z",
        "last_authenticated_scan_date": "2025-04-18T14:20:36.407Z",
        "last_licensed_scan_date": "2025-04-18T14:20:36.407Z",
        "last_scan_id": "1bd973b9-85d2-4a4d-90c6-60d399238435",
        "last_schedule_id": (
            "template-83dfa4ac-32cc-92dd-4a5e-2ff4136cecaa9f62a41bc3058712"
        ),
        "sources": [
            {
                "name": "NESSUS_AGENT",
                "first_seen": "2025-04-18T11:48:03.328Z",
                "last_seen": "2025-04-30T12:45:41.039Z",
            }
        ],
        "tags": [
            {
                "tag_uuid": "a9b7a9c6-7a5a-4b5e-a2c1-4a1d2c6b8e7f",
                "tag_key": "Location",
                "tag_value": "Columbia",
                "added_by": "0f403df2-3b35-4339-9f74-1574805de203",
                "added_at": "2025-04-18T10:31:22.214Z",
            }
        ],
        "acr_score": 5,
        "exposure_score": 686,
        "scan_frequency": [{"interval": 90, "frequency": 3, "licensed": False}],
        "interfaces": [
            {
                "ipv4": ["192.0.2.80"],
                "ipv6": [],
                "fqdn": ["lab.example.com"],
                "mac_address": ["10:50:56:a6:90:fb"],
                "name": "ens192",
                "virtual": None,
                "aliased": None,
            }
        ],
        "network_id": [DEFAULT_NET],
        "ipv4": ["192.0.2.80"],
        "system_type": ["general-purpose"],
        "tenable_uuid": ["76cd04c276c9431ebeabd8a98ec2af69"],
        "bios_uuid": ["9b922642-7e01-6c78-e9b3-8618c18f023d"],
        "aws_region": ["us-west-1"],
        "installed_software": ["cpe:/a:openbsd:openssh:8.0"],
        "bigfix_asset_id": [],
    }


@pytest.fixture
def job_json() -> dict[str, Any]:
    return {
        "job_id": JOB_UUID,
        "container_id": "1a2d819b-c818-40a8-a2eb-3f746c4b0ab3",
        "source": "test1",
        "batches": 1,
        "uploaded_assets": 0,
        "failed_assets": 0,
        "start_time": 1544480303548,
        "last_update_time": 1544484511492,
        "end_time": 1544484511492,
        "status": "ERROR",
        "status_message": "Job failed by exceeding time limit",
    }


@pytest.fixture
def cloud() -> TenableCloud:
    return TenableCloud(access_key="ABC", secret_key="DEF")


@pytest.fixture
def acloud() -> AsyncTenableCloud:
    return AsyncTenableCloud(access_key="ABC", secret_key="DEF")


def test_asset_summary_model(summary_json):
    asset = AssetSummary.model_validate(summary_json)
    assert asset.id == UUID("436224b4-e3e7-4761-ad47-e32daaebec6b")
    assert isinstance(asset.last_seen, datetime)
    # Custom source names outside of the documented enum must be accepted.
    assert asset.sources[1].name == "ExternalAttackSurfaceMap"
    assert asset.scan_frequency is None


def test_asset_model(asset_json):
    asset = Asset.model_validate(asset_json)
    assert asset.network_id == [UUID(DEFAULT_NET)]
    assert asset.tags[0].tag_key == "Location"
    assert asset.interfaces[0].name == "ens192"
    assert asset.terminated_at is None
    assert asset.aws_ec2_instance_id == []


def test_import_job_model_timestamps(job_json):
    job = AssetImportJob.model_validate(job_json)
    assert job.start_time == datetime(
        2018, 12, 10, 22, 18, 23, 548000, tzinfo=timezone.utc
    )


@pytest.mark.parametrize(
    "value",
    [
        {"id": ASSET_UUID},
        {"fqdn": ["db.example.com"]},
        {"id": None, "ipv4": ["192.0.2.1"]},
    ],
)
def test_acr_identifier_single_property(value):
    assert AssetAcrIdentifier.model_validate(value)


@pytest.mark.parametrize(
    "value",
    [{}, {"id": None}, {"id": ASSET_UUID, "fqdn": ["db.example.com"]}],
)
def test_acr_identifier_requires_single_property(value):
    with pytest.raises(ValidationError, match="exactly one of"):
        AssetAcrIdentifier.model_validate(value)


def test_acr_update_splits_identifiers():
    other = "a9b7a9c6-7a5a-4b5e-a2c1-4a1d2c6b8e7f"
    update = AssetAcrUpdate.model_validate(
        {
            "acr_score": 5,
            "asset": [
                {
                    "id": [ASSET_UUID, other],
                    "fqdn": ["db.example.com"],
                    "ipv4": None,
                    "mac_address": [],
                },
                {"netbios_name": ["DB01"]},
                AssetAcrIdentifier(id=UUID(other)),
            ],
        }
    )
    assert update.model_dump(mode="json", exclude_none=True)["asset"] == [
        {"id": ASSET_UUID},
        {"id": other},
        {"fqdn": ["db.example.com"]},
        {"netbios_name": ["DB01"]},
        {"id": other},
    ]


def test_acr_update_single_id_not_split():
    update = AssetAcrUpdate.model_validate(
        {"acr_score": 5, "asset": [{"id": ASSET_UUID}]}
    )
    assert update.asset == [AssetAcrIdentifier(id=UUID(ASSET_UUID))]


@pytest.mark.parametrize(
    "value",
    [
        "ipv4:eq:192.0.2.1",
        ("ipv4", "eq", "192.0.2.1"),
        {"field": "ipv4", "operator": "eq", "value": "192.0.2.1"},
    ],
)
def test_query_filter_formats(value):
    assert AssetQueryFilter.model_validate(value).model_dump() == {
        "field": "ipv4",
        "operator": "eq",
        "value": "192.0.2.1",
    }


def test_query_filter_value_may_contain_colons():
    flt = AssetQueryFilter.model_validate("ipv6:eq:2001:db8::1")
    assert flt.value == "2001:db8::1"


def test_query_filter_invalid_format():
    with pytest.raises(ValidationError, match="not in a valid filter format"):
        AssetQueryFilter.model_validate("ipv4:eq")


def test_assets_get(httpx_mock: HTTPXMock, cloud, summary_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/assets", json={"assets": [summary_json], "total": 1}
    )
    assert cloud.vm.assets.get() == [AssetSummary.model_validate(summary_json)]


def test_assets_details(httpx_mock: HTTPXMock, cloud, asset_json):
    httpx_mock.add_response(url=f"{BASE_URL}/assets/{ASSET_UUID}", json=asset_json)
    assert cloud.vm.assets.details(ASSET_UUID) == Asset.model_validate(asset_json)


def test_assets_details_error(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/assets/{ASSET_UUID}",
        status_code=404,
        headers={"Request-UUID": "abc123"},
    )
    with pytest.raises(TenableCloudAPIError) as err:
        cloud.vm.assets.details(ASSET_UUID)
    assert err.value.status_code == 404
    assert err.value.request_uuid == "abc123"


def test_assets_update_acr(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/acr",
        method="post",
        status_code=202,
        match_json=[
            {
                "acr_score": 8,
                "reason": ["Business Critical", "Other"],
                "note": "Production database",
                "asset": [
                    {"id": ASSET_UUID},
                    {"fqdn": ["db.example.com"]},
                    {"ipv4": ["192.0.2.1", "192.0.2.2"]},
                    {"mac_address": ["10:50:56:a6:90:fb"]},
                    {"netbios_name": ["DB01"]},
                ],
            }
        ],
    )
    assert (
        cloud.vm.assets.update_acr(
            8,
            asset_ids=[ASSET_UUID],
            fqdns=["db.example.com"],
            ipv4s=["192.0.2.1", "192.0.2.2"],
            mac_addresses=["10:50:56:a6:90:fb"],
            netbios_names=["DB01"],
            reasons=["Business Critical", "Other"],
            note="Production database",
        )
        is None
    )


def test_assets_update_acr_minimal(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/acr",
        method="post",
        status_code=202,
        match_json=[{"acr_score": 1, "asset": [{"id": ASSET_UUID}]}],
    )
    cloud.vm.assets.update_acr(1, asset_ids=[ASSET_UUID])


@pytest.mark.parametrize("score", [0, 11])
def test_assets_update_acr_invalid_score(cloud, score):
    with pytest.raises(ValidationError):
        cloud.vm.assets.update_acr(score, asset_ids=[ASSET_UUID])


def test_assets_update_acr_requires_identifier(cloud):
    with pytest.raises(ValidationError):
        cloud.vm.assets.update_acr(5)


def test_assets_update_acr_invalid_reason(cloud):
    with pytest.raises(ValidationError):
        cloud.vm.assets.update_acr(5, asset_ids=[ASSET_UUID], reasons=["Because"])


def test_assets_move(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/move-to-network",
        method="post",
        status_code=202,
        match_json={
            "source": DEFAULT_NET,
            "destination": CUSTOM_NET,
            "targets": "192.0.2.57-192.0.2.69,198.51.100.0/24",
        },
        json=BULK_RESP,
    )
    count = cloud.vm.assets.move(
        DEFAULT_NET, CUSTOM_NET, ["192.0.2.57-192.0.2.69", "198.51.100.0/24"]
    )
    assert count == 512


def test_assets_move_string_targets(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/move-to-network",
        method="post",
        status_code=202,
        match_json={
            "source": DEFAULT_NET,
            "destination": CUSTOM_NET,
            "targets": "192.0.2.1,192.0.2.2",
        },
        json=BULK_RESP,
    )
    assert cloud.vm.assets.move(DEFAULT_NET, CUSTOM_NET, "192.0.2.1, 192.0.2.2") == 512


def test_assets_move_ok_response(httpx_mock: HTTPXMock, cloud):
    # Should the API ever respond with a 200 instead of a 202, it should still work.
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/move-to-network",
        method="post",
        status_code=200,
        json=BULK_RESP,
    )
    assert cloud.vm.assets.move(DEFAULT_NET, CUSTOM_NET, "192.0.2.1") == 512


def test_assets_move_error(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/move-to-network",
        method="post",
        status_code=400,
    )
    with pytest.raises(TenableCloudAPIError):
        cloud.vm.assets.move(DEFAULT_NET, CUSTOM_NET, "192.0.2.1")


def test_assets_bulk_delete(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/delete",
        method="post",
        status_code=202,
        match_json={
            "query": {
                "or": [
                    {"field": "host.hostname", "operator": "match", "value": "ex"},
                    {"field": "ipv4", "operator": "eq", "value": "192.0.2.1"},
                ]
            },
            "hard_delete": True,
        },
        json=BULK_RESP,
    )
    count = cloud.vm.assets.bulk_delete(
        ("host.hostname", "match", "ex"),
        "ipv4:eq:192.0.2.1",
        filter_type="or",
        hard_delete=True,
    )
    assert count == 512


def test_assets_bulk_delete_defaults(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/delete",
        method="post",
        status_code=202,
        match_json={
            "query": {"and": [{"field": "ipv4", "operator": "eq", "value": "1.2.3.4"}]}
        },
        json=BULK_RESP,
    )
    assert cloud.vm.assets.bulk_delete("ipv4:eq:1.2.3.4") == 512


def test_assets_bulk_delete_requires_filter(cloud):
    with pytest.raises(ValueError, match="At least one filter"):
        cloud.vm.assets.bulk_delete()


def test_assets_import_jobs(httpx_mock: HTTPXMock, cloud, job_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/import/asset-jobs", json={"asset_import_jobs": [job_json]}
    )
    assert cloud.vm.assets.import_jobs() == [AssetImportJob.model_validate(job_json)]


def test_assets_import_job_details(httpx_mock: HTTPXMock, cloud, job_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/import/asset-jobs/{JOB_UUID}", json=job_json
    )
    job = cloud.vm.assets.import_job_details(JOB_UUID)
    assert job == AssetImportJob.model_validate(job_json)


def test_assets_import_assets(httpx_mock: HTTPXMock, cloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/import/assets",
        method="post",
        match_json={
            "source": "Custom Import",
            "assets": [
                {"ipv4": ["192.0.2.57"], "operating_system": ["Windows 7 x64"]},
                {"netbios_name": "HOST01", "aws_region": "us-east-1"},
            ],
        },
        json={"asset_import_job_uuid": JOB_UUID},
    )
    job_id = cloud.vm.assets.import_assets(
        "Custom Import",
        [
            {"ipv4": ["192.0.2.57"], "operating_system": ["Windows 7 x64"]},
            {"netbios_name": "HOST01", "aws_region": "us-east-1"},
        ],
    )
    assert job_id == UUID(JOB_UUID)


def test_assets_import_assets_requires_identifier(cloud):
    with pytest.raises(ValidationError, match="at least one of"):
        cloud.vm.assets.import_assets("src", [{"hostname": ["host01"]}])


def test_assets_import_assets_requires_assets(cloud):
    with pytest.raises(ValidationError):
        cloud.vm.assets.import_assets("src", [])


@pytest.mark.asyncio
async def test_async_assets_get(httpx_mock: HTTPXMock, acloud, summary_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/assets", json={"assets": [summary_json], "total": 1}
    )
    assert await acloud.vm.assets.get() == [AssetSummary.model_validate(summary_json)]


@pytest.mark.asyncio
async def test_async_assets_details(httpx_mock: HTTPXMock, acloud, asset_json):
    httpx_mock.add_response(url=f"{BASE_URL}/assets/{ASSET_UUID}", json=asset_json)
    asset = await acloud.vm.assets.details(ASSET_UUID)
    assert asset == Asset.model_validate(asset_json)


@pytest.mark.asyncio
async def test_async_assets_update_acr(httpx_mock: HTTPXMock, acloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/acr",
        method="post",
        status_code=202,
        match_json=[
            {
                "acr_score": 8,
                "reason": ["Business Critical"],
                "note": "note",
                "asset": [{"id": ASSET_UUID}, {"fqdn": ["db.example.com"]}],
            }
        ],
    )
    result = await acloud.vm.assets.update_acr(
        8,
        asset_ids=[ASSET_UUID],
        fqdns=["db.example.com"],
        reasons=["Business Critical"],
        note="note",
    )
    assert result is None


@pytest.mark.asyncio
async def test_async_assets_move(httpx_mock: HTTPXMock, acloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/move-to-network",
        method="post",
        status_code=202,
        match_json={
            "source": DEFAULT_NET,
            "destination": CUSTOM_NET,
            "targets": "192.0.2.0/24",
        },
        json=BULK_RESP,
    )
    count = await acloud.vm.assets.move(DEFAULT_NET, CUSTOM_NET, ["192.0.2.0/24"])
    assert count == 512


@pytest.mark.asyncio
async def test_async_assets_move_ok_response(httpx_mock: HTTPXMock, acloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/move-to-network",
        method="post",
        status_code=200,
        json=BULK_RESP,
    )
    count = await acloud.vm.assets.move(DEFAULT_NET, CUSTOM_NET, "192.0.2.1")
    assert count == 512


@pytest.mark.asyncio
async def test_async_assets_bulk_delete(httpx_mock: HTTPXMock, acloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/api/v2/assets/bulk-jobs/delete",
        method="post",
        status_code=202,
        match_json={
            "query": {"and": [{"field": "ipv4", "operator": "eq", "value": "1.2.3.4"}]},
            "hard_delete": False,
        },
        json=BULK_RESP,
    )
    count = await acloud.vm.assets.bulk_delete("ipv4:eq:1.2.3.4", hard_delete=False)
    assert count == 512


@pytest.mark.asyncio
async def test_async_assets_bulk_delete_requires_filter(acloud):
    with pytest.raises(ValueError, match="At least one filter"):
        await acloud.vm.assets.bulk_delete()


@pytest.mark.asyncio
async def test_async_assets_import_jobs(httpx_mock: HTTPXMock, acloud, job_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/import/asset-jobs", json={"asset_import_jobs": [job_json]}
    )
    jobs = await acloud.vm.assets.import_jobs()
    assert jobs == [AssetImportJob.model_validate(job_json)]


@pytest.mark.asyncio
async def test_async_assets_import_job_details(httpx_mock: HTTPXMock, acloud, job_json):
    httpx_mock.add_response(
        url=f"{BASE_URL}/import/asset-jobs/{JOB_UUID}", json=job_json
    )
    job = await acloud.vm.assets.import_job_details(JOB_UUID)
    assert job == AssetImportJob.model_validate(job_json)


@pytest.mark.asyncio
async def test_async_assets_import_assets(httpx_mock: HTTPXMock, acloud):
    httpx_mock.add_response(
        url=f"{BASE_URL}/import/assets",
        method="post",
        match_json={"source": "Custom Import", "assets": [{"fqdn": ["a.example"]}]},
        json={"asset_import_job_uuid": JOB_UUID},
    )
    job_id = await acloud.vm.assets.import_assets(
        "Custom Import", [{"fqdn": ["a.example"]}]
    )
    assert job_id == UUID(JOB_UUID)


def test_acr_update_asset_must_be_list():
    with pytest.raises(ValidationError):
        AssetAcrUpdate.model_validate({"acr_score": 5, "asset": {"id": ASSET_UUID}})
