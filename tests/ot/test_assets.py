"""
test assets
"""
import datetime
import uuid

import responses

from tenable.ot.graphql.schema.assets import Asset, Risk, Segment
from tenable.ot.schema.assets import Revisions, Segments
from tenable.ot.schema.base import NodesList


@responses.activate
def test_list(fixture_ot):
    """
    Tests the assets Graphql list iterator
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "assets": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjE5OQ=="},
                    "nodes": [
                        {
                            "category": "ControllersCategory",
                            "criticality": "HighCriticality",
                            "customField1": None,
                            "customField2": None,
                            "customField3": None,
                            "customField4": None,
                            "customField5": None,
                            "customField6": None,
                            "customField7": None,
                            "customField8": None,
                            "customField9": None,
                            "customField10": None,
                            "description": None,
                            "details": {
                                "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                                "name": "Comm. Adapter #110",
                                "firstSeen": "2022-09-11T07:34:54.764844Z",
                                "lastSeen": "2022-09-11T10:39:33.720514Z",
                                "macs": ["f4:54:33:a6:78:c9"],
                                "ips": ["10.100.101.158"],
                                "type": "Cp",
                                "superType": "Controller",
                                "category": "ControllersCategory",
                                "purdueLevel": "Level1",
                                "vendor": "Rockwell",
                                "runStatus": "Unknown",
                                "runStatusTime": "0001-01-01T00:00:00Z",
                                "rawFamily": "MicroLogix1100",
                                "family": "MicroLogix 1100",
                                "modelName": "1763-L16BBB B/11.00",
                                "firmwareVersion": "2.011",
                                "serial": "33A678C9",
                                "risk": 23.87340490112799,
                                "criticality": "HighCriticality",
                                "hidden": False,
                                "lastUpdate": "2022-09-11T10:40:28.234644Z",
                                "cip": {"deviceType": "Communications Adapter"},
                                "classificationIncidents": [
                                    "OuiOtDeviceVendorIncident",
                                    "ConversationIcsProtocolDstIncident",
                                    "DirectConnectorIncident",
                                    "CipIdentityCpIncident",
                                    "NnmCpIncident",
                                ],
                                "names": [
                                    {
                                        "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                                        "source": "Default",
                                        "value": "Comm. Adapter #110",
                                    },
                                    {
                                        "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                                        "source": "Chosen",
                                        "value": "Comm. Adapter #110",
                                    },
                                ],
                                "customFields": [],
                                "directIp": "10.100.101.158",
                                "directIps": None,
                                "directMac": "f4:54:33:a6:78:c9",
                                "directMacs": None,
                                "additionalIp": None,
                                "additionalIps": None,
                                "additionalMac": None,
                                "additionalMacs": None,
                                "stateUpdateTime": "0001-01-01T00:00:00Z",
                                "extendedSegments": [
                                    {
                                        "id": "6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1",
                                        "name": "Controller / 10.100.101.X",
                                        "archived": False,
                                        "system": True,
                                        "key": "AG1-35",
                                        "type": "Segment",
                                        "systemName": "Controller / 10.100.101.X",
                                        "vlan": None,
                                        "description": None,
                                        "isPredefinedName": True,
                                        "subnet": "10.100.101.X",
                                        "assetType": "Controller",
                                    }
                                ],
                                "state": "Unknown",
                                "backplaneName": None,
                            },
                            "family": "MicroLogix 1100",
                            "firmwareVersion": "2.011",
                            "firstSeen": "2022-09-11T07:34:54.764844Z",
                            "hidden": False,
                            "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                            "ips": {"nodes": ["10.100.101.158"]},
                            "lastSeen": "2022-09-11T10:39:33.720514Z",
                            "lastUpdate": "2022-09-11T10:40:28.234644Z",
                            "location": None,
                            "macs": {"nodes": ["f4:54:33:a6:78:c9"]},
                            "model": "1763-L16BBB B/11.00",
                            "name": "Comm. Adapter #110",
                            "os": None,
                            "osDetails": None,
                            "purdueLevel": "Level1",
                            "runStatus": "Unknown",
                            "runStatusTime": "0001-01-01T00:00:00Z",
                            "serial": "33A678C9",
                            "slot": None,
                            "superType": "Controller",
                            "type": "Cp",
                            "vendor": "Rockwell",
                            "risk": {
                                "unresolvedEvents": 0,
                                "totalRisk": 23.87340490112799,
                            },
                            "backplane": None,
                            "segments": {
                                "nodes": [
                                    {
                                        "id": "6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1",
                                        "name": "Controller / 10.100.101.X",
                                        "type": "Segment",
                                        "key": "AG1-35",
                                        "systemName": "Controller / 10.100.101.X",
                                        "vlan": None,
                                        "description": None,
                                        "assetType": "Controller",
                                        "subnet": "10.100.101.X",
                                    }
                                ]
                            },
                            "revisions": {"nodes": []},
                        }
                    ],
                }
            }
        },
    )

    expected = Asset(
        backplane=None,
        category="ControllersCategory",
        criticality="HighCriticality",
        description=None,
        details={
            "additionalIp": None,
            "additionalIps": None,
            "additionalMac": None,
            "additionalMacs": None,
            "backplaneName": None,
            "category": "ControllersCategory",
            "cip": {"deviceType": "Communications Adapter"},
            "classificationIncidents": [
                "OuiOtDeviceVendorIncident",
                "ConversationIcsProtocolDstIncident",
                "DirectConnectorIncident",
                "CipIdentityCpIncident",
                "NnmCpIncident",
            ],
            "criticality": "HighCriticality",
            "customFields": [],
            "directIp": "10.100.101.158",
            "directIps": None,
            "directMac": "f4:54:33:a6:78:c9",
            "directMacs": None,
            "extendedSegments": [
                {
                    "archived": False,
                    "assetType": "Controller",
                    "description": None,
                    "id": "6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1",
                    "isPredefinedName": True,
                    "key": "AG1-35",
                    "name": "Controller / 10.100.101.X",
                    "subnet": "10.100.101.X",
                    "system": True,
                    "systemName": "Controller / 10.100.101.X",
                    "type": "Segment",
                    "vlan": None,
                }
            ],
            "family": "MicroLogix 1100",
            "firmwareVersion": "2.011",
            "firstSeen": "2022-09-11T07:34:54.764844Z",
            "hidden": False,
            "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
            "ips": ["10.100.101.158"],
            "lastSeen": "2022-09-11T10:39:33.720514Z",
            "lastUpdate": "2022-09-11T10:40:28.234644Z",
            "macs": ["f4:54:33:a6:78:c9"],
            "modelName": "1763-L16BBB B/11.00",
            "name": "Comm. Adapter #110",
            "names": [
                {
                    "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                    "source": "Default",
                    "value": "Comm. Adapter #110",
                },
                {
                    "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                    "source": "Chosen",
                    "value": "Comm. Adapter #110",
                },
            ],
            "purdueLevel": "Level1",
            "rawFamily": "MicroLogix1100",
            "risk": 23.87340490112799,
            "runStatus": "Unknown",
            "runStatusTime": "0001-01-01T00:00:00Z",
            "serial": "33A678C9",
            "state": "Unknown",
            "stateUpdateTime": "0001-01-01T00:00:00Z",
            "superType": "Controller",
            "type": "Cp",
            "vendor": "Rockwell",
        },
        family="MicroLogix 1100",
        firmware_version="2.011",
        first_seen=datetime.datetime(
            2022, 9, 11, 7, 34, 54, 764844, tzinfo=datetime.timezone.utc
        ),
        hidden=False,
        id=uuid.UUID("fff9f1b9-26db-4bf4-9d87-bd915aaede36"),
        ips=NodesList(nodes=["10.100.101.158"]),
        last_seen=datetime.datetime(
            2022, 9, 11, 10, 39, 33, 720514, tzinfo=datetime.timezone.utc
        ),
        last_update="2022-09-11T10:40:28.234644Z",
        location=None,
        macs=NodesList(nodes=["f4:54:33:a6:78:c9"]),
        model="1763-L16BBB B/11.00",
        name="Comm. Adapter #110",
        os=None,
        os_details=None,
        purdue_level="Level1",
        revisions=Revisions(nodes=[]),
        risk=Risk(unresolved_events=0, total_risk=23.87340490112799),
        run_status="Unknown",
        run_status_time=datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        segments=Segments(
            nodes=[
                Segment(
                    id=uuid.UUID("6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1"),
                    name="Controller / 10.100.101.X",
                    type="Segment",
                    key="AG1-35",
                    system_name="Controller / 10.100.101.X",
                    vlan=None,
                    description=None,
                    asset_type="Controller",
                    subnet="10.100.101.X",
                )
            ]
        ),
        serial="33A678C9",
        slot=None,
        super_type="Controller",
        type="Cp",
        vendor="Rockwell",
        custom_field1=None,
        custom_field2=None,
        custom_field3=None,
        custom_field4=None,
        custom_field5=None,
        custom_field6=None,
        custom_field7=None,
        custom_field8=None,
        custom_field9=None,
        custom_field10=None,
    )

    resp = fixture_ot.assets.list()
    assert resp.next() == expected


@responses.activate
def test_asset(fixture_ot):
    """
    Tests the assets Graphql asset retriever
    """
    responses.add(
        method="POST",
        url="https://localhost/graphql",
        json={
            "data": {
                "assets": {
                    "pageInfo": {"endCursor": "YXJyYXljb25uZWN0aW9uOjE5OQ=="},
                    "nodes": [
                        {
                            "category": "ControllersCategory",
                            "criticality": "HighCriticality",
                            "customField1": None,
                            "customField2": None,
                            "customField3": None,
                            "customField4": None,
                            "customField5": None,
                            "customField6": None,
                            "customField7": None,
                            "customField8": None,
                            "customField9": None,
                            "customField10": None,
                            "description": None,
                            "details": {
                                "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                                "name": "Comm. Adapter #110",
                                "firstSeen": "2022-09-11T07:34:54.764844Z",
                                "lastSeen": "2022-09-11T10:39:33.720514Z",
                                "macs": ["f4:54:33:a6:78:c9"],
                                "ips": ["10.100.101.158"],
                                "type": "Cp",
                                "superType": "Controller",
                                "category": "ControllersCategory",
                                "purdueLevel": "Level1",
                                "vendor": "Rockwell",
                                "runStatus": "Unknown",
                                "runStatusTime": "0001-01-01T00:00:00Z",
                                "rawFamily": "MicroLogix1100",
                                "family": "MicroLogix 1100",
                                "modelName": "1763-L16BBB B/11.00",
                                "firmwareVersion": "2.011",
                                "serial": "33A678C9",
                                "risk": 23.87340490112799,
                                "criticality": "HighCriticality",
                                "hidden": False,
                                "lastUpdate": "2022-09-11T10:40:28.234644Z",
                                "cip": {"deviceType": "Communications Adapter"},
                                "classificationIncidents": [
                                    "OuiOtDeviceVendorIncident",
                                    "ConversationIcsProtocolDstIncident",
                                    "DirectConnectorIncident",
                                    "CipIdentityCpIncident",
                                    "NnmCpIncident",
                                ],
                                "names": [
                                    {
                                        "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                                        "source": "Default",
                                        "value": "Comm. Adapter #110",
                                    },
                                    {
                                        "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                                        "source": "Chosen",
                                        "value": "Comm. Adapter #110",
                                    },
                                ],
                                "customFields": [],
                                "directIp": "10.100.101.158",
                                "directIps": None,
                                "directMac": "f4:54:33:a6:78:c9",
                                "directMacs": None,
                                "additionalIp": None,
                                "additionalIps": None,
                                "additionalMac": None,
                                "additionalMacs": None,
                                "stateUpdateTime": "0001-01-01T00:00:00Z",
                                "extendedSegments": [
                                    {
                                        "id": "6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1",
                                        "name": "Controller / 10.100.101.X",
                                        "archived": False,
                                        "system": True,
                                        "key": "AG1-35",
                                        "type": "Segment",
                                        "systemName": "Controller / 10.100.101.X",
                                        "vlan": None,
                                        "description": None,
                                        "isPredefinedName": True,
                                        "subnet": "10.100.101.X",
                                        "assetType": "Controller",
                                    }
                                ],
                                "state": "Unknown",
                                "backplaneName": None,
                            },
                            "family": "MicroLogix 1100",
                            "firmwareVersion": "2.011",
                            "firstSeen": "2022-09-11T07:34:54.764844Z",
                            "hidden": False,
                            "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                            "ips": {"nodes": ["10.100.101.158"]},
                            "lastSeen": "2022-09-11T10:39:33.720514Z",
                            "lastUpdate": "2022-09-11T10:40:28.234644Z",
                            "location": None,
                            "macs": {"nodes": ["f4:54:33:a6:78:c9"]},
                            "model": "1763-L16BBB B/11.00",
                            "name": "Comm. Adapter #110",
                            "os": None,
                            "osDetails": None,
                            "purdueLevel": "Level1",
                            "runStatus": "Unknown",
                            "runStatusTime": "0001-01-01T00:00:00Z",
                            "serial": "33A678C9",
                            "slot": None,
                            "superType": "Controller",
                            "type": "Cp",
                            "vendor": "Rockwell",
                            "risk": {
                                "unresolvedEvents": 0,
                                "totalRisk": 23.87340490112799,
                            },
                            "backplane": None,
                            "segments": {
                                "nodes": [
                                    {
                                        "id": "6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1",
                                        "name": "Controller / 10.100.101.X",
                                        "type": "Segment",
                                        "key": "AG1-35",
                                        "systemName": "Controller / 10.100.101.X",
                                        "vlan": None,
                                        "description": None,
                                        "assetType": "Controller",
                                        "subnet": "10.100.101.X",
                                    }
                                ]
                            },
                            "revisions": {"nodes": []},
                        },
                    ],
                }
            }
        },
    )

    expected = Asset(
        backplane=None,
        category="ControllersCategory",
        criticality="HighCriticality",
        description=None,
        details={
            "additionalIp": None,
            "additionalIps": None,
            "additionalMac": None,
            "additionalMacs": None,
            "backplaneName": None,
            "category": "ControllersCategory",
            "cip": {"deviceType": "Communications Adapter"},
            "classificationIncidents": [
                "OuiOtDeviceVendorIncident",
                "ConversationIcsProtocolDstIncident",
                "DirectConnectorIncident",
                "CipIdentityCpIncident",
                "NnmCpIncident",
            ],
            "criticality": "HighCriticality",
            "customFields": [],
            "directIp": "10.100.101.158",
            "directIps": None,
            "directMac": "f4:54:33:a6:78:c9",
            "directMacs": None,
            "extendedSegments": [
                {
                    "archived": False,
                    "assetType": "Controller",
                    "description": None,
                    "id": "6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1",
                    "isPredefinedName": True,
                    "key": "AG1-35",
                    "name": "Controller / 10.100.101.X",
                    "subnet": "10.100.101.X",
                    "system": True,
                    "systemName": "Controller / 10.100.101.X",
                    "type": "Segment",
                    "vlan": None,
                }
            ],
            "family": "MicroLogix 1100",
            "firmwareVersion": "2.011",
            "firstSeen": "2022-09-11T07:34:54.764844Z",
            "hidden": False,
            "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
            "ips": ["10.100.101.158"],
            "lastSeen": "2022-09-11T10:39:33.720514Z",
            "lastUpdate": "2022-09-11T10:40:28.234644Z",
            "macs": ["f4:54:33:a6:78:c9"],
            "modelName": "1763-L16BBB B/11.00",
            "name": "Comm. Adapter #110",
            "names": [
                {
                    "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                    "source": "Default",
                    "value": "Comm. Adapter #110",
                },
                {
                    "id": "fff9f1b9-26db-4bf4-9d87-bd915aaede36",
                    "source": "Chosen",
                    "value": "Comm. Adapter #110",
                },
            ],
            "purdueLevel": "Level1",
            "rawFamily": "MicroLogix1100",
            "risk": 23.87340490112799,
            "runStatus": "Unknown",
            "runStatusTime": "0001-01-01T00:00:00Z",
            "serial": "33A678C9",
            "state": "Unknown",
            "stateUpdateTime": "0001-01-01T00:00:00Z",
            "superType": "Controller",
            "type": "Cp",
            "vendor": "Rockwell",
        },
        family="MicroLogix 1100",
        firmware_version="2.011",
        first_seen=datetime.datetime(
            2022, 9, 11, 7, 34, 54, 764844, tzinfo=datetime.timezone.utc
        ),
        hidden=False,
        id=uuid.UUID("fff9f1b9-26db-4bf4-9d87-bd915aaede36"),
        ips=NodesList(nodes=["10.100.101.158"]),
        last_seen=datetime.datetime(
            2022, 9, 11, 10, 39, 33, 720514, tzinfo=datetime.timezone.utc
        ),
        last_update="2022-09-11T10:40:28.234644Z",
        location=None,
        macs=NodesList(nodes=["f4:54:33:a6:78:c9"]),
        model="1763-L16BBB B/11.00",
        name="Comm. Adapter #110",
        os=None,
        os_details=None,
        purdue_level="Level1",
        revisions=Revisions(nodes=[]),
        risk=Risk(unresolved_events=0, total_risk=23.87340490112799),
        run_status="Unknown",
        run_status_time=datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        segments=Segments(
            nodes=[
                Segment(
                    id=uuid.UUID("6cd69f4e-6e68-4af0-b9ae-5d24b4ed4eb1"),
                    name="Controller / 10.100.101.X",
                    type="Segment",
                    key="AG1-35",
                    system_name="Controller / 10.100.101.X",
                    vlan=None,
                    description=None,
                    asset_type="Controller",
                    subnet="10.100.101.X",
                )
            ]
        ),
        serial="33A678C9",
        slot=None,
        super_type="Controller",
        type="Cp",
        vendor="Rockwell",
        custom_field1=None,
        custom_field2=None,
        custom_field3=None,
        custom_field4=None,
        custom_field5=None,
        custom_field6=None,
        custom_field7=None,
        custom_field8=None,
        custom_field9=None,
        custom_field10=None,
    )

    resp = fixture_ot.assets.asset("fff9f1b9-26db-4bf4-9d87-bd915aaede36")
    assert resp.next() == expected
