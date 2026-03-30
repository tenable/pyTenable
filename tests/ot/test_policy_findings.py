"""
test policy findings
"""
import datetime
import uuid

import pytest
import responses

from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.schema.policy_findings import (
    PolicyFinding,
    PolicyFindingAsset,
    PolicyFindingAssets,
    PolicyFindingAssetRisk,
    EventTypeDetails,
    PolicyInfo,
)


@responses.activate
def test_list(fixture_ot):
    """
    Tests the policy findings GraphQL list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "policyFindings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "f5fdbd87-993d-4d81-84b6-ba94fa4f5fe8",
                            "status": "Active",
                            "severity": "Medium",
                            "category": "NetworkEvents",
                            "policyTitle": "SSH Communications to Engineering Stations",
                            "firstHitTime": "2026-02-20T00:27:01.087816Z",
                            "lastHitTime": "2026-02-20T03:02:58.594846Z",
                            "activePolicyHits": 28,
                            "resolvedOn": None,
                            "resolvedUser": None,
                            "srcNames": ["Endpoint #575"],
                            "srcIps": ["192.168.37.117"],
                            "dstNames": ["Eng. Station #1"],
                            "dstIps": ["172.27.52.55"],
                            "eventType": {
                                "type": "Conversation",
                                "description": "Unauthorized Conversation",
                                "category": "NetworkEvents",
                                "family": None
                            },
                            "policy": {
                                "id": "1ab9c93c-3114-4f60-9f3d-d88ba33d332a",
                                "title": "SSH Communications to Engineering Stations",
                                "level": "Medium",
                                "schema": "NetworkSchema",
                                "disabled": False,
                                "archived": False,
                                "system": True
                            },
                            "srcAssets": {
                                "nodes": [
                                    {
                                        "id": "51844e94-48d1-4185-98d4-0b962ec5b966",
                                        "name": "Endpoint #575",
                                        "type": "Unknown",
                                        "criticality": "LowCriticality",
                                        "location": "Building A",
                                        "purdueLevel": "Level3",
                                        "risk": {
                                            "totalRisk": 5.2,
                                            "unresolvedEvents": 5
                                        }
                                    }
                                ]
                            },
                            "dstAssets": {
                                "nodes": []
                            }
                        }
                    ],
                    "totalCount": 181
                }
            }
        },
    )

    expected = PolicyFinding(
        id=uuid.UUID("f5fdbd87-993d-4d81-84b6-ba94fa4f5fe8"),
        status="Active",
        severity="Medium",
        category="NetworkEvents",
        policy_title="SSH Communications to Engineering Stations",
        first_hit_time=datetime.datetime(2026, 2, 20, 0, 27, 1, 87816, tzinfo=datetime.timezone.utc),
        last_hit_time=datetime.datetime(2026, 2, 20, 3, 2, 58, 594846, tzinfo=datetime.timezone.utc),
        active_policy_hits=28,
        resolved_on=None,
        resolved_user=None,
        src_names=["Endpoint #575"],
        src_ips=["192.168.37.117"],
        dst_names=["Eng. Station #1"],
        dst_ips=["172.27.52.55"],
        event_type=EventTypeDetails(
            type="Conversation",
            description="Unauthorized Conversation",
            category="NetworkEvents",
            family=None
        ),
        policy=PolicyInfo(
            id=uuid.UUID("1ab9c93c-3114-4f60-9f3d-d88ba33d332a"),
            title="SSH Communications to Engineering Stations",
            level="Medium",
            schema="NetworkSchema",
            disabled=False,
            archived=False,
            system=True
        ),
        src_assets=PolicyFindingAssets(
            nodes=[
                PolicyFindingAsset(
                    id=uuid.UUID("51844e94-48d1-4185-98d4-0b962ec5b966"),
                    name="Endpoint #575",
                    type="Unknown",
                    criticality="LowCriticality",
                    location="Building A",
                    purdue_level="Level3",
                    risk=PolicyFindingAssetRisk(total_risk=5.2, unresolved_events=5)
                )
            ]
        ),
        dst_assets=PolicyFindingAssets(nodes=[])
    )

    resp = fixture_ot.policy_findings.list()
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, PolicyFinding)
    assert finding == expected


@responses.activate
def test_by_policy(fixture_ot):
    """
    Tests the policy findings by_policy method
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "policyFindings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb",
                            "status": "Active",
                            "severity": "High",
                            "category": "ActivityEvents",
                            "policyTitle": "Test Policy",
                            "firstHitTime": "2026-03-01T10:00:00Z",
                            "lastHitTime": "2026-03-04T15:30:00Z",
                            "activePolicyHits": 5,
                            "resolvedOn": None,
                            "resolvedUser": None,
                            "srcNames": ["Asset A"],
                            "srcIps": ["10.0.1.1"],
                            "dstNames": ["Asset B"],
                            "dstIps": ["10.0.1.2"],
                            "eventType": {
                                "type": "TestEvent",
                                "description": "Test Description",
                                "category": "ActivityEvents",
                                "family": "TestFamily"
                            },
                            "policy": {
                                "id": "1ab9c93c-3114-4f60-9f3d-d88ba33d332a",
                                "title": "Test Policy",
                                "level": "High",
                                "schema": "ActivitySchema",
                                "disabled": False,
                                "archived": False,
                                "system": False
                            },
                            "srcAssets": {
                                "nodes": [
                                    {
                                        "id": "11111111-2222-3333-4444-555555555555",
                                        "name": "Asset A",
                                        "type": "PLC",
                                        "criticality": None,
                                        "location": None,
                                        "purdueLevel": None,
                                        "risk": None
                                    }
                                ]
                            },
                            "dstAssets": {
                                "nodes": [
                                    {
                                        "id": "66666666-7777-8888-9999-000000000000",
                                        "name": "Asset B",
                                        "type": "HMI",
                                        "criticality": None,
                                        "location": None,
                                        "purdueLevel": None,
                                        "risk": None
                                    }
                                ]
                            }
                        }
                    ],
                    "totalCount": 4
                }
            }
        },
    )

    resp = fixture_ot.policy_findings.by_policy(
        policy_id="1ab9c93c-3114-4f60-9f3d-d88ba33d332a",
        status="Active"
    )
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, PolicyFinding)
    assert finding.policy.id == uuid.UUID("1ab9c93c-3114-4f60-9f3d-d88ba33d332a")
    assert finding.policy.title == "Test Policy"
    assert finding.status == "Active"
    assert finding.active_policy_hits == 5


@responses.activate
def test_by_asset_source(fixture_ot):
    """
    Tests the policy findings by_asset method with source direction
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "policyFindings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "bbbbbbbb-2222-3333-4444-cccccccccccc",
                            "status": "Active",
                            "severity": "Low",
                            "category": "NetworkEvents",
                            "policyTitle": "Source Asset Policy",
                            "firstHitTime": "2026-03-04T08:00:00Z",
                            "lastHitTime": "2026-03-04T12:00:00Z",
                            "activePolicyHits": 10,
                            "resolvedOn": None,
                            "resolvedUser": None,
                            "srcNames": ["Test Source Asset"],
                            "srcIps": ["192.168.1.50"],
                            "dstNames": ["Destination"],
                            "dstIps": ["192.168.1.100"],
                            "eventType": {
                                "type": "Communication",
                                "description": "Network Communication",
                                "category": "NetworkEvents",
                                "family": None
                            },
                            "policy": {
                                "id": "cccccccc-3333-4444-5555-dddddddddddd",
                                "title": "Source Asset Policy",
                                "level": "Low",
                                "schema": "NetworkSchema",
                                "disabled": False,
                                "archived": False,
                                "system": False
                            },
                            "srcAssets": {
                                "nodes": [
                                    {
                                        "id": "51844e94-48d1-4185-98d4-0b962ec5b966",
                                        "name": "Test Source Asset",
                                        "type": "Workstation",
                                        "criticality": "MediumCriticality",
                                        "location": "Floor 2",
                                        "purdueLevel": "Level2",
                                        "risk": {
                                            "totalRisk": 3.5,
                                            "unresolvedEvents": 2
                                        }
                                    }
                                ]
                            },
                            "dstAssets": {
                                "nodes": []
                            }
                        }
                    ],
                    "totalCount": 1
                }
            }
        },
    )

    resp = fixture_ot.policy_findings.by_asset(
        asset_id="51844e94-48d1-4185-98d4-0b962ec5b966",
        direction="source"
    )
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, PolicyFinding)
    assert len(finding.src_assets.nodes) == 1
    assert finding.src_assets.nodes[0].id == uuid.UUID("51844e94-48d1-4185-98d4-0b962ec5b966")


@responses.activate
def test_finding_by_id(fixture_ot):
    """
    Tests the policy findings finding method (get by ID)
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "policyFindings": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjA="},
                    "nodes": [
                        {
                            "id": "dddddddd-4444-5555-6666-eeeeeeeeeeee",
                            "status": "Resolved",
                            "severity": "Critical",
                            "category": "SecurityEvents",
                            "policyTitle": "Critical Security Policy",
                            "firstHitTime": "2026-02-15T09:00:00Z",
                            "lastHitTime": "2026-02-16T14:30:00Z",
                            "activePolicyHits": 0,
                            "resolvedOn": "2026-02-17T10:00:00Z",
                            "resolvedUser": "admin@company.com",
                            "srcNames": ["Compromised Asset"],
                            "srcIps": ["192.168.10.50"],
                            "dstNames": ["Protected Asset"],
                            "dstIps": ["192.168.10.100"],
                            "eventType": {
                                "type": "Intrusion",
                                "description": "Intrusion Attempt",
                                "category": "SecurityEvents",
                                "family": "Security"
                            },
                            "policy": {
                                "id": "eeeeeeee-5555-6666-7777-ffffffffffff",
                                "title": "Critical Security Policy",
                                "level": "Critical",
                                "schema": "SecuritySchema",
                                "disabled": False,
                                "archived": False,
                                "system": True
                            },
                            "srcAssets": {
                                "nodes": [
                                    {
                                        "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                                        "name": "Compromised Asset",
                                        "type": "Server",
                                        "criticality": "HighCriticality",
                                        "location": "DMZ",
                                        "purdueLevel": "Level3",
                                        "risk": {
                                            "totalRisk": 9.5,
                                            "unresolvedEvents": 15
                                        }
                                    }
                                ]
                            },
                            "dstAssets": {
                                "nodes": [
                                    {
                                        "id": "11111111-2222-3333-4444-555555555555",
                                        "name": "Protected Asset",
                                        "type": "Controller",
                                        "criticality": "CriticalCriticality",
                                        "location": "Control Room",
                                        "purdueLevel": "Level1",
                                        "risk": {
                                            "totalRisk": 2.0,
                                            "unresolvedEvents": 1
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "totalCount": 1
                }
            }
        },
    )

    resp = fixture_ot.policy_findings.finding(
        finding_id="dddddddd-4444-5555-6666-eeeeeeeeeeee"
    )
    assert isinstance(resp, OTGraphIterator)

    finding = next(resp)
    assert isinstance(finding, PolicyFinding)
    assert finding.id == uuid.UUID("dddddddd-4444-5555-6666-eeeeeeeeeeee")
    assert finding.status == "Resolved"
    assert finding.severity == "Critical"
    assert finding.resolved_user == "admin@company.com"
    assert finding.resolved_on == datetime.datetime(2026, 2, 17, 10, 0, tzinfo=datetime.timezone.utc)
    assert finding.active_policy_hits == 0
