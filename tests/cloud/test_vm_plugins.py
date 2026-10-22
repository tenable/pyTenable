from datetime import date, datetime, timezone
from typing import Any

import pytest
from pydantic import ValidationError
from pytest_httpx import HTTPXMock

from tenable.cloud import AsyncTenableCloud, TenableCloud
from tenable.cloud.vm.models.plugins import (
    Plugin,
    PluginDetails,
    PluginFamily,
    PluginFamilyDetails,
    PluginListParams,
)
from tenable.errors import TenableCloudAPIError

BASE_URL = "https://cloud.tenable.com"
PLUGINS_URL = f"{BASE_URL}/plugins/plugin"
FAMILIES_URL = f"{BASE_URL}/plugins/families"


@pytest.fixture
def plugin_json() -> dict[str, Any]:
    return {
        "id": 13670,
        "name": "Fedora Core 1 : kernel-2.4.22-1.2140.nptl (2003-047)",
        "family_id": 30,
        "family_name": "Fedora Local Security Checks",
        "attributes": {
            "plugin_modification_date": "2018-07-19T00:00:00Z",
            "plugin_version": "1.17",
            "exploited_by_malware": False,
            "description": "Various RTC drivers had the potential to leak memory.",
            "unsupported_by_vendor": False,
            "cvss_temporal_score": 0,
            "patch_publication_date": "2004-01-07T00:00:00Z",
            "see_also": ["http://www.nessus.org/u?07bc9e7f"],
            "default_account": False,
            "exploit_available": False,
            "cve": ["CVE-2003-0984"],
            "bid": [9154],
            "cvss_base_score": 4.6,
            "solution": "Update the affected packages.",
            "cvss_vector": {
                "raw": "AV:L/AC:L/Au:N/C:P/I:P/A:P",
                "AccessVector": "Local-access",
                "Availability-Impact": "Partial",
                "Authentication": "None required",
                "Integrity-Impact": "Partial",
                "AccessComplexity": "Low",
                "Confidentiality-Impact": "Partial",
            },
            "cvss3_vector": {
                "raw": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                "AttackVector": "Network",
                "PrivilegesRequired": "None",
                "Confidentiality-Impact": "High",
            },
            "cvss3_temporal_vector": {
                "raw": "E:U/RL:O/RC:C",
                "ExploitCodeMaturity": "Unproven",
            },
            "cpe": ["cpe:/o:fedoraproject:fedora_core:1"],
            "plugin_publication_date": "2004-07-23T00:00:00Z",
            "vuln_publication_date": "2004-01-07T00:00:00Z",
            "xrefs": [{"type": "FEDORA", "id": "2003-047"}],
            "risk_factor": "Medium",
            "synopsis": "The remote Fedora Core host is missing a security update.",
            "vpr": {
                "score": 5.9,
                "drivers": {"age_of_vuln": {"lower_bound": 730}},
                "updated": "2025-04-01T10:00:00Z",
            },
        },
    }


@pytest.fixture
def details_json() -> dict[str, Any]:
    return {
        "attributes": [
            {"attribute_value": "aix_IY19744.nasl", "attribute_name": "fname"},
            {"attribute_value": "High", "attribute_name": "risk_factor"},
        ],
        "family_name": "AIX Local Security Checks",
        "name": "AIX 5.1 : IY19744",
        "id": 22372,
        "vpr": {"score": 6.7},
    }


@pytest.fixture
def family_json() -> dict[str, Any]:
    return {
        "plugins": [
            {"id": 22372, "name": "AIX 5.1 : IY19744"},
            {"id": 22373, "name": "AIX 5.1 : IY20486"},
        ],
        "name": "AIX Local Security Checks",
        "id": 1,
    }


@pytest.fixture
def families_json() -> dict[str, Any]:
    return {
        "families": [
            {"count": 11342, "name": "AIX Local Security Checks", "id": 1},
            {"count": 114, "name": "Backdoors", "id": 17},
        ]
    }


def plugin_page(plugin_json: dict[str, Any], count: int, total: int) -> dict:
    return {
        "data": {"plugin_details": [plugin_json for _ in range(count)]},
        "size": count,
        "params": {"page": 1, "size": 2},
        "total_count": total,
    }


def test_plugin_model(plugin_json):
    plugin = Plugin.model_validate(plugin_json)
    attrs = plugin.attributes
    assert attrs is not None
    assert attrs.plugin_modification_date == datetime(2018, 7, 19, tzinfo=timezone.utc)
    assert attrs.cvss_vector is not None
    assert attrs.cvss_vector.availability_impact == "Partial"
    assert attrs.cvss_vector.access_vector == "Local-access"
    assert attrs.cvss3_vector is not None
    assert attrs.cvss3_vector.attack_vector == "Network"
    assert attrs.cvss3_temporal_vector is not None
    assert attrs.cvss3_temporal_vector.exploit_code_maturity == "Unproven"
    assert attrs.vpr is not None
    assert attrs.vpr.updated == datetime(2025, 4, 1, 10, tzinfo=timezone.utc)
    assert attrs.xrefs[0].type == "FEDORA"
    # The vector objects must serialize back to the API's field names.
    dumped = plugin.model_dump(exclude_none=True)
    assert dumped["attributes"]["cvss_vector"]["Availability-Impact"] == "Partial"


def test_plugin_details_model(details_json):
    details = PluginDetails.model_validate(details_json)
    assert details.attributes[0].name == "fname"
    assert details.attributes[0].value == "aix_IY19744.nasl"
    assert details.vpr is not None and details.vpr.score == 6.7


def test_plugin_list_params():
    params = PluginListParams.model_validate({"last_updated": "2025-01-01"})
    assert params.model_dump(mode="json", exclude_none=True) == {
        "last_updated": "2025-01-01"
    }
    with pytest.raises(ValidationError):
        PluginListParams(size=10001)
    with pytest.raises(ValidationError):
        PluginListParams(last_updated="not-a-date")  # type: ignore[arg-type]


def test_plugins_get(httpx_mock: HTTPXMock, plugin_json):
    httpx_mock.add_response(
        url=f"{PLUGINS_URL}?last_updated=2025-01-01&size=2&page=1",
        json=plugin_page(plugin_json, 2, 5),
    )
    httpx_mock.add_response(
        url=f"{PLUGINS_URL}?last_updated=2025-01-01&size=2&page=2",
        json=plugin_page(plugin_json, 2, 5),
    )
    httpx_mock.add_response(
        url=f"{PLUGINS_URL}?last_updated=2025-01-01&size=2&page=3",
        json=plugin_page(plugin_json, 1, 5),
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    plugins = cloud.vm.plugins.get(last_updated=date(2025, 1, 1), size=2)
    expected = Plugin.model_validate(plugin_json)
    for plugin in plugins:
        assert plugin == expected
    assert plugins.count == 5
    assert plugins.total == 5
    assert plugins.num_pages == 3


def test_plugins_get_defaults(httpx_mock: HTTPXMock, plugin_json):
    httpx_mock.add_response(
        url=f"{PLUGINS_URL}?size=1000&page=1",
        json=plugin_page(plugin_json, 1, 1),
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert len(list(cloud.vm.plugins.get())) == 1


def test_plugins_get_empty(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=f"{PLUGINS_URL}?size=1000&page=1",
        json={"data": {"plugin_details": []}, "size": 0, "total_count": 0},
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert list(cloud.vm.plugins.get()) == []


def test_plugins_details(httpx_mock: HTTPXMock, details_json):
    httpx_mock.add_response(url=f"{PLUGINS_URL}/22372", json=details_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    assert cloud.vm.plugins.details(22372) == PluginDetails.model_validate(details_json)


def test_plugins_details_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(url=f"{PLUGINS_URL}/1", status_code=404, json={})
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    with pytest.raises(TenableCloudAPIError):
        cloud.vm.plugins.details(1)


def test_plugins_families(httpx_mock: HTTPXMock, families_json):
    httpx_mock.add_response(url=FAMILIES_URL, json=families_json)
    httpx_mock.add_response(url=f"{FAMILIES_URL}?all=true", json=families_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    expected = [PluginFamily.model_validate(f) for f in families_json["families"]]
    assert cloud.vm.plugins.families() == expected
    assert cloud.vm.plugins.families(all=True) == expected


def test_plugins_family_details_by_id(httpx_mock: HTTPXMock, family_json):
    httpx_mock.add_response(url=f"{FAMILIES_URL}/1", json=family_json)
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    family = cloud.vm.plugins.family_details(1)
    assert family == PluginFamilyDetails.model_validate(family_json)
    assert family.plugins[1].id == 22373


def test_plugins_family_details_by_name(httpx_mock: HTTPXMock, family_json):
    httpx_mock.add_response(
        url=f"{FAMILIES_URL}/_byName",
        method="POST",
        match_json={"name": "AIX Local Security Checks"},
        json=family_json,
    )
    cloud = TenableCloud(access_key="ABC", secret_key="DEF")
    family = cloud.vm.plugins.family_details("AIX Local Security Checks")
    assert family == PluginFamilyDetails.model_validate(family_json)


@pytest.mark.asyncio
async def test_async_plugins_get(httpx_mock: HTTPXMock, plugin_json):
    httpx_mock.add_response(
        url=f"{PLUGINS_URL}?size=2&page=1",
        json=plugin_page(plugin_json, 2, 3),
    )
    httpx_mock.add_response(
        url=f"{PLUGINS_URL}?size=2&page=2",
        json=plugin_page(plugin_json, 1, 3),
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    plugins = await cloud.vm.plugins.get(size=2)
    expected = Plugin.model_validate(plugin_json)
    async for plugin in plugins:
        assert plugin == expected
    assert plugins.count == 3
    assert plugins.total == 3


@pytest.mark.asyncio
async def test_async_plugins_details(httpx_mock: HTTPXMock, details_json):
    httpx_mock.add_response(url=f"{PLUGINS_URL}/22372", json=details_json)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    assert await cloud.vm.plugins.details(22372) == PluginDetails.model_validate(
        details_json
    )


@pytest.mark.asyncio
async def test_async_plugins_families(httpx_mock: HTTPXMock, families_json):
    httpx_mock.add_response(url=f"{FAMILIES_URL}?all=false", json=families_json)
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    families = await cloud.vm.plugins.families(all=False)
    assert [f.id for f in families] == [1, 17]


@pytest.mark.asyncio
async def test_async_plugins_family_details(httpx_mock: HTTPXMock, family_json):
    httpx_mock.add_response(url=f"{FAMILIES_URL}/1", json=family_json)
    httpx_mock.add_response(
        url=f"{FAMILIES_URL}/_byName",
        method="POST",
        match_json={"name": "AIX Local Security Checks"},
        json=family_json,
    )
    cloud = AsyncTenableCloud(access_key="ABC", secret_key="DEF")
    expected = PluginFamilyDetails.model_validate(family_json)
    assert await cloud.vm.plugins.family_details(1) == expected
    assert (
        await cloud.vm.plugins.family_details("AIX Local Security Checks") == expected
    )
