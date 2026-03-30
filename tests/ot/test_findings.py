"""
test findings
"""
import datetime
import uuid

import pytest
import responses

from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.schema.findings import (
    Finding,
    FindingAsset,
    FindingPlugin,
    FindingPluginDetails,
    FindingAssetRisk,
    PluginRef,
)


@responses.activate
def test_list(fixture_ot):
    """
    Tests the findings GraphQL list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "findings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "d9dc32ba06243f814f819d363b521d55e351d9370b17c750c6322a67bc9d0086",
                            "status": "Active",
                            "firstHit": "2026-03-04T17:05:24.449819Z",
                            "lastHit": "2026-03-04T17:05:24.449819Z",
                            "fixedAt": None,
                            "port": 0,
                            "protocol": "tcp",
                            "svcName": None,
                            "output": "Test output",
                            "asset": {
                                "id": "5cb025fd-524b-47f1-81f7-bd472b450c7d",
                                "name": "Server Room - SNC-EB630",
                                "type": "Camera",
                                "criticality": "MediumCriticality",
                                "location": "Server Room",
                                "purdueLevel": "Level2",
                                "risk": {
                                    "totalRisk": 8.5,
                                    "unresolvedEvents": 3
                                },
                                "ips": {"nodes": ["192.168.1.100"]},
                                "macs": {"nodes": ["00:11:22:33:44:55"]}
                            },
                            "plugin": {
                                "id": 502387,
                                "name": "Sony Network Cameras Stack-based Buffer Overflow (CVE-2018-3938)",
                                "severity": "Critical",
                                "family": "Tenable.ot",
                                "source": "Tot",
                                "vprScore": 6.5,
                                "comment": None,
                                "owner": None,
                                "details": {
                                    "id": 502387,
                                    "name": "Sony Network Cameras Stack-based Buffer Overflow (CVE-2018-3938)",
                                    "description": "An exploitable stack-based buffer overflow vulnerability exists",
                                    "solution": "Apply vendor updates",
                                    "seeAlso": ["https://example.com/advisory"],
                                    "pluginType": "remote",
                                    "pluginPubDate": "2018-08-01T00:00:00Z",
                                    "pluginModDate": "2019-01-15T00:00:00Z",
                                    "vulnPubDate": "2018-07-20T00:00:00Z",
                                    "vulnModDate": "2018-08-05T00:00:00Z",
                                    "refs": [
                                        {
                                            "name": "CVE",
                                            "value": "CVE-2018-3938",
                                            "url": "http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2018-3938"
                                        }
                                    ],
                                    "cpe": "cpe:/a:sony:network_camera",
                                    "cvssVector": "CVSS2#AV:N/AC:L/Au:N/C:C/I:C/A:C",
                                    "cvssV3Vector": "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                                    "cvssBaseScore": 10.0,
                                    "cvssV3BaseScore": 10.0,
                                    "cvssTemporalScore": 8.7,
                                    "cvssV3TemporalScore": 8.7,
                                    "cvssImpactScore": 10.0
                                }
                            }
                        }
                    ],
                    "totalCount": 83
                }
            }
        },
    )

    expected = Finding(
        id="d9dc32ba06243f814f819d363b521d55e351d9370b17c750c6322a67bc9d0086",
        status="Active",
        first_hit=datetime.datetime(2026, 3, 4, 17, 5, 24, 449819, tzinfo=datetime.timezone.utc),
        last_hit=datetime.datetime(2026, 3, 4, 17, 5, 24, 449819, tzinfo=datetime.timezone.utc),
        fixed_at=None,
        port=0,
        protocol="tcp",
        svc_name=None,
        output="Test output",
        asset=FindingAsset(
            id=uuid.UUID("5cb025fd-524b-47f1-81f7-bd472b450c7d"),
            name="Server Room - SNC-EB630",
            type="Camera",
            criticality="MediumCriticality",
            location="Server Room",
            purdue_level="Level2",
            risk=FindingAssetRisk(total_risk=8.5, unresolved_events=3),
            ips={"nodes": ["192.168.1.100"]},
            macs={"nodes": ["00:11:22:33:44:55"]}
        ),
        plugin=FindingPlugin(
            id=502387,
            name="Sony Network Cameras Stack-based Buffer Overflow (CVE-2018-3938)",
            severity="Critical",
            family="Tenable.ot",
            source="Tot",
            vpr_score=6.5,
            comment=None,
            owner=None,
            details=FindingPluginDetails(
                id=502387,
                name="Sony Network Cameras Stack-based Buffer Overflow (CVE-2018-3938)",
                description="An exploitable stack-based buffer overflow vulnerability exists",
                solution="Apply vendor updates",
                see_also=["https://example.com/advisory"],
                plugin_type="remote",
                plugin_pub_date=datetime.datetime(2018, 8, 1, 0, 0, tzinfo=datetime.timezone.utc),
                plugin_mod_date=datetime.datetime(2019, 1, 15, 0, 0, tzinfo=datetime.timezone.utc),
                vuln_pub_date=datetime.datetime(2018, 7, 20, 0, 0, tzinfo=datetime.timezone.utc),
                vuln_mod_date=datetime.datetime(2018, 8, 5, 0, 0, tzinfo=datetime.timezone.utc),
                refs=[
                    PluginRef(
                        name="CVE",
                        value="CVE-2018-3938",
                        url="http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2018-3938"
                    )
                ],
                cpe="cpe:/a:sony:network_camera",
                cvss_vector="CVSS2#AV:N/AC:L/Au:N/C:C/I:C/A:C",
                cvss_v3_vector="CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
                cvss_base_score=10.0,
                cvss_v3_base_score=10.0,
                cvss_temporal_score=8.7,
                cvss_v3_temporal_score=8.7,
                cvss_impact_score=10.0
            )
        )
    )

    resp = fixture_ot.findings.list()
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, Finding)
    assert finding == expected


@responses.activate
def test_by_asset(fixture_ot):
    """
    Tests the findings by_asset method
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "findings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "test-finding-id",
                            "status": "Active",
                            "firstHit": "2026-03-04T17:05:24.449819Z",
                            "lastHit": "2026-03-04T17:05:24.449819Z",
                            "fixedAt": None,
                            "port": 443,
                            "protocol": "tcp",
                            "svcName": "https",
                            "output": None,
                            "asset": {
                                "id": "5cb025fd-524b-47f1-81f7-bd472b450c7d",
                                "name": "Test Asset",
                                "type": "Server",
                                "criticality": None,
                                "location": None,
                                "purdueLevel": None,
                                "risk": None,
                                "ips": None,
                                "macs": None
                            },
                            "plugin": {
                                "id": 12345,
                                "name": "Test Plugin",
                                "severity": "High",
                                "family": "Test Family",
                                "source": "NNM",
                                "vprScore": None,
                                "comment": None,
                                "owner": None,
                                "details": None
                            }
                        }
                    ],
                    "totalCount": 1
                }
            }
        },
    )

    resp = fixture_ot.findings.by_asset(
        asset_id="5cb025fd-524b-47f1-81f7-bd472b450c7d",
        status="Active"
    )
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, Finding)
    assert finding.asset.id == uuid.UUID("5cb025fd-524b-47f1-81f7-bd472b450c7d")
    assert finding.status == "Active"


@responses.activate
def test_by_plugin(fixture_ot):
    """
    Tests the findings by_plugin method
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "findings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "test-finding-id-2",
                            "status": "Active",
                            "firstHit": "2026-03-04T17:05:24.449819Z",
                            "lastHit": "2026-03-04T17:05:24.449819Z",
                            "fixedAt": None,
                            "port": 80,
                            "protocol": "tcp",
                            "svcName": None,
                            "output": None,
                            "asset": {
                                "id": "aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb",
                                "name": "Asset 1",
                                "type": "PLC",
                                "criticality": None,
                                "location": None,
                                "purdueLevel": None,
                                "risk": None,
                                "ips": None,
                                "macs": None
                            },
                            "plugin": {
                                "id": 502387,
                                "name": "Critical Vulnerability",
                                "severity": "Critical",
                                "family": "Test",
                                "source": "Tot",
                                "vprScore": 9.5,
                                "comment": None,
                                "owner": None,
                                "details": None
                            }
                        }
                    ],
                    "totalCount": 1
                }
            }
        },
    )

    resp = fixture_ot.findings.by_plugin(plugin_id=502387)
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, Finding)
    assert finding.plugin.id == 502387
    assert finding.plugin.severity == "Critical"


@responses.activate
def test_finding_by_id(fixture_ot):
    """
    Tests the findings finding method (get by ID)
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "findings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "specific-finding-id",
                            "status": "Resolved",
                            "firstHit": "2026-03-01T10:00:00Z",
                            "lastHit": "2026-03-02T15:30:00Z",
                            "fixedAt": "2026-03-03T09:00:00Z",
                            "port": 22,
                            "protocol": "tcp",
                            "svcName": "ssh",
                            "output": "Fixed by patch",
                            "asset": {
                                "id": "cccccccc-1111-2222-3333-dddddddddddd",
                                "name": "Fixed Asset",
                                "type": "Switch",
                                "criticality": "HighCriticality",
                                "location": "Datacenter",
                                "purdueLevel": "Level1",
                                "risk": {
                                    "totalRisk": 2.0,
                                    "unresolvedEvents": 0
                                },
                                "ips": {"nodes": ["10.0.0.1"]},
                                "macs": {"nodes": ["AA:BB:CC:DD:EE:FF"]}
                            },
                            "plugin": {
                                "id": 99999,
                                "name": "SSH Vulnerability",
                                "severity": "Medium",
                                "family": "Network",
                                "source": "NNM",
                                "vprScore": 4.5,
                                "comment": "Patched",
                                "owner": "security-team",
                                "details": None
                            }
                        }
                    ],
                    "totalCount": 1
                }
            }
        },
    )

    resp = fixture_ot.findings.finding(finding_id="specific-finding-id")
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, Finding)
    assert finding.id == "specific-finding-id"
    assert finding.status == "Resolved"
    assert finding.fixed_at == datetime.datetime(2026, 3, 3, 9, 0, tzinfo=datetime.timezone.utc)
