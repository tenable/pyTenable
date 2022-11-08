"""
test events
"""
import datetime
import uuid
from ipaddress import IPv4Address

import responses

from tenable.ot.schema.base import AssetInfo, NodesList, AssetInfoList
from tenable.ot.schema.events import (
    Event,
    EventTypeDetails,
    Policy,
    GroupMember,
    Group,
    EventCount,
    ActionList, IDList,
)


@responses.activate
def test_list(fixture_ot):
    """
    Tests the events Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "events": {
                    "nodes": [
                        {
                            "id": "a54444f5-318f-4e2f-92a9-623b69f1c837",
                            "eventType": {
                                "type": "Conversation",
                                "group": "NetworkEvent",
                                "description": "Unauthorized Conversation",
                                "schema": "NetworkSchema",
                                "category": "NetworkEvents",
                                "family": None,
                                "canCapture": True,
                                "actions": [
                                    "ServiceNow",
                                    "FortiGate",
                                    "Email",
                                    "Syslog",
                                ],
                                "exclusion": "Conversation",
                            },
                            "srcIP": "10.100.20.82",
                            "dstIP": "10.100.102.34",
                            "protocolRaw": "ADS_UDP",
                            "policy": {
                                "id": "3fe25234-4509-4c0a-80b8-aa727bdbb8bc",
                                "index": 179,
                                "title": "Use of Unauthorized Protocols in Siemens SIMATIC Controllers",
                                "level": "Medium",
                                "disabled": True,
                                "archived": False,
                                "schema": "NetworkSchema",
                                "continuous": False,
                                "snapshot": False,
                                "system": True,
                                "key": "P3-16",
                                "eventTypeDetails": {
                                    "type": "Conversation",
                                    "group": "NetworkEvent",
                                    "description": "Unauthorized Conversation",
                                    "schema": "NetworkSchema",
                                    "category": "NetworkEvents",
                                    "family": None,
                                    "canCapture": True,
                                    "actions": [
                                        "ServiceNow",
                                        "FortiGate",
                                        "Email",
                                        "Syslog",
                                    ],
                                    "exclusion": "Conversation",
                                },
                                "disableAfterHit": False,
                                "actions": {"nodes": []},
                                "paused": True,
                                "srcAssetGroup": [
                                    [
                                        {
                                            "group": {
                                                "id": "e7ecc8d1-5ca9-478f-b06b-9aaf113b3c65"
                                            },
                                            "negate": False,
                                        }
                                    ]
                                ],
                                "dstAssetGroup": [
                                    [
                                        {
                                            "group": {
                                                "id": "259549cd-23b5-4000-b28f-6b8911c1f08f"
                                            },
                                            "negate": False,
                                        }
                                    ]
                                ],
                                "schedule": {
                                    "group": {
                                        "id": "3f9dbc8c-41ad-42a4-935a-b65fed0a49cb"
                                    },
                                    "negate": False,
                                },
                                "protocolGroup": {
                                    "group": {
                                        "id": "964ce980-d7cb-408f-8185-a69418bb2eb7"
                                    },
                                    "negate": True,
                                },
                                "portGroup": None,
                                "tagGroup": None,
                                "valueGroup": None,
                                "ruleGroup": None,
                                "exclusions": {"nodes": []},
                                "aggregatedEventsCount": {
                                    "last24h": 11,
                                    "last7d": 11,
                                    "last30d": 11,
                                },
                            },
                            "time": "2022-09-11T07:53:51.349315Z",
                            "srcMac": None,
                            "dstMac": None,
                            "completion": "CompletionUnknown",
                            "protocolNiceName": None,
                            "resolved": False,
                            "resolvedTs": None,
                            "hitId": "a54444f5-318f-4e2f-92a9-623b69f1c837",
                            "severity": "Medium",
                            "category": "NetworkEvents",
                            "comment": None,
                            "logId": 288,
                            "resolvedUser": None,
                            "type": "Conversation",
                            "srcAssets": {
                                "nodes": [
                                    {
                                        "name": "Eng. Station #100",
                                        "id": "70716a10-5c52-459e-9bf7-55098585d87b",
                                    }
                                ]
                            },
                            "srcInterface": None,
                            "srcNames": {"nodes": ["Eng. Station #100"]},
                            "dstAssets": {
                                "nodes": [
                                    {
                                        "name": "CPU 412-2 PN/DP",
                                        "id": "2a8e4470-08f0-46df-952a-e3895da5c456",
                                    }
                                ]
                            },
                            "dstInterface": None,
                            "dstNames": {"nodes": ["CPU 412-2 PN/DP"]},
                            "hasDetails": False,
                            "payloadSize": 0,
                            "protocol": "ADS/AMS (udp/48899)",
                            "port": 48899,
                            "continuous": False,
                        }
                    ]
                }
            }
        },
    )

    expected = Event(
        id=uuid.UUID("a54444f5-318f-4e2f-92a9-623b69f1c837"),
        event_type=EventTypeDetails(
            type="Conversation",
            group="NetworkEvent",
            description="Unauthorized Conversation",
            schema="NetworkSchema",
            category="NetworkEvents",
            family=None,
            can_capture=True,
            actions=["ServiceNow", "FortiGate", "Email", "Syslog"],
            exclusion="Conversation",
        ),
        src_ip=IPv4Address("10.100.20.82"),
        dst_ip=IPv4Address("10.100.102.34"),
        protocol_raw="ADS_UDP",
        policy=Policy(
            id=uuid.UUID("3fe25234-4509-4c0a-80b8-aa727bdbb8bc"),
            index=179,
            title="Use of Unauthorized Protocols in Siemens SIMATIC " "Controllers",
            level="Medium",
            disabled=True,
            archived=False,
            schema="NetworkSchema",
            continuous=False,
            snapshot=False,
            system=True,
            key="P3-16",
            event_type_details=EventTypeDetails(
                type="Conversation",
                group="NetworkEvent",
                description="Unauthorized " "Conversation",
                schema="NetworkSchema",
                category="NetworkEvents",
                family=None,
                can_capture=True,
                actions=["ServiceNow", "FortiGate", "Email", "Syslog"],
                exclusion="Conversation",
            ),
            disable_after_hit=False,
            actions=ActionList(nodes=[]),
            paused=True,
            src_asset_group=[
                [
                    GroupMember(
                        group=Group(
                            id=uuid.UUID("e7ecc8d1-5ca9-478f-b06b-9aaf113b3c65"),
                            name=None,
                            type=None,
                            archived=None,
                            system=None,
                            key=None,
                        ),
                        negate=False,
                    )
                ]
            ],
            dst_asset_group=[
                [
                    GroupMember(
                        group=Group(
                            id=uuid.UUID("259549cd-23b5-4000-b28f-6b8911c1f08f"),
                            name=None,
                            type=None,
                            archived=None,
                            system=None,
                            key=None,
                        ),
                        negate=False,
                    )
                ]
            ],
            schedule=GroupMember(
                group=Group(
                    id=uuid.UUID("3f9dbc8c-41ad-42a4-935a-b65fed0a49cb"),
                    name=None,
                    type=None,
                    archived=None,
                    system=None,
                    key=None,
                ),
                negate=False,
            ),
            protocol_group=GroupMember(
                group=Group(
                    id=uuid.UUID("964ce980-d7cb-408f-8185-a69418bb2eb7"),
                    name=None,
                    type=None,
                    archived=None,
                    system=None,
                    key=None,
                ),
                negate=True,
            ),
            port_group=None,
            tag_group=None,
            value_group=None,
            rule_group=None,
            exclusions=IDList(nodes=[]),
            aggregated_events_count=EventCount(last_24h=11, last_7d=11, last_30d=11),
        ),
        time=datetime.datetime(
            2022, 9, 11, 7, 53, 51, 349315, tzinfo=datetime.timezone.utc
        ),
        src_mac=None,
        dst_mac=None,
        completion="CompletionUnknown",
        protocol_nice_name=None,
        resolved=False,
        resolved_ts=None,
        severity="Medium",
        category="NetworkEvents",
        comment=None,
        hit_id=uuid.UUID("a54444f5-318f-4e2f-92a9-623b69f1c837"),
        log_id=288.0,
        resolved_user=None,
        type="Conversation",
        src_assets=AssetInfoList(
            nodes=[
                AssetInfo(
                    id=uuid.UUID("70716a10-5c52-459e-9bf7-55098585d87b"),
                    name="Eng. Station #100",
                )
            ]
        ),
        src_interface=None,
        src_names=NodesList(nodes=["Eng. Station #100"]),
        dst_assets=AssetInfoList(
            nodes=[
                AssetInfo(
                    id=uuid.UUID("2a8e4470-08f0-46df-952a-e3895da5c456"),
                    name="CPU 412-2 PN/DP",
                )
            ]
        ),
        dst_interface=None,
        dst_names=NodesList(nodes=["CPU 412-2 PN/DP"]),
        has_details=False,
        payload_size=0,
        protocol="ADS/AMS (udp/48899)",
        port=48899,
        continuous=False,
    )

    resp = fixture_ot.events.list()
    assert resp.next() == expected
