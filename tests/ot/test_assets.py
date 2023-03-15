"""
test assets
"""
import datetime
import uuid

import pytest
import responses

from tenable.ot.graphql.iterators import OTGraphIterator
from tenable.ot.graphql.schema.assets import Asset, Risk, Segment
from tenable.ot.graphql.schema.plugins import Plugin
from tenable.ot.schema.assets import Revisions, Segments, Hotfix, HotFixes, OSDetails
from tenable.ot.schema.base import NodesList
from tenable.ot.schema.plugins import Plugins


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
                            "category": "NetworkAssetsCategory",
                            "criticality": "LowCriticality",
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
                                "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                                "name": "STEP7",
                                "firstSeen": "2021-04-11T21:00:09.154979Z",
                                "lastSeen": "2021-06-25T13:02:37.178997Z",
                                "macs": [],
                                "ips": ["10.100.30.37"],
                                "type": "Server",
                                "superType": "Server",
                                "category": "NetworkAssetsCategory",
                                "purdueLevel": "Level3",
                                "runStatus": "Unknown",
                                "runStatusTime": "0001-01-01T00:00:00Z",
                                "os": "Windows Server 2008 R2",
                                "rawFamily": "UnknownFamily",
                                "risk": 0,
                                "criticality": "LowCriticality",
                                "hidden": True,
                                "lastUpdate": "2022-10-04T02:18:54.78456Z",
                                "classificationIncidents": [
                                    "DirectConnectorIncident",
                                    "WindowsServerWmiIncident",
                                ],
                                "hardware": {
                                    "numOfProcessors": "2",
                                    "cpu": "Intel(R) Xeon(R) Silver 4114 CPU @ 2.20GHz",
                                    "cpuSpeed": 2597,
                                    "cpuLoad": 2,
                                    "cpuArchitecture": "x64",
                                    "cpuRevision": 16128,
                                    "totalPhysicalMemory": 2146951168,
                                    "usedPhysicalMemory": 952430592,
                                    "freePhysicalMemory": 1194520576,
                                    "totalVirtualMemory": 4293902336,
                                    "usedVirtualMemory": 2070228992,
                                    "freeVirtualMemory": 2223673344,
                                    "biosVersion": "6.00",
                                    "biosSerial": "VMware-42 12 e4 83 95 a1 87 7a-07 1c c1 c2 05 a6 41 81",
                                    "biosMajor": 2,
                                    "biosMinor": 4,
                                    "csManufacturer": "VMware, Inc.",
                                    "csModel": "VMware Virtual Platform",
                                    "devicesAndDrives": [
                                        {
                                            "name": "System Reserved",
                                            "capacity": 104853504,
                                            "driveLetter": "",
                                            "deviceType": "Unknown",
                                        },
                                        {
                                            "name": "",
                                            "capacity": 42842714112,
                                            "driveLetter": "C:",
                                            "deviceType": "Unknown",
                                        },
                                        {
                                            "name": "",
                                            "capacity": 0,
                                            "driveLetter": "D:",
                                            "deviceType": "Unknown",
                                        },
                                    ],
                                },
                                "names": [
                                    {
                                        "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                                        "source": "Default",
                                        "value": "Server #7",
                                    },
                                    {
                                        "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                                        "source": "Wmi",
                                        "value": "STEP7",
                                    },
                                    {
                                        "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                                        "source": "Chosen",
                                        "value": "STEP7",
                                    },
                                    {
                                        "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                                        "source": "Dns",
                                        "value": "ipaserver.indegy.local",
                                    },
                                ],
                                "windows": {
                                    "osName": "Microsoft Windows Server 2008 R2 Standard ",
                                    "computerName": "STEP7",
                                    "version": "6.1.7601",
                                    "servicepackMajor": 1,
                                    "servicepackMinor": 0,
                                    "buildType": "Multiprocessor Free",
                                    "buildNumber": "7601",
                                    "osArchitecture": "64-bit",
                                    "serialNumber": "55041-507-9059273-84698",
                                    "registeredUser": "Windows User",
                                    "installDate": "2016-01-04T00:26:08Z",
                                    "lastBootUpTime": "2021-01-30T16:13:42.359599Z",
                                    "csDomain": "WORKGROUP",
                                    "hotFixes": [
                                        {
                                            "hotFixId": "KB4019990",
                                            "installedOn": "2018-05-27T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB4095874",
                                            "installedOn": "2018-05-27T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB4103718",
                                            "installedOn": "2018-05-27T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB4103768",
                                            "installedOn": "2018-05-27T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3167679",
                                            "installedOn": "2016-08-31T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3177723",
                                            "installedOn": "2016-08-31T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3163245",
                                            "installedOn": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3168965",
                                            "installedOn": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3170455",
                                            "installedOn": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3175443",
                                            "installedOn": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3177725",
                                            "installedOn": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3178034",
                                            "installedOn": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3142024",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3153171",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3156016",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3156017",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3156019",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3159398",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3160005",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3161561",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3161664",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3161949",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3161958",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3162835",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3164033",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3164035",
                                            "installedOn": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3135983",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3138612",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3139398",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3139914",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3139940",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3140735",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3142042",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3145739",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3146706",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3146963",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3148198",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3148851",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3149090",
                                            "installedOn": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3122648",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3126587",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3126593",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3127220",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3133043",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3134214",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3134814",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3141092",
                                            "installedOn": "2016-03-28T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3072305",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3108664",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3109560",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3110329",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3121212",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3121918",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3123479",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3124000",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3124001",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3124275",
                                            "installedOn": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB917607",
                                            "installedOn": "2016-02-02T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2670838",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2729094",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2834140",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2841134",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2849696",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2849697",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2882822",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2912390",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2973351",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3042058",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3104002",
                                            "installedOn": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2506014",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2506212",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2509553",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2511455",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2536275",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2544893",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2552343",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2560656",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2564958",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2570947",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2585542",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2604115",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2620704",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2621440",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2631813",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2643719",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2653956",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2654428",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2656356",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2667402",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2676562",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2685939",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2690533",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2698365",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2705219",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2706045",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2712808",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2718704",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2729452",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2736422",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2742599",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2758857",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2765809",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2770660",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2786081",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2789645",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2798162",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2807986",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2813430",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2836942",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2836943",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2839894",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2840149",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2840631",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2861698",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2862152",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2862330",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2862335",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2862973",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2864202",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2868038",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2868116",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2868626",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2871997",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2884256",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2887069",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2892074",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2893294",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2894844",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2900986",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2911501",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2929733",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB2931356",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2937610",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2943357",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2957189",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2968294",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2972100",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2972211",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2973112",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2973201",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2976897",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2977292",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2978120",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2984972",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2991963",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2992611",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB2993651",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3000483",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3003743",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3004361",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3004375",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3005607",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3006226",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3010788",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3011780",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3014029",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3018238",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3019978",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3020369",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB3021674",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3022777",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3023215",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3030377",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3031432",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3032655",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3033889",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3033929",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3035126",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3035132",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3037574",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3042553",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3045685",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3046017",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3046269",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3055642",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3059317",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3060716",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3061518",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3068457",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3069392",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3071756",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3072595",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3072630",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3072633",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3074543",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3075220",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3076895",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3078601",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3080446",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3081320",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3084135",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3086255",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3087039",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3092601",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3097966",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3097989",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3099862",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3101246",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3101722",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3101746",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3108371",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3108381",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3108670",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3109094",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3109103",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "hotFixId": "KB3112343",
                                            "installedOn": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "hotFixId": "KB976902",
                                            "installedOn": "2010-11-21T00:00:00Z",
                                            "description": "Update",
                                        },
                                    ],
                                    "installedSoftware": [
                                        {
                                            "name": "Microsoft Application Error Reporting",
                                            "version": "12.0.6012.5000",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Sql Server Customer Experience Improvement Program",
                                            "version": "10.50.1600.1",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC  STEP 7 V5.5 + SP4  ",
                                            "version": "05.05.0400",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "OPC .NET API 2.00 Redistributables (x86) 101.0",
                                            "version": "2.00.10200",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219",
                                            "version": "10.0.40219",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.20.27508",
                                            "version": "14.20.27508",
                                            "installDate": "Jan 16 2020",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219",
                                            "version": "10.0.40219",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - HM NoBasic Single SetupPackage  V13.0 SP1 UPD7",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "SIMATIC S7-PCT V3.2  ",
                                            "version": "03.02.0000",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "NETLink-S7-NET",
                                            "version": "3.5.0.3",
                                            "installDate": "Aug 17 2020",
                                        },
                                        {
                                            "name": "SQL Server 2008 R2 SP2 Database Engine Services",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SQL Server 2008 R2 SP2 Database Engine Services",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2005 Redistributable",
                                            "version": "8.0.59193",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft SQL Server 2008 Setup Support Files ",
                                            "version": "10.1.2731.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft SQL Server 2008 R2 RsFx Driver",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - HM All Editions Single SetupPackage  V13.0 SP1 UPD7",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.20.27508",
                                            "version": "14.20.27508",
                                            "installDate": "Jan 16 2020",
                                        },
                                        {
                                            "name": "SIMATIC WinCC/Audit Viewer 2008 SP2  ",
                                            "version": "07.02.0000",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - TIA Tour Single SetupPackage  V13.0 + SP1",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC S7-Web2PLC V1.0 + SP2 + HF1  ",
                                            "version": "01.00.0201",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package WCF-01  V13.0",
                                            "version": "13.00.0000",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "OPC Core Components Redistributable (x86) 101.2",
                                            "version": "3.00.10102",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2013 x64 Additional Runtime - 12.0.21005",
                                            "version": "12.0.21005",
                                            "installDate": "Apr 20 2016",
                                        },
                                        {
                                            "name": "Microsoft .NET Framework 4.5.2",
                                            "version": "4.5.51209",
                                            "installDate": "May 27 2018",
                                        },
                                        {
                                            "name": "SQL Server 2008 R2 SP2 Common Files",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161",
                                            "version": "9.0.30729.6161",
                                            "installDate": "Jan 3 2016",
                                        },
                                        {
                                            "name": "WinCC Runtime Advanced V13.0 SP1 -  SIMATIC WinCC Runtime Advanced  V13.0 + SP1",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161",
                                            "version": "9.0.30729.6161",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "MSXML 4.0 SP2 (KB973688)",
                                            "version": "4.20.9876.0",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2013 x64 Minimum Runtime - 12.0.21005",
                                            "version": "12.0.21005",
                                            "installDate": "Apr 20 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 03  V13.0",
                                            "version": "13.00.0000",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2012 x64 Additional Runtime - 11.0.61030",
                                            "version": "11.0.61030",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft SQL Server Browser",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                                            "version": "8.0.56336",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Totally Integrated Automation Portal V13 -  TIA Portal Single SetupPackage  V13.0 + SP1",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "SQL Server 2008 R2 SP2 Common Files",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Siemens Automation License Manager V5.3 + SP2 + Upd2  ",
                                            "version": "05.03.0202",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft SQL Server 2008 R2 Native Client",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2019 X86 Additional Runtime - 14.20.27508",
                                            "version": "14.20.27508",
                                            "installDate": "Jan 16 2020",
                                        },
                                        {
                                            "name": "WinCC Runtime Advanced V13.0 SP1 - HMIRTM Simulation Single SetupPackage  V13.0 SP1 UPD7",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - Simatic Single SetupPackage  V13.0 SP1 UPD7",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 0  V13.0",
                                            "version": "13.00.0000",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Primary Interoperability Assemblies 2005",
                                            "version": "8.0.50727.42",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 02  V13.0",
                                            "version": "13.00.0000",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                                            "version": "8.0.59192",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft SQL Server 2008 R2 Setup (English)",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft SOAP Toolkit 3.0",
                                            "version": "3.0.1325.4",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC Prosave V13.0 SP1  ",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "License Logon Interface",
                                            "version": "04.00.0300",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC Process Diagnosis Database",
                                            "version": "5.3",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC DIAGNOSTIC REPEATER GUI CTRL",
                                            "version": "05.02.0300",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.17",
                                            "version": "9.0.30729",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2005 Redistributable",
                                            "version": "8.0.56336",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148",
                                            "version": "9.0.30729.4148",
                                            "installDate": "Jan 3 2016",
                                        },
                                        {
                                            "name": "Automation Software Updater",
                                            "version": "02.05.0000",
                                            "installDate": "Feb 3 2020",
                                        },
                                        {
                                            "name": "MSXML 4.0 SP2 (KB954430)",
                                            "version": "4.20.9870.0",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "SeCon",
                                            "version": "02.02.0000",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "VMware Tools",
                                            "version": "11.0.1.14773994",
                                            "installDate": "Jan 16 2020",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2019 X64 Additional Runtime - 14.20.27508",
                                            "version": "14.20.27508",
                                            "installDate": "Jan 16 2020",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.17",
                                            "version": "9.0.30729",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC Extended Interfaces",
                                            "version": "05.04.0600",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC Colour Editor",
                                            "version": "05.01.1600",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC NCM FWL 64",
                                            "version": "05.05.0400",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "PKZIP Server for Windows 12.40.0008",
                                            "version": "12.40.0008",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - TIACOMPCHECK Single SetupPackage  V13.0 + SP1 + Upd7",
                                            "version": "13.00.0107",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "SIMATIC Device Drivers WoW",
                                            "version": "29.00.0700",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "SIMATIC Process Diagnosis Base",
                                            "version": "5.3",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC HMI Symbol Library",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2012 x86 Minimum Runtime - 11.0.61030",
                                            "version": "11.0.61030",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC Device Drivers",
                                            "version": "09.00.0700",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "SIMATIC Interface Editor",
                                            "version": "05.04.1800",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC HMI Touch Input",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2012 x86 Additional Runtime - 11.0.61030",
                                            "version": "11.0.61030",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "WinCC Runtime Advanced Simulator",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC Grid Control",
                                            "version": "02.06.0000",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC GSD CONTROL",
                                            "version": "03.05.0600",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC HMI ProSave",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "OPC UA SDK 1.1 Redistributables 331.0",
                                            "version": "1.01.33100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC HMI License Manager Panel Plugin (x64)",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC GSD Interpreter",
                                            "version": "02.04.0200",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC Common Services",
                                            "version": "05.03.1500",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC NCM",
                                            "version": "05.05.0400",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC WinCC Runtime Advanced Driver (x64)",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC LanguageSupportTool",
                                            "version": "05.08.0300",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC Version View",
                                            "version": "01.07.0900",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "Siemens  Totally Integrated Automation Portal V13 - WinCC Single SetupPackage  V13.0 SP1 UPD7",
                                            "version": "13.00.0100",
                                            "installDate": "Feb 9 2016",
                                        },
                                        {
                                            "name": "Microsoft Visual C++ 2012 x64 Minimum Runtime - 11.0.61030",
                                            "version": "11.0.61030",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIEMENS OPC",
                                            "version": "03.09.0502",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC Event Database",
                                            "version": "05.05.0402",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "SIMATIC X-Ref Control",
                                            "version": "05.02.0800",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC S7-Block Privacy V1.0 + SP3  ",
                                            "version": "01.00.0300",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "VC User 71 RTL X86 ---",
                                            "version": "1.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                        {
                                            "name": "Automation Access Control Component",
                                            "version": "04.00.0100",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC S7-Status-OCX",
                                            "version": "05.03.1100",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "SIMATIC Technological Parameter Assignment",
                                            "version": "05.03.1100",
                                            "installDate": "Jul 10 2017",
                                        },
                                        {
                                            "name": "Microsoft SQL Server VSS Writer",
                                            "version": "10.52.4000.0",
                                            "installDate": "Feb 2 2016",
                                        },
                                    ],
                                },
                                "customFields": [
                                    ["customField1", "Building", "PlainText"],
                                    ["customField10", "Line", "PlainText"],
                                    ["customField2", "Point of Contact", "PlainText"],
                                    ["customField4", "Vertical", "PlainText"],
                                    ["customField5", "Geo-Location", "HyperLink"],
                                    ["customField7", "Revisions", "PlainText"],
                                    ["customField8", "Temp", "PlainText"],
                                    ["customField6", "TAGS OR OTHER NAME", "PlainText"],
                                    ["customField3", "map", "HyperLink"],
                                ],
                                "directIp": "10.100.30.37",
                                "directIps": None,
                                "directMac": None,
                                "directMacs": None,
                                "additionalIp": None,
                                "additionalIps": None,
                                "additionalMac": None,
                                "additionalMacs": None,
                                "stateUpdateTime": "0001-01-01T00:00:00Z",
                                "extendedSegments": [
                                    {
                                        "id": "59161089-c6f7-4f8c-90a3-92f5be9d3b9d",
                                        "name": "Server / 10.100.30.X",
                                        "archived": False,
                                        "system": True,
                                        "key": "AG1-20",
                                        "type": "Segment",
                                        "systemName": "Server / 10.100.30.X",
                                        "vlan": None,
                                        "description": None,
                                        "isPredefinedName": True,
                                        "subnet": "10.100.30.X",
                                        "assetType": "Server",
                                    }
                                ],
                                "state": "Unknown",
                                "backplaneName": None,
                                "hotFixes": {
                                    "columns": [
                                        {"field": "Id"},
                                        {"field": "Description"},
                                        {"field": "Installed Date"},
                                    ],
                                    "data": [
                                        {
                                            "Id": "KB4019990",
                                            "Description": "Update",
                                            "Installed Date": "2018-05-27T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB4095874",
                                            "Description": "Update",
                                            "Installed Date": "2018-05-27T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB4103718",
                                            "Description": "Security Update",
                                            "Installed Date": "2018-05-27T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB4103768",
                                            "Description": "Security Update",
                                            "Installed Date": "2018-05-27T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3167679",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-08-31T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3177723",
                                            "Description": "Update",
                                            "Installed Date": "2016-08-31T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3163245",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-08-29T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3168965",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-08-29T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3170455",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-08-29T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3175443",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-08-29T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3177725",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-08-29T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3178034",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-08-29T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3142024",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3153171",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3156016",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3156017",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3156019",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3159398",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3160005",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3161561",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3161664",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3161949",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3161958",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3162835",
                                            "Description": "Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3164033",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3164035",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-06-16T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3135983",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3138612",
                                            "Description": "Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3139398",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3139914",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3139940",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3140735",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3142042",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3145739",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3146706",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3146963",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3148198",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3148851",
                                            "Description": "Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3149090",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-04-20T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3122648",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3126587",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3126593",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3127220",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3133043",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3134214",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3134814",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3141092",
                                            "Description": "Update",
                                            "Installed Date": "2016-03-28T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3072305",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3108664",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3109560",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3110329",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3121212",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3121918",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3123479",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3124000",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3124001",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3124275",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-02-09T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB917607",
                                            "Description": "Update",
                                            "Installed Date": "2016-02-02T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2670838",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2729094",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2834140",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2841134",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2849696",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2849697",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2882822",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2912390",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2973351",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3042058",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3104002",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-04T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2506014",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2506212",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2509553",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2511455",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2536275",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2544893",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2552343",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2560656",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2564958",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2570947",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2585542",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2604115",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2620704",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2621440",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2631813",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2643719",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2653956",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2654428",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2656356",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2667402",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2676562",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2685939",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2690533",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2698365",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2705219",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2706045",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2712808",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2718704",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2729452",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2736422",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2742599",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2758857",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2765809",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2770660",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2786081",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2789645",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2798162",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2807986",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2813430",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2836942",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2836943",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2839894",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2840149",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2840631",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2861698",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2862152",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2862330",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2862335",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2862973",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2864202",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2868038",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2868116",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2868626",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2871997",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2884256",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2887069",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2892074",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2893294",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2894844",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2900986",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2911501",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2929733",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2931356",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2937610",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2943357",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2957189",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2968294",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2972100",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2972211",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2973112",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2973201",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2976897",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2977292",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2978120",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2984972",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2991963",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2992611",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB2993651",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3000483",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3003743",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3004361",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3004375",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3005607",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3006226",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3010788",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3011780",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3014029",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3018238",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3019978",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3020369",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3021674",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3022777",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3023215",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3030377",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3031432",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3032655",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3033889",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3033929",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3035126",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3035132",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3037574",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3042553",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3045685",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3046017",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3046269",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3055642",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3059317",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3060716",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3061518",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3068457",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3069392",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3071756",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3072595",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3072630",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3072633",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3074543",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3075220",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3076895",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3078601",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3080446",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3081320",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3084135",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3086255",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3087039",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3092601",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3097966",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3097989",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3099862",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3101246",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3101722",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3101746",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3108371",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3108381",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3108670",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3109094",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3109103",
                                            "Description": "Security Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB3112343",
                                            "Description": "Update",
                                            "Installed Date": "2016-01-03T00:00:00Z",
                                        },
                                        {
                                            "Id": "KB976902",
                                            "Description": "Update",
                                            "Installed Date": "2010-11-21T00:00:00Z",
                                        },
                                    ],
                                },
                                "installedSoftware": {
                                    "columns": [
                                        {"field": "Name"},
                                        {"field": "Version"},
                                        {"field": "Installed Date"},
                                    ],
                                    "data": [
                                        {
                                            "Name": "Microsoft Application Error Reporting",
                                            "Version": "12.0.6012.5000",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Sql Server Customer Experience Improvement Program",
                                            "Version": "10.50.1600.1",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC  STEP 7 V5.5 + SP4  ",
                                            "Version": "05.05.0400",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "OPC .NET API 2.00 Redistributables (x86) 101.0",
                                            "Version": "2.00.10200",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219",
                                            "Version": "10.0.40219",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.20.27508",
                                            "Version": "14.20.27508",
                                            "Installed Date": "Jan 16 2020",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219",
                                            "Version": "10.0.40219",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - HM NoBasic Single SetupPackage  V13.0 SP1 UPD7",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "SIMATIC S7-PCT V3.2  ",
                                            "Version": "03.02.0000",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "NETLink-S7-NET",
                                            "Version": "3.5.0.3",
                                            "Installed Date": "Aug 17 2020",
                                        },
                                        {
                                            "Name": "SQL Server 2008 R2 SP2 Database Engine Services",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SQL Server 2008 R2 SP2 Database Engine Services",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2005 Redistributable",
                                            "Version": "8.0.59193",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft SQL Server 2008 Setup Support Files ",
                                            "Version": "10.1.2731.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft SQL Server 2008 R2 RsFx Driver",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - HM All Editions Single SetupPackage  V13.0 SP1 UPD7",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.20.27508",
                                            "Version": "14.20.27508",
                                            "Installed Date": "Jan 16 2020",
                                        },
                                        {
                                            "Name": "SIMATIC WinCC/Audit Viewer 2008 SP2  ",
                                            "Version": "07.02.0000",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - TIA Tour Single SetupPackage  V13.0 + SP1",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC S7-Web2PLC V1.0 + SP2 + HF1  ",
                                            "Version": "01.00.0201",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package WCF-01  V13.0",
                                            "Version": "13.00.0000",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "OPC Core Components Redistributable (x86) 101.2",
                                            "Version": "3.00.10102",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2013 x64 Additional Runtime - 12.0.21005",
                                            "Version": "12.0.21005",
                                            "Installed Date": "Apr 20 2016",
                                        },
                                        {
                                            "Name": "Microsoft .NET Framework 4.5.2",
                                            "Version": "4.5.51209",
                                            "Installed Date": "May 27 2018",
                                        },
                                        {
                                            "Name": "SQL Server 2008 R2 SP2 Common Files",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161",
                                            "Version": "9.0.30729.6161",
                                            "Installed Date": "Jan 3 2016",
                                        },
                                        {
                                            "Name": "WinCC Runtime Advanced V13.0 SP1 -  SIMATIC WinCC Runtime Advanced  V13.0 + SP1",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161",
                                            "Version": "9.0.30729.6161",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "MSXML 4.0 SP2 (KB973688)",
                                            "Version": "4.20.9876.0",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2013 x64 Minimum Runtime - 12.0.21005",
                                            "Version": "12.0.21005",
                                            "Installed Date": "Apr 20 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 03  V13.0",
                                            "Version": "13.00.0000",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2012 x64 Additional Runtime - 11.0.61030",
                                            "Version": "11.0.61030",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft SQL Server Browser",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                                            "Version": "8.0.56336",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Totally Integrated Automation Portal V13 -  TIA Portal Single SetupPackage  V13.0 + SP1",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "SQL Server 2008 R2 SP2 Common Files",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Siemens Automation License Manager V5.3 + SP2 + Upd2  ",
                                            "Version": "05.03.0202",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft SQL Server 2008 R2 Native Client",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2019 X86 Additional Runtime - 14.20.27508",
                                            "Version": "14.20.27508",
                                            "Installed Date": "Jan 16 2020",
                                        },
                                        {
                                            "Name": "WinCC Runtime Advanced V13.0 SP1 - HMIRTM Simulation Single SetupPackage  V13.0 SP1 UPD7",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - Simatic Single SetupPackage  V13.0 SP1 UPD7",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 0  V13.0",
                                            "Version": "13.00.0000",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Primary Interoperability Assemblies 2005",
                                            "Version": "8.0.50727.42",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 02  V13.0",
                                            "Version": "13.00.0000",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                                            "Version": "8.0.59192",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft SQL Server 2008 R2 Setup (English)",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft SOAP Toolkit 3.0",
                                            "Version": "3.0.1325.4",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Prosave V13.0 SP1  ",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "License Logon Interface",
                                            "Version": "04.00.0300",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC Process Diagnosis Database",
                                            "Version": "5.3",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC DIAGNOSTIC REPEATER GUI CTRL",
                                            "Version": "05.02.0300",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.17",
                                            "Version": "9.0.30729",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2005 Redistributable",
                                            "Version": "8.0.56336",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148",
                                            "Version": "9.0.30729.4148",
                                            "Installed Date": "Jan 3 2016",
                                        },
                                        {
                                            "Name": "Automation Software Updater",
                                            "Version": "02.05.0000",
                                            "Installed Date": "Feb 3 2020",
                                        },
                                        {
                                            "Name": "MSXML 4.0 SP2 (KB954430)",
                                            "Version": "4.20.9870.0",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "SeCon",
                                            "Version": "02.02.0000",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "VMware Tools",
                                            "Version": "11.0.1.14773994",
                                            "Installed Date": "Jan 16 2020",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2019 X64 Additional Runtime - 14.20.27508",
                                            "Version": "14.20.27508",
                                            "Installed Date": "Jan 16 2020",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.17",
                                            "Version": "9.0.30729",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Extended Interfaces",
                                            "Version": "05.04.0600",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC Colour Editor",
                                            "Version": "05.01.1600",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC NCM FWL 64",
                                            "Version": "05.05.0400",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "PKZIP Server for Windows 12.40.0008",
                                            "Version": "12.40.0008",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - TIACOMPCHECK Single SetupPackage  V13.0 + SP1 + Upd7",
                                            "Version": "13.00.0107",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Device Drivers WoW",
                                            "Version": "29.00.0700",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Process Diagnosis Base",
                                            "Version": "5.3",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC HMI Symbol Library",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2012 x86 Minimum Runtime - 11.0.61030",
                                            "Version": "11.0.61030",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Device Drivers",
                                            "Version": "09.00.0700",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Interface Editor",
                                            "Version": "05.04.1800",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC HMI Touch Input",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2012 x86 Additional Runtime - 11.0.61030",
                                            "Version": "11.0.61030",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "WinCC Runtime Advanced Simulator",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Grid Control",
                                            "Version": "02.06.0000",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC GSD CONTROL",
                                            "Version": "03.05.0600",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC HMI ProSave",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "OPC UA SDK 1.1 Redistributables 331.0",
                                            "Version": "1.01.33100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC HMI License Manager Panel Plugin (x64)",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC GSD Interpreter",
                                            "Version": "02.04.0200",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC Common Services",
                                            "Version": "05.03.1500",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC NCM",
                                            "Version": "05.05.0400",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC WinCC Runtime Advanced Driver (x64)",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC LanguageSupportTool",
                                            "Version": "05.08.0300",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC Version View",
                                            "Version": "01.07.0900",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "Siemens  Totally Integrated Automation Portal V13 - WinCC Single SetupPackage  V13.0 SP1 UPD7",
                                            "Version": "13.00.0100",
                                            "Installed Date": "Feb 9 2016",
                                        },
                                        {
                                            "Name": "Microsoft Visual C++ 2012 x64 Minimum Runtime - 11.0.61030",
                                            "Version": "11.0.61030",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIEMENS OPC",
                                            "Version": "03.09.0502",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC Event Database",
                                            "Version": "05.05.0402",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "SIMATIC X-Ref Control",
                                            "Version": "05.02.0800",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC S7-Block Privacy V1.0 + SP3  ",
                                            "Version": "01.00.0300",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "VC User 71 RTL X86 ---",
                                            "Version": "1.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                        {
                                            "Name": "Automation Access Control Component",
                                            "Version": "04.00.0100",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC S7-Status-OCX",
                                            "Version": "05.03.1100",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "SIMATIC Technological Parameter Assignment",
                                            "Version": "05.03.1100",
                                            "Installed Date": "Jul 10 2017",
                                        },
                                        {
                                            "Name": "Microsoft SQL Server VSS Writer",
                                            "Version": "10.52.4000.0",
                                            "Installed Date": "Feb 2 2016",
                                        },
                                    ],
                                },
                                "devicesAndDrives": {
                                    "columns": [
                                        {"field": "Name"},
                                        {"field": "Drive Letter"},
                                        {"field": "Capacity", "format": "Bytes"},
                                        {"field": "Device Type"},
                                    ],
                                    "data": [
                                        {
                                            "Name": "System Reserved",
                                            "Drive Letter": "",
                                            "Capacity": 104853504,
                                            "Device Type": "Unknown",
                                        },
                                        {
                                            "Name": "",
                                            "Drive Letter": "C:",
                                            "Capacity": 42842714112,
                                            "Device Type": "Unknown",
                                        },
                                        {
                                            "Name": "",
                                            "Drive Letter": "D:",
                                            "Capacity": 0,
                                            "Device Type": "Unknown",
                                        },
                                    ],
                                },
                            },
                            "family": None,
                            "firmwareVersion": None,
                            "firstSeen": "2021-04-11T21:00:09.154979Z",
                            "hidden": True,
                            "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                            "ips": {"nodes": ["10.100.30.37"]},
                            "lastSeen": "2021-06-25T13:02:37.178997Z",
                            "lastUpdate": "2022-10-04T02:18:54.78456Z",
                            "location": None,
                            "macs": {"nodes": []},
                            "model": None,
                            "name": "STEP7",
                            "os": "Windows Server 2008 R2",
                            "osDetails": {
                                "name": "Microsoft Windows Server 2008 R2 Standard ",
                                "architecture": "64-bit",
                                "hotFixes": {
                                    "nodes": [
                                        {
                                            "name": "KB4095874",
                                            "installDate": "2018-05-27T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB4103768",
                                            "installDate": "2018-05-27T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB4103718",
                                            "installDate": "2018-05-27T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB4019990",
                                            "installDate": "2018-05-27T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3167679",
                                            "installDate": "2016-08-31T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3177723",
                                            "installDate": "2016-08-31T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3168965",
                                            "installDate": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3170455",
                                            "installDate": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3175443",
                                            "installDate": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3177725",
                                            "installDate": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3178034",
                                            "installDate": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3163245",
                                            "installDate": "2016-08-29T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3142024",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3156017",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3164033",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3156019",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3164035",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3159398",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3160005",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3161561",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3161664",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3161949",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3161958",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3153171",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3162835",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3156016",
                                            "installDate": "2016-06-16T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3142042",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3145739",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3135983",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3146706",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3138612",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3146963",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3139398",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3148198",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3139914",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3148851",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3139940",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3149090",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3140735",
                                            "installDate": "2016-04-20T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3133043",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3134214",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3122648",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3134814",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3126587",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3126593",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3127220",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3141092",
                                            "installDate": "2016-03-28T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3072305",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3121212",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3121918",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3108664",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3123479",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3124000",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3124001",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3124275",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3109560",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3110329",
                                            "installDate": "2016-02-09T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB917607",
                                            "installDate": "2016-02-02T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2849697",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2849696",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2841134",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2670838",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2729094",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2834140",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2882822",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2912390",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2973351",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3104002",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3042058",
                                            "installDate": "2016-01-04T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2506014",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2506212",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2509553",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2511455",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2536275",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2544893",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2552343",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2560656",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2564958",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2570947",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2585542",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2604115",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2620704",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2621440",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2631813",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2643719",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2653956",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2654428",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2656356",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2667402",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2676562",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2685939",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2690533",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2698365",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2705219",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2706045",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2712808",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2718704",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2729452",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2736422",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2742599",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2758857",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2765809",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2770660",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2786081",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2789645",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2798162",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2807986",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2813430",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2836942",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2836943",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2839894",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2840149",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2840631",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2861698",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2862152",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2862330",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2862335",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2862973",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2864202",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2868038",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2868116",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2868626",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2871997",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2884256",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2887069",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2892074",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2893294",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2894844",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2900986",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2911501",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2929733",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB2931356",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2937610",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2943357",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2957189",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2968294",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2972100",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2972211",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2973112",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2973201",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2976897",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2977292",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2978120",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3006226",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3030377",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3045685",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3084135",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2984972",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3010788",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3031432",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3046017",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3072595",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3086255",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3108371",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2991963",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3011780",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3032655",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3046269",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3072630",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3087039",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3108381",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2992611",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3014029",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3033889",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3055642",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3072633",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3092601",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB2993651",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3018238",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3033929",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3059317",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3074543",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3097966",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3108670",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3000483",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3019978",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3035126",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3060716",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3075220",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3097989",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3109094",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3003743",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3020369",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB3035132",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3061518",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3076895",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3099862",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3109103",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3004361",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3021674",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3037574",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3068457",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3078601",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3101246",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3004375",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3022777",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3069392",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3080446",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3101722",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3005607",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3023215",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3042553",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3071756",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3081320",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3101746",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Security Update",
                                        },
                                        {
                                            "name": "KB3112343",
                                            "installDate": "2016-01-03T00:00:00Z",
                                            "description": "Update",
                                        },
                                        {
                                            "name": "KB976902",
                                            "installDate": "2010-11-21T00:00:00Z",
                                            "description": "Update",
                                        },
                                    ]
                                },
                                "version": "6.1.7601",
                            },
                            "purdueLevel": "Level3",
                            "runStatus": "Unknown",
                            "runStatusTime": "0001-01-01T00:00:00Z",
                            "serial": None,
                            "slot": None,
                            "superType": "Server",
                            "type": "Server",
                            "vendor": None,
                            "risk": {"unresolvedEvents": 0, "totalRisk": 0},
                            "backplane": None,
                            "segments": {
                                "nodes": [
                                    {
                                        "id": "59161089-c6f7-4f8c-90a3-92f5be9d3b9d",
                                        "name": "Server / 10.100.30.X",
                                        "type": "Segment",
                                        "key": "AG1-20",
                                        "systemName": "Server / 10.100.30.X",
                                        "vlan": None,
                                        "description": None,
                                        "assetType": "Server",
                                        "subnet": "10.100.30.X",
                                    }
                                ]
                            },
                            "revisions": {"nodes": []},
                            "plugins": {
                                "nodes": [
                                    {
                                        "id": 10107,
                                        "name": "HTTP Server Type and Version",
                                        "source": "Nessus",
                                        "family": "Web Servers",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 8,
                                    },
                                    {
                                        "id": 19506,
                                        "name": "Nessus Scan Information",
                                        "source": "Nessus",
                                        "family": "Settings",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 10,
                                    },
                                    {
                                        "id": 22964,
                                        "name": "Service Detection",
                                        "source": "Nessus",
                                        "family": "Service detection",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 9,
                                    },
                                    {
                                        "id": 56984,
                                        "name": "SSL / TLS Versions Supported",
                                        "source": "Nessus",
                                        "family": "General",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 9,
                                    },
                                ]
                            },
                        }
                    ],
                }
            }
        },
    )

    expected = Asset(
        backplane=None,
        category="NetworkAssetsCategory",
        criticality="LowCriticality",
        description=None,
        details={
            "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
            "name": "STEP7",
            "firstSeen": "2021-04-11T21:00:09.154979Z",
            "lastSeen": "2021-06-25T13:02:37.178997Z",
            "macs": [],
            "ips": ["10.100.30.37"],
            "type": "Server",
            "superType": "Server",
            "category": "NetworkAssetsCategory",
            "purdueLevel": "Level3",
            "runStatus": "Unknown",
            "runStatusTime": "0001-01-01T00:00:00Z",
            "os": "Windows Server 2008 R2",
            "rawFamily": "UnknownFamily",
            "risk": 0,
            "criticality": "LowCriticality",
            "hidden": True,
            "lastUpdate": "2022-10-04T02:18:54.78456Z",
            "classificationIncidents": [
                "DirectConnectorIncident",
                "WindowsServerWmiIncident",
            ],
            "hardware": {
                "numOfProcessors": "2",
                "cpu": "Intel(R) Xeon(R) Silver 4114 CPU @ 2.20GHz",
                "cpuSpeed": 2597,
                "cpuLoad": 2,
                "cpuArchitecture": "x64",
                "cpuRevision": 16128,
                "totalPhysicalMemory": 2146951168,
                "usedPhysicalMemory": 952430592,
                "freePhysicalMemory": 1194520576,
                "totalVirtualMemory": 4293902336,
                "usedVirtualMemory": 2070228992,
                "freeVirtualMemory": 2223673344,
                "biosVersion": "6.00",
                "biosSerial": "VMware-42 12 e4 83 95 a1 87 7a-07 1c c1 c2 05 a6 41 81",
                "biosMajor": 2,
                "biosMinor": 4,
                "csManufacturer": "VMware, Inc.",
                "csModel": "VMware Virtual Platform",
                "devicesAndDrives": [
                    {
                        "name": "System Reserved",
                        "capacity": 104853504,
                        "driveLetter": "",
                        "deviceType": "Unknown",
                    },
                    {
                        "name": "",
                        "capacity": 42842714112,
                        "driveLetter": "C:",
                        "deviceType": "Unknown",
                    },
                    {
                        "name": "",
                        "capacity": 0,
                        "driveLetter": "D:",
                        "deviceType": "Unknown",
                    },
                ],
            },
            "names": [
                {
                    "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                    "source": "Default",
                    "value": "Server #7",
                },
                {
                    "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                    "source": "Wmi",
                    "value": "STEP7",
                },
                {
                    "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                    "source": "Chosen",
                    "value": "STEP7",
                },
                {
                    "id": "e419cab7-4a5a-4f0d-a05f-982928919eba",
                    "source": "Dns",
                    "value": "ipaserver.indegy.local",
                },
            ],
            "windows": {
                "osName": "Microsoft Windows Server 2008 R2 Standard ",
                "computerName": "STEP7",
                "version": "6.1.7601",
                "servicepackMajor": 1,
                "servicepackMinor": 0,
                "buildType": "Multiprocessor Free",
                "buildNumber": "7601",
                "osArchitecture": "64-bit",
                "serialNumber": "55041-507-9059273-84698",
                "registeredUser": "Windows User",
                "installDate": "2016-01-04T00:26:08Z",
                "lastBootUpTime": "2021-01-30T16:13:42.359599Z",
                "csDomain": "WORKGROUP",
                "hotFixes": [
                    {
                        "hotFixId": "KB4019990",
                        "installedOn": "2018-05-27T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB4095874",
                        "installedOn": "2018-05-27T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB4103718",
                        "installedOn": "2018-05-27T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB4103768",
                        "installedOn": "2018-05-27T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3167679",
                        "installedOn": "2016-08-31T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3177723",
                        "installedOn": "2016-08-31T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3163245",
                        "installedOn": "2016-08-29T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3168965",
                        "installedOn": "2016-08-29T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3170455",
                        "installedOn": "2016-08-29T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3175443",
                        "installedOn": "2016-08-29T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3177725",
                        "installedOn": "2016-08-29T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3178034",
                        "installedOn": "2016-08-29T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3142024",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3153171",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3156016",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3156017",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3156019",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3159398",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3160005",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3161561",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3161664",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3161949",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3161958",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3162835",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3164033",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3164035",
                        "installedOn": "2016-06-16T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3135983",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3138612",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3139398",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3139914",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3139940",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3140735",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3142042",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3145739",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3146706",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3146963",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3148198",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3148851",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3149090",
                        "installedOn": "2016-04-20T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3122648",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3126587",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3126593",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3127220",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3133043",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3134214",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3134814",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3141092",
                        "installedOn": "2016-03-28T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3072305",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3108664",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3109560",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3110329",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3121212",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3121918",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3123479",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3124000",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3124001",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3124275",
                        "installedOn": "2016-02-09T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB917607",
                        "installedOn": "2016-02-02T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2670838",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2729094",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2834140",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2841134",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2849696",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2849697",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2882822",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2912390",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2973351",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3042058",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3104002",
                        "installedOn": "2016-01-04T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2506014",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2506212",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2509553",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2511455",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2536275",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2544893",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2552343",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2560656",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2564958",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2570947",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2585542",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2604115",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2620704",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2621440",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2631813",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2643719",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2653956",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2654428",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2656356",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2667402",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2676562",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2685939",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2690533",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2698365",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2705219",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2706045",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2712808",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2718704",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2729452",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2736422",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2742599",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2758857",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2765809",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2770660",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2786081",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2789645",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2798162",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2807986",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2813430",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2836942",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2836943",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2839894",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2840149",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2840631",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2861698",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2862152",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2862330",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2862335",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2862973",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2864202",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2868038",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2868116",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2868626",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2871997",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2884256",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2887069",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2892074",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2893294",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2894844",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2900986",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2911501",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2929733",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB2931356",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2937610",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2943357",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2957189",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2968294",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2972100",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2972211",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2973112",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2973201",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2976897",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2977292",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2978120",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2984972",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2991963",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2992611",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB2993651",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3000483",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3003743",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3004361",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3004375",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3005607",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3006226",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3010788",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3011780",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3014029",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3018238",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3019978",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3020369",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB3021674",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3022777",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3023215",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3030377",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3031432",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3032655",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3033889",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3033929",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3035126",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3035132",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3037574",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3042553",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3045685",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3046017",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3046269",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3055642",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3059317",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3060716",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3061518",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3068457",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3069392",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3071756",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3072595",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3072630",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3072633",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3074543",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3075220",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3076895",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3078601",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3080446",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3081320",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3084135",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3086255",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3087039",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3092601",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3097966",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3097989",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3099862",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3101246",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3101722",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3101746",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3108371",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3108381",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3108670",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3109094",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3109103",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Security Update",
                    },
                    {
                        "hotFixId": "KB3112343",
                        "installedOn": "2016-01-03T00:00:00Z",
                        "description": "Update",
                    },
                    {
                        "hotFixId": "KB976902",
                        "installedOn": "2010-11-21T00:00:00Z",
                        "description": "Update",
                    },
                ],
                "installedSoftware": [
                    {
                        "name": "Microsoft Application Error Reporting",
                        "version": "12.0.6012.5000",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Sql Server Customer Experience Improvement Program",
                        "version": "10.50.1600.1",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC  STEP 7 V5.5 + SP4  ",
                        "version": "05.05.0400",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "OPC .NET API 2.00 Redistributables (x86) 101.0",
                        "version": "2.00.10200",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219",
                        "version": "10.0.40219",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.20.27508",
                        "version": "14.20.27508",
                        "installDate": "Jan 16 2020",
                    },
                    {
                        "name": "Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219",
                        "version": "10.0.40219",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - HM NoBasic Single SetupPackage  V13.0 SP1 UPD7",
                        "version": "13.00.0100",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "SIMATIC S7-PCT V3.2  ",
                        "version": "03.02.0000",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "NETLink-S7-NET",
                        "version": "3.5.0.3",
                        "installDate": "Aug 17 2020",
                    },
                    {
                        "name": "SQL Server 2008 R2 SP2 Database Engine Services",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SQL Server 2008 R2 SP2 Database Engine Services",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2005 Redistributable",
                        "version": "8.0.59193",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft SQL Server 2008 Setup Support Files ",
                        "version": "10.1.2731.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft SQL Server 2008 R2 RsFx Driver",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - HM All Editions Single SetupPackage  V13.0 SP1 UPD7",
                        "version": "13.00.0100",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.20.27508",
                        "version": "14.20.27508",
                        "installDate": "Jan 16 2020",
                    },
                    {
                        "name": "SIMATIC WinCC/Audit Viewer 2008 SP2  ",
                        "version": "07.02.0000",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - TIA Tour Single SetupPackage  V13.0 + SP1",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC S7-Web2PLC V1.0 + SP2 + HF1  ",
                        "version": "01.00.0201",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package WCF-01  V13.0",
                        "version": "13.00.0000",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "OPC Core Components Redistributable (x86) 101.2",
                        "version": "3.00.10102",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2013 x64 Additional Runtime - 12.0.21005",
                        "version": "12.0.21005",
                        "installDate": "Apr 20 2016",
                    },
                    {
                        "name": "Microsoft .NET Framework 4.5.2",
                        "version": "4.5.51209",
                        "installDate": "May 27 2018",
                    },
                    {
                        "name": "SQL Server 2008 R2 SP2 Common Files",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161",
                        "version": "9.0.30729.6161",
                        "installDate": "Jan 3 2016",
                    },
                    {
                        "name": "WinCC Runtime Advanced V13.0 SP1 -  SIMATIC WinCC Runtime Advanced  V13.0 + SP1",
                        "version": "13.00.0100",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161",
                        "version": "9.0.30729.6161",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "MSXML 4.0 SP2 (KB973688)",
                        "version": "4.20.9876.0",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2013 x64 Minimum Runtime - 12.0.21005",
                        "version": "12.0.21005",
                        "installDate": "Apr 20 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 03  V13.0",
                        "version": "13.00.0000",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2012 x64 Additional Runtime - 11.0.61030",
                        "version": "11.0.61030",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft SQL Server Browser",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                        "version": "8.0.56336",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Totally Integrated Automation Portal V13 -  TIA Portal Single SetupPackage  V13.0 + SP1",
                        "version": "13.00.0100",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "SQL Server 2008 R2 SP2 Common Files",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Siemens Automation License Manager V5.3 + SP2 + Upd2  ",
                        "version": "05.03.0202",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft SQL Server 2008 R2 Native Client",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2019 X86 Additional Runtime - 14.20.27508",
                        "version": "14.20.27508",
                        "installDate": "Jan 16 2020",
                    },
                    {
                        "name": "WinCC Runtime Advanced V13.0 SP1 - HMIRTM Simulation Single SetupPackage  V13.0 SP1 UPD7",
                        "version": "13.00.0100",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - Simatic Single SetupPackage  V13.0 SP1 UPD7",
                        "version": "13.00.0100",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 0  V13.0",
                        "version": "13.00.0000",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Primary Interoperability Assemblies 2005",
                        "version": "8.0.50727.42",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 02  V13.0",
                        "version": "13.00.0000",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                        "version": "8.0.59192",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft SQL Server 2008 R2 Setup (English)",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft SOAP Toolkit 3.0",
                        "version": "3.0.1325.4",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC Prosave V13.0 SP1  ",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "License Logon Interface",
                        "version": "04.00.0300",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC Process Diagnosis Database",
                        "version": "5.3",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC DIAGNOSTIC REPEATER GUI CTRL",
                        "version": "05.02.0300",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.17",
                        "version": "9.0.30729",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2005 Redistributable",
                        "version": "8.0.56336",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148",
                        "version": "9.0.30729.4148",
                        "installDate": "Jan 3 2016",
                    },
                    {
                        "name": "Automation Software Updater",
                        "version": "02.05.0000",
                        "installDate": "Feb 3 2020",
                    },
                    {
                        "name": "MSXML 4.0 SP2 (KB954430)",
                        "version": "4.20.9870.0",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "SeCon",
                        "version": "02.02.0000",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "VMware Tools",
                        "version": "11.0.1.14773994",
                        "installDate": "Jan 16 2020",
                    },
                    {
                        "name": "Microsoft Visual C++ 2019 X64 Additional Runtime - 14.20.27508",
                        "version": "14.20.27508",
                        "installDate": "Jan 16 2020",
                    },
                    {
                        "name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.17",
                        "version": "9.0.30729",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC Extended Interfaces",
                        "version": "05.04.0600",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC Colour Editor",
                        "version": "05.01.1600",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC NCM FWL 64",
                        "version": "05.05.0400",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "PKZIP Server for Windows 12.40.0008",
                        "version": "12.40.0008",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - TIACOMPCHECK Single SetupPackage  V13.0 + SP1 + Upd7",
                        "version": "13.00.0107",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "SIMATIC Device Drivers WoW",
                        "version": "29.00.0700",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "SIMATIC Process Diagnosis Base",
                        "version": "5.3",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC HMI Symbol Library",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2012 x86 Minimum Runtime - 11.0.61030",
                        "version": "11.0.61030",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC Device Drivers",
                        "version": "09.00.0700",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "SIMATIC Interface Editor",
                        "version": "05.04.1800",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC HMI Touch Input",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2012 x86 Additional Runtime - 11.0.61030",
                        "version": "11.0.61030",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "WinCC Runtime Advanced Simulator",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC Grid Control",
                        "version": "02.06.0000",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC GSD CONTROL",
                        "version": "03.05.0600",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC HMI ProSave",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "OPC UA SDK 1.1 Redistributables 331.0",
                        "version": "1.01.33100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC HMI License Manager Panel Plugin (x64)",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC GSD Interpreter",
                        "version": "02.04.0200",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC Common Services",
                        "version": "05.03.1500",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC NCM",
                        "version": "05.05.0400",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC WinCC Runtime Advanced Driver (x64)",
                        "version": "13.00.0100",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC LanguageSupportTool",
                        "version": "05.08.0300",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC Version View",
                        "version": "01.07.0900",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "Siemens  Totally Integrated Automation Portal V13 - WinCC Single SetupPackage  V13.0 SP1 UPD7",
                        "version": "13.00.0100",
                        "installDate": "Feb 9 2016",
                    },
                    {
                        "name": "Microsoft Visual C++ 2012 x64 Minimum Runtime - 11.0.61030",
                        "version": "11.0.61030",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIEMENS OPC",
                        "version": "03.09.0502",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC Event Database",
                        "version": "05.05.0402",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "SIMATIC X-Ref Control",
                        "version": "05.02.0800",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC S7-Block Privacy V1.0 + SP3  ",
                        "version": "01.00.0300",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "VC User 71 RTL X86 ---",
                        "version": "1.0",
                        "installDate": "Feb 2 2016",
                    },
                    {
                        "name": "Automation Access Control Component",
                        "version": "04.00.0100",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC S7-Status-OCX",
                        "version": "05.03.1100",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "SIMATIC Technological Parameter Assignment",
                        "version": "05.03.1100",
                        "installDate": "Jul 10 2017",
                    },
                    {
                        "name": "Microsoft SQL Server VSS Writer",
                        "version": "10.52.4000.0",
                        "installDate": "Feb 2 2016",
                    },
                ],
            },
            "customFields": [
                ["customField1", "Building", "PlainText"],
                ["customField10", "Line", "PlainText"],
                ["customField2", "Point of Contact", "PlainText"],
                ["customField4", "Vertical", "PlainText"],
                ["customField5", "Geo-Location", "HyperLink"],
                ["customField7", "Revisions", "PlainText"],
                ["customField8", "Temp", "PlainText"],
                ["customField6", "TAGS OR OTHER NAME", "PlainText"],
                ["customField3", "map", "HyperLink"],
            ],
            "directIp": "10.100.30.37",
            "directIps": None,
            "directMac": None,
            "directMacs": None,
            "additionalIp": None,
            "additionalIps": None,
            "additionalMac": None,
            "additionalMacs": None,
            "stateUpdateTime": "0001-01-01T00:00:00Z",
            "extendedSegments": [
                {
                    "id": "59161089-c6f7-4f8c-90a3-92f5be9d3b9d",
                    "name": "Server / 10.100.30.X",
                    "archived": False,
                    "system": True,
                    "key": "AG1-20",
                    "type": "Segment",
                    "systemName": "Server / 10.100.30.X",
                    "vlan": None,
                    "description": None,
                    "isPredefinedName": True,
                    "subnet": "10.100.30.X",
                    "assetType": "Server",
                }
            ],
            "state": "Unknown",
            "backplaneName": None,
            "hotFixes": {
                "columns": [
                    {"field": "Id"},
                    {"field": "Description"},
                    {"field": "Installed Date"},
                ],
                "data": [
                    {
                        "Id": "KB4019990",
                        "Description": "Update",
                        "Installed Date": "2018-05-27T00:00:00Z",
                    },
                    {
                        "Id": "KB4095874",
                        "Description": "Update",
                        "Installed Date": "2018-05-27T00:00:00Z",
                    },
                    {
                        "Id": "KB4103718",
                        "Description": "Security Update",
                        "Installed Date": "2018-05-27T00:00:00Z",
                    },
                    {
                        "Id": "KB4103768",
                        "Description": "Security Update",
                        "Installed Date": "2018-05-27T00:00:00Z",
                    },
                    {
                        "Id": "KB3167679",
                        "Description": "Security Update",
                        "Installed Date": "2016-08-31T00:00:00Z",
                    },
                    {
                        "Id": "KB3177723",
                        "Description": "Update",
                        "Installed Date": "2016-08-31T00:00:00Z",
                    },
                    {
                        "Id": "KB3163245",
                        "Description": "Security Update",
                        "Installed Date": "2016-08-29T00:00:00Z",
                    },
                    {
                        "Id": "KB3168965",
                        "Description": "Security Update",
                        "Installed Date": "2016-08-29T00:00:00Z",
                    },
                    {
                        "Id": "KB3170455",
                        "Description": "Security Update",
                        "Installed Date": "2016-08-29T00:00:00Z",
                    },
                    {
                        "Id": "KB3175443",
                        "Description": "Security Update",
                        "Installed Date": "2016-08-29T00:00:00Z",
                    },
                    {
                        "Id": "KB3177725",
                        "Description": "Security Update",
                        "Installed Date": "2016-08-29T00:00:00Z",
                    },
                    {
                        "Id": "KB3178034",
                        "Description": "Security Update",
                        "Installed Date": "2016-08-29T00:00:00Z",
                    },
                    {
                        "Id": "KB3142024",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3153171",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3156016",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3156017",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3156019",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3159398",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3160005",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3161561",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3161664",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3161949",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3161958",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3162835",
                        "Description": "Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3164033",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3164035",
                        "Description": "Security Update",
                        "Installed Date": "2016-06-16T00:00:00Z",
                    },
                    {
                        "Id": "KB3135983",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3138612",
                        "Description": "Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3139398",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3139914",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3139940",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3140735",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3142042",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3145739",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3146706",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3146963",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3148198",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3148851",
                        "Description": "Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3149090",
                        "Description": "Security Update",
                        "Installed Date": "2016-04-20T00:00:00Z",
                    },
                    {
                        "Id": "KB3122648",
                        "Description": "Security Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3126587",
                        "Description": "Security Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3126593",
                        "Description": "Security Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3127220",
                        "Description": "Security Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3133043",
                        "Description": "Security Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3134214",
                        "Description": "Security Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3134814",
                        "Description": "Security Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3141092",
                        "Description": "Update",
                        "Installed Date": "2016-03-28T00:00:00Z",
                    },
                    {
                        "Id": "KB3072305",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3108664",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3109560",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3110329",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3121212",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3121918",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3123479",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3124000",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3124001",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB3124275",
                        "Description": "Security Update",
                        "Installed Date": "2016-02-09T00:00:00Z",
                    },
                    {
                        "Id": "KB917607",
                        "Description": "Update",
                        "Installed Date": "2016-02-02T00:00:00Z",
                    },
                    {
                        "Id": "KB2670838",
                        "Description": "Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2729094",
                        "Description": "Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2834140",
                        "Description": "Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2841134",
                        "Description": "Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2849696",
                        "Description": "Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2849697",
                        "Description": "Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2882822",
                        "Description": "Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2912390",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2973351",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB3042058",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB3104002",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-04T00:00:00Z",
                    },
                    {
                        "Id": "KB2506014",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2506212",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2509553",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2511455",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2536275",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2544893",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2552343",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2560656",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2564958",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2570947",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2585542",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2604115",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2620704",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2621440",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2631813",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2643719",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2653956",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2654428",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2656356",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2667402",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2676562",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2685939",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2690533",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2698365",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2705219",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2706045",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2712808",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2718704",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2729452",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2736422",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2742599",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2758857",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2765809",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2770660",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2786081",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2789645",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2798162",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2807986",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2813430",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2836942",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2836943",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2839894",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2840149",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2840631",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2861698",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2862152",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2862330",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2862335",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2862973",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2864202",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2868038",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2868116",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2868626",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2871997",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2884256",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2887069",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2892074",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2893294",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2894844",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2900986",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2911501",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2929733",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2931356",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2937610",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2943357",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2957189",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2968294",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2972100",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2972211",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2973112",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2973201",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2976897",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2977292",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2978120",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2984972",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2991963",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2992611",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB2993651",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3000483",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3003743",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3004361",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3004375",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3005607",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3006226",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3010788",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3011780",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3014029",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3018238",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3019978",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3020369",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3021674",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3022777",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3023215",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3030377",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3031432",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3032655",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3033889",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3033929",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3035126",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3035132",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3037574",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3042553",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3045685",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3046017",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3046269",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3055642",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3059317",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3060716",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3061518",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3068457",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3069392",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3071756",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3072595",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3072630",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3072633",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3074543",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3075220",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3076895",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3078601",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3080446",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3081320",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3084135",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3086255",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3087039",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3092601",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3097966",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3097989",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3099862",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3101246",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3101722",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3101746",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3108371",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3108381",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3108670",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3109094",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3109103",
                        "Description": "Security Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB3112343",
                        "Description": "Update",
                        "Installed Date": "2016-01-03T00:00:00Z",
                    },
                    {
                        "Id": "KB976902",
                        "Description": "Update",
                        "Installed Date": "2010-11-21T00:00:00Z",
                    },
                ],
            },
            "installedSoftware": {
                "columns": [
                    {"field": "Name"},
                    {"field": "Version"},
                    {"field": "Installed Date"},
                ],
                "data": [
                    {
                        "Name": "Microsoft Application Error Reporting",
                        "Version": "12.0.6012.5000",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Sql Server Customer Experience Improvement Program",
                        "Version": "10.50.1600.1",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC  STEP 7 V5.5 + SP4  ",
                        "Version": "05.05.0400",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "OPC .NET API 2.00 Redistributables (x86) 101.0",
                        "Version": "2.00.10200",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219",
                        "Version": "10.0.40219",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.20.27508",
                        "Version": "14.20.27508",
                        "Installed Date": "Jan 16 2020",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219",
                        "Version": "10.0.40219",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - HM NoBasic Single SetupPackage  V13.0 SP1 UPD7",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "SIMATIC S7-PCT V3.2  ",
                        "Version": "03.02.0000",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "NETLink-S7-NET",
                        "Version": "3.5.0.3",
                        "Installed Date": "Aug 17 2020",
                    },
                    {
                        "Name": "SQL Server 2008 R2 SP2 Database Engine Services",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SQL Server 2008 R2 SP2 Database Engine Services",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2005 Redistributable",
                        "Version": "8.0.59193",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft SQL Server 2008 Setup Support Files ",
                        "Version": "10.1.2731.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft SQL Server 2008 R2 RsFx Driver",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - HM All Editions Single SetupPackage  V13.0 SP1 UPD7",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.20.27508",
                        "Version": "14.20.27508",
                        "Installed Date": "Jan 16 2020",
                    },
                    {
                        "Name": "SIMATIC WinCC/Audit Viewer 2008 SP2  ",
                        "Version": "07.02.0000",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - TIA Tour Single SetupPackage  V13.0 + SP1",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC S7-Web2PLC V1.0 + SP2 + HF1  ",
                        "Version": "01.00.0201",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package WCF-01  V13.0",
                        "Version": "13.00.0000",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "OPC Core Components Redistributable (x86) 101.2",
                        "Version": "3.00.10102",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2013 x64 Additional Runtime - 12.0.21005",
                        "Version": "12.0.21005",
                        "Installed Date": "Apr 20 2016",
                    },
                    {
                        "Name": "Microsoft .NET Framework 4.5.2",
                        "Version": "4.5.51209",
                        "Installed Date": "May 27 2018",
                    },
                    {
                        "Name": "SQL Server 2008 R2 SP2 Common Files",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161",
                        "Version": "9.0.30729.6161",
                        "Installed Date": "Jan 3 2016",
                    },
                    {
                        "Name": "WinCC Runtime Advanced V13.0 SP1 -  SIMATIC WinCC Runtime Advanced  V13.0 + SP1",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161",
                        "Version": "9.0.30729.6161",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "MSXML 4.0 SP2 (KB973688)",
                        "Version": "4.20.9876.0",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2013 x64 Minimum Runtime - 12.0.21005",
                        "Version": "12.0.21005",
                        "Installed Date": "Apr 20 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 03  V13.0",
                        "Version": "13.00.0000",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2012 x64 Additional Runtime - 11.0.61030",
                        "Version": "11.0.61030",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft SQL Server Browser",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                        "Version": "8.0.56336",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Totally Integrated Automation Portal V13 -  TIA Portal Single SetupPackage  V13.0 + SP1",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "SQL Server 2008 R2 SP2 Common Files",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Siemens Automation License Manager V5.3 + SP2 + Upd2  ",
                        "Version": "05.03.0202",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft SQL Server 2008 R2 Native Client",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2019 X86 Additional Runtime - 14.20.27508",
                        "Version": "14.20.27508",
                        "Installed Date": "Jan 16 2020",
                    },
                    {
                        "Name": "WinCC Runtime Advanced V13.0 SP1 - HMIRTM Simulation Single SetupPackage  V13.0 SP1 UPD7",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - Simatic Single SetupPackage  V13.0 SP1 UPD7",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 0  V13.0",
                        "Version": "13.00.0000",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Primary Interoperability Assemblies 2005",
                        "Version": "8.0.50727.42",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - Hardware Support Base Package 02  V13.0",
                        "Version": "13.00.0000",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2005 Redistributable (x64)",
                        "Version": "8.0.59192",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft SQL Server 2008 R2 Setup (English)",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft SOAP Toolkit 3.0",
                        "Version": "3.0.1325.4",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC Prosave V13.0 SP1  ",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "License Logon Interface",
                        "Version": "04.00.0300",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC Process Diagnosis Database",
                        "Version": "5.3",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC DIAGNOSTIC REPEATER GUI CTRL",
                        "Version": "05.02.0300",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.17",
                        "Version": "9.0.30729",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2005 Redistributable",
                        "Version": "8.0.56336",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.4148",
                        "Version": "9.0.30729.4148",
                        "Installed Date": "Jan 3 2016",
                    },
                    {
                        "Name": "Automation Software Updater",
                        "Version": "02.05.0000",
                        "Installed Date": "Feb 3 2020",
                    },
                    {
                        "Name": "MSXML 4.0 SP2 (KB954430)",
                        "Version": "4.20.9870.0",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "SeCon",
                        "Version": "02.02.0000",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "VMware Tools",
                        "Version": "11.0.1.14773994",
                        "Installed Date": "Jan 16 2020",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2019 X64 Additional Runtime - 14.20.27508",
                        "Version": "14.20.27508",
                        "Installed Date": "Jan 16 2020",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.17",
                        "Version": "9.0.30729",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC Extended Interfaces",
                        "Version": "05.04.0600",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC Colour Editor",
                        "Version": "05.01.1600",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC NCM FWL 64",
                        "Version": "05.05.0400",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "PKZIP Server for Windows 12.40.0008",
                        "Version": "12.40.0008",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - TIACOMPCHECK Single SetupPackage  V13.0 + SP1 + Upd7",
                        "Version": "13.00.0107",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "SIMATIC Device Drivers WoW",
                        "Version": "29.00.0700",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "SIMATIC Process Diagnosis Base",
                        "Version": "5.3",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC HMI Symbol Library",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2012 x86 Minimum Runtime - 11.0.61030",
                        "Version": "11.0.61030",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC Device Drivers",
                        "Version": "09.00.0700",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "SIMATIC Interface Editor",
                        "Version": "05.04.1800",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC HMI Touch Input",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2012 x86 Additional Runtime - 11.0.61030",
                        "Version": "11.0.61030",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "WinCC Runtime Advanced Simulator",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC Grid Control",
                        "Version": "02.06.0000",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC GSD CONTROL",
                        "Version": "03.05.0600",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC HMI ProSave",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "OPC UA SDK 1.1 Redistributables 331.0",
                        "Version": "1.01.33100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC HMI License Manager Panel Plugin (x64)",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC GSD Interpreter",
                        "Version": "02.04.0200",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC Common Services",
                        "Version": "05.03.1500",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC NCM",
                        "Version": "05.05.0400",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SQL Server 2008 R2 SP2 Database Engine Shared",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC WinCC Runtime Advanced Driver (x64)",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC LanguageSupportTool",
                        "Version": "05.08.0300",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC Version View",
                        "Version": "01.07.0900",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "Siemens  Totally Integrated Automation Portal V13 - WinCC Single SetupPackage  V13.0 SP1 UPD7",
                        "Version": "13.00.0100",
                        "Installed Date": "Feb 9 2016",
                    },
                    {
                        "Name": "Microsoft Visual C++ 2012 x64 Minimum Runtime - 11.0.61030",
                        "Version": "11.0.61030",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIEMENS OPC",
                        "Version": "03.09.0502",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC Event Database",
                        "Version": "05.05.0402",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "SIMATIC X-Ref Control",
                        "Version": "05.02.0800",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC S7-Block Privacy V1.0 + SP3  ",
                        "Version": "01.00.0300",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "VC User 71 RTL X86 ---",
                        "Version": "1.0",
                        "Installed Date": "Feb 2 2016",
                    },
                    {
                        "Name": "Automation Access Control Component",
                        "Version": "04.00.0100",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC S7-Status-OCX",
                        "Version": "05.03.1100",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "SIMATIC Technological Parameter Assignment",
                        "Version": "05.03.1100",
                        "Installed Date": "Jul 10 2017",
                    },
                    {
                        "Name": "Microsoft SQL Server VSS Writer",
                        "Version": "10.52.4000.0",
                        "Installed Date": "Feb 2 2016",
                    },
                ],
            },
            "devicesAndDrives": {
                "columns": [
                    {"field": "Name"},
                    {"field": "Drive Letter"},
                    {"field": "Capacity", "format": "Bytes"},
                    {"field": "Device Type"},
                ],
                "data": [
                    {
                        "Name": "System Reserved",
                        "Drive Letter": "",
                        "Capacity": 104853504,
                        "Device Type": "Unknown",
                    },
                    {
                        "Name": "",
                        "Drive Letter": "C:",
                        "Capacity": 42842714112,
                        "Device Type": "Unknown",
                    },
                    {
                        "Name": "",
                        "Drive Letter": "D:",
                        "Capacity": 0,
                        "Device Type": "Unknown",
                    },
                ],
            },
        },
        family=None,
        firmware_version=None,
        first_seen=datetime.datetime(
            2021, 4, 11, 21, 0, 9, 154979, tzinfo=datetime.timezone.utc
        ),
        hidden=True,
        id=uuid.UUID("e419cab7-4a5a-4f0d-a05f-982928919eba"),
        ips=NodesList(nodes=["10.100.30.37"]),
        last_seen=datetime.datetime(
            2021, 6, 25, 13, 2, 37, 178997, tzinfo=datetime.timezone.utc
        ),
        last_update="2022-10-04T02:18:54.78456Z",
        location=None,
        macs=NodesList(nodes=[]),
        model=None,
        name="STEP7",
        os="Windows Server 2008 R2",
        os_details=OSDetails(
            name="Microsoft Windows Server 2008 R2 Standard ",
            architecture="64-bit",
            version="6.1.7601",
            hot_fixes=HotFixes(
                nodes=[
                    Hotfix(
                        name="KB4095874",
                        install_date=datetime.datetime(
                            2018, 5, 27, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB4103768",
                        install_date=datetime.datetime(
                            2018, 5, 27, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB4103718",
                        install_date=datetime.datetime(
                            2018, 5, 27, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB4019990",
                        install_date=datetime.datetime(
                            2018, 5, 27, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3167679",
                        install_date=datetime.datetime(
                            2016, 8, 31, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3177723",
                        install_date=datetime.datetime(
                            2016, 8, 31, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3168965",
                        install_date=datetime.datetime(
                            2016, 8, 29, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3170455",
                        install_date=datetime.datetime(
                            2016, 8, 29, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3175443",
                        install_date=datetime.datetime(
                            2016, 8, 29, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3177725",
                        install_date=datetime.datetime(
                            2016, 8, 29, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3178034",
                        install_date=datetime.datetime(
                            2016, 8, 29, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3163245",
                        install_date=datetime.datetime(
                            2016, 8, 29, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3142024",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3156017",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3164033",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3156019",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3164035",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3159398",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3160005",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3161561",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3161664",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3161949",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3161958",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3153171",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3162835",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3156016",
                        install_date=datetime.datetime(
                            2016, 6, 16, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3142042",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3145739",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3135983",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3146706",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3138612",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3146963",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3139398",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3148198",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3139914",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3148851",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3139940",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3149090",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3140735",
                        install_date=datetime.datetime(
                            2016, 4, 20, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3133043",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3134214",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3122648",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3134814",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3126587",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3126593",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3127220",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3141092",
                        install_date=datetime.datetime(
                            2016, 3, 28, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3072305",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3121212",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3121918",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3108664",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3123479",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3124000",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3124001",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3124275",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3109560",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3110329",
                        install_date=datetime.datetime(
                            2016, 2, 9, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB917607",
                        install_date=datetime.datetime(
                            2016, 2, 2, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2849697",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2849696",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2841134",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2670838",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2729094",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2834140",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2882822",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2912390",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2973351",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3104002",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3042058",
                        install_date=datetime.datetime(
                            2016, 1, 4, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2506014",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2506212",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2509553",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2511455",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2536275",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2544893",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2552343",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2560656",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2564958",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2570947",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2585542",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2604115",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2620704",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2621440",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2631813",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2643719",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2653956",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2654428",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2656356",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2667402",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2676562",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2685939",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2690533",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2698365",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2705219",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2706045",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2712808",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2718704",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2729452",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2736422",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2742599",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2758857",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2765809",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2770660",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2786081",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2789645",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2798162",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2807986",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2813430",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2836942",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2836943",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2839894",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2840149",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2840631",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2861698",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2862152",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2862330",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2862335",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2862973",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2864202",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2868038",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2868116",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2868626",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2871997",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2884256",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2887069",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2892074",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2893294",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2894844",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2900986",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2911501",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2929733",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB2931356",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2937610",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2943357",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2957189",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2968294",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2972100",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2972211",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2973112",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2973201",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2976897",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2977292",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2978120",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3006226",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3030377",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3045685",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3084135",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2984972",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3010788",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3031432",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3046017",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3072595",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3086255",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3108371",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2991963",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3011780",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3032655",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3046269",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3072630",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3087039",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3108381",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2992611",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3014029",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3033889",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3055642",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3072633",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3092601",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB2993651",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3018238",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3033929",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3059317",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3074543",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3097966",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3108670",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3000483",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3019978",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3035126",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3060716",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3075220",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3097989",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3109094",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3003743",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3020369",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB3035132",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3061518",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3076895",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3099862",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3109103",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3004361",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3021674",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3037574",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3068457",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3078601",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3101246",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3004375",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3022777",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3069392",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3080446",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3101722",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3005607",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3023215",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3042553",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3071756",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3081320",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3101746",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Security Update",
                    ),
                    Hotfix(
                        name="KB3112343",
                        install_date=datetime.datetime(
                            2016, 1, 3, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                    Hotfix(
                        name="KB976902",
                        install_date=datetime.datetime(
                            2010, 11, 21, 0, 0, tzinfo=datetime.timezone.utc
                        ),
                        description="Update",
                    ),
                ]
            ),
        ),
        plugins=Plugins(
            nodes=[
                Plugin(
                    comment=None,
                    family="Web Servers",
                    id=10107,
                    name="HTTP Server Type and Version",
                    owner=None,
                    source="Nessus",
                    severity="Info",
                    total_affected_assets=8,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Settings",
                    id=19506,
                    name="Nessus Scan Information",
                    owner=None,
                    source="Nessus",
                    severity="Info",
                    total_affected_assets=10,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Service detection",
                    id=22964,
                    name="Service Detection",
                    owner=None,
                    source="Nessus",
                    severity="Info",
                    total_affected_assets=9,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="General",
                    id=56984,
                    name="SSL / TLS Versions Supported",
                    owner=None,
                    source="Nessus",
                    severity="Info",
                    total_affected_assets=9,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
            ]
        ),
        purdue_level="Level3",
        revisions=Revisions(nodes=[]),
        risk=Risk(unresolved_events=0, total_risk=0.0),
        run_status="Unknown",
        run_status_time=datetime.datetime(1, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        segments=Segments(
            nodes=[
                Segment(
                    id=uuid.UUID("59161089-c6f7-4f8c-90a3-92f5be9d3b9d"),
                    name="Server / 10.100.30.X",
                    type="Segment",
                    key="AG1-20",
                    system_name="Server / 10.100.30.X",
                    vlan=None,
                    description=None,
                    asset_type="Server",
                    subnet="10.100.30.X",
                )
            ]
        ),
        serial=None,
        slot=None,
        super_type="Server",
        type="Server",
        vendor=None,
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
                            "plugins": {
                                "nodes": [
                                    {
                                        "id": 0,
                                        "name": "Open Port",
                                        "source": "NNM",
                                        "family": "Generic",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 98,
                                    },
                                    {
                                        "id": 12,
                                        "name": "Number of Hops",
                                        "source": "NNM",
                                        "family": "Generic",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 258,
                                    },
                                    {
                                        "id": 18,
                                        "name": "Generic Protocol Detection",
                                        "source": "NNM",
                                        "family": "Generic",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 281,
                                    },
                                    {
                                        "id": 65,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix 1100 Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 74,
                                        "name": "Ethernet Industrial Protocol (EtherNet/IP) Server Explicit Message Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 4,
                                    },
                                    {
                                        "id": 76,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix 1100 L16xxx < 10.000 HTTP Remote DoS",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "High",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 91,
                                        "name": "Ethernet/IP Protocol Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 26,
                                    },
                                    {
                                        "id": 110,
                                        "name": "UDP Activity",
                                        "source": "NNM",
                                        "family": "Generic",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 140,
                                    },
                                    {
                                        "id": 111,
                                        "name": "ICMP Activity",
                                        "source": "NNM",
                                        "family": "Generic",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 189,
                                    },
                                    {
                                        "id": 122,
                                        "name": "Ethernet/IP CIP List Identity Device Detection Response",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 4,
                                    },
                                    {
                                        "id": 132,
                                        "name": "Host Attribute Enumeration",
                                        "source": "NNM",
                                        "family": "Generic",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 276,
                                    },
                                    {
                                        "id": 280,
                                        "name": "OT Vendor Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 10,
                                    },
                                    {
                                        "id": 282,
                                        "name": "OT Serial Number Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 3,
                                    },
                                    {
                                        "id": 283,
                                        "name": "OT Protocol Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 68,
                                    },
                                    {
                                        "id": 284,
                                        "name": "OT Product Family Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 8,
                                    },
                                    {
                                        "id": 285,
                                        "name": "OT Model Name Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 3,
                                    },
                                    {
                                        "id": 286,
                                        "name": "OT Firmware Version Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 7,
                                    },
                                    {
                                        "id": 500028,
                                        "name": "Rockwell (CVE-2012-6442)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 6,
                                    },
                                    {
                                        "id": 500036,
                                        "name": "Rockwell (CVE-2012-6436)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 13,
                                    },
                                    {
                                        "id": 500038,
                                        "name": "Rockwell (CVE-2015-6486)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Medium",
                                        "vprScore": 5.8,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500043,
                                        "name": "Rockwell (CVE-2015-6488)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Medium",
                                        "vprScore": 3,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500082,
                                        "name": "Rockwell (CVE-2017-7901)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 4.7,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500084,
                                        "name": "Rockwell (CVE-2017-7899)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Critical",
                                        "vprScore": 5.9,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500089,
                                        "name": "Rockwell (CVE-2015-6492)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.4,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500110,
                                        "name": "Rockwell (CVE-2017-7903)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Critical",
                                        "vprScore": 5.9,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500111,
                                        "name": "Rockwell (CVE-2012-6440)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 6.7,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 13,
                                    },
                                    {
                                        "id": 500133,
                                        "name": "Rockwell (CVE-2012-6438)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 13,
                                    },
                                    {
                                        "id": 500134,
                                        "name": "Rockwell (CVE-2015-6490)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Critical",
                                        "vprScore": 5.9,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500147,
                                        "name": "Rockwell (CVE-2012-6441)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Medium",
                                        "vprScore": 3.4,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 13,
                                    },
                                    {
                                        "id": 500152,
                                        "name": "Rockwell (CVE-2015-6491)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Medium",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500181,
                                        "name": "Rockwell (CVE-2016-9334)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.4,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500198,
                                        "name": "Rockwell (CVE-2012-6435)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 13,
                                    },
                                    {
                                        "id": 500230,
                                        "name": "Rockwell (CVE-2016-9338)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Low",
                                        "vprScore": 1.4,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500253,
                                        "name": "Rockwell (CVE-2012-6437)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Critical",
                                        "vprScore": 6.7,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 13,
                                    },
                                    {
                                        "id": 500254,
                                        "name": "Rockwell (CVE-2012-6439)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 5.3,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 13,
                                    },
                                    {
                                        "id": 500278,
                                        "name": "Rockwell (CVE-2017-7924)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500281,
                                        "name": "Rockwell (CVE-2019-10955)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Medium",
                                        "vprScore": 3,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 2,
                                    },
                                    {
                                        "id": 500283,
                                        "name": "Rockwell (CVE-2017-7902)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Critical",
                                        "vprScore": 5.9,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500320,
                                        "name": "Rockwell (CVE-2017-7898)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Critical",
                                        "vprScore": 5.9,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500366,
                                        "name": "Rockwell (CVE-2020-6980)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Low",
                                        "vprScore": 1.4,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500367,
                                        "name": "Rockwell (CVE-2020-6984)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500368,
                                        "name": "Rockwell (CVE-2020-6988)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 3.6,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500369,
                                        "name": "Rockwell (CVE-2020-6990)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Critical",
                                        "vprScore": 5.9,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500542,
                                        "name": "Rockwell (CVE-2021-33012)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "High",
                                        "vprScore": 4.4,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 500693,
                                        "name": "Rockwell (CVE-2022-2179)",
                                        "source": "Tot",
                                        "family": "Tenable.ot",
                                        "severity": "Medium",
                                        "vprScore": 4.4,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720023,
                                        "name": "Rockwell Automation Allen-Bradley Multiple Controllers Multiple Versions Denial of Service",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "High",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720025,
                                        "name": "Rockwell Automation/Allen-Bradley Ethernet/IP Products Improper Authentication",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Critical",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720026,
                                        "name": "Rockwell Automation/Allen-Bradley Ethernet/IP Products Improper Input Validation",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "High",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720027,
                                        "name": "Rockwell Automation/Allen-Bradley Ethernet/IP Products Improper Access Control",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "High",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720028,
                                        "name": "Rockwell Automation/Allen-Bradley Ethernet/IP Products Authentication Bypass",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Critical",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720030,
                                        "name": "Rockwell Automation/Allen-Bradley Ethernet/IP Products Improper Access Control",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "High",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720068,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Multiple Devices SQL Injection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720069,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Multiple Devices XSS",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720070,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Multiple Devices Buffer Overflow",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Critical",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720071,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Multiple Devices Unrestricted Upload",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720072,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Multiple Devices Denial of Service",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "High",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720076,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix 1100 Multiple Devices Buffer Overflow",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Critical",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720102,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix 1400 Series B FRN < 21.2 Multiple Vulnerabilities (ICSA-18-095-01)",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720123,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Controllers <= 16.00 Improper Restriction of Excessive Authentication Attempts",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720124,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Controllers <= 16.00 Information Exposure",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720125,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Controllers <= 16.00 Predictable Value Range",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Critical",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720127,
                                        "name": "Rockwell Automation/Allen-Bradley MicroLogix Controllers <= 16.00 Week Password Requirements",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720209,
                                        "name": "Rockwell Automation Micrologix 1100 and 1400 <= 11 Unauthorized Privilege Access or DOS",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Critical",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720251,
                                        "name": "Rockwell Automation MicroLogix and CompactLogix Multiple Controllers Open Redirect",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720294,
                                        "name": "Rockwell Automation MicroLogix 1100 <= 16.0 and MicroLogix 1400 <= 21.003 Improper Authentication (ICSA-18-095-01)",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Medium",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 720295,
                                        "name": "Rockwell Automation MicroLogix 1100 and 1400 <= 16.0 Improper Information Handling (ICSA-17-115-04)",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Critical",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 752975,
                                        "name": "Rockwell Automation MicroLogix1100 1763-L16 Communications Adapter",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 1,
                                    },
                                    {
                                        "id": 764398,
                                        "name": "EtherNet/IP Protocol Port Server Detection",
                                        "source": "NNM",
                                        "family": "SCADA",
                                        "severity": "Info",
                                        "vprScore": None,
                                        "comment": None,
                                        "owner": None,
                                        "totalAffectedAssets": 4,
                                    },
                                ]
                            },
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
        plugins=Plugins(
            nodes=[
                Plugin(
                    comment=None,
                    family="Generic",
                    id=0,
                    name="Open Port",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=98,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Generic",
                    id=12,
                    name="Number of Hops",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=258,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Generic",
                    id=18,
                    name="Generic Protocol Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=281,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=65,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix 1100 Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=74,
                    name="Ethernet Industrial Protocol "
                         "(EtherNet/IP) Server Explicit "
                         "Message Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=4,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=76,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix 1100 L16xxx < 10.000 HTTP "
                         "Remote DoS",
                    owner=None,
                    source="NNM",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=91,
                    name="Ethernet/IP Protocol Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=26,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Generic",
                    id=110,
                    name="UDP Activity",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=140,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Generic",
                    id=111,
                    name="ICMP Activity",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=189,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=122,
                    name="Ethernet/IP CIP List Identity Device " "Detection Response",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=4,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Generic",
                    id=132,
                    name="Host Attribute Enumeration",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=276,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=280,
                    name="OT Vendor Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=10,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=282,
                    name="OT Serial Number Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=3,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=283,
                    name="OT Protocol Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=68,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=284,
                    name="OT Product Family Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=8,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=285,
                    name="OT Model Name Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=3,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=286,
                    name="OT Firmware Version Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=7,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500028,
                    name="Rockwell (CVE-2012-6442)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=6,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500036,
                    name="Rockwell (CVE-2012-6436)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=13,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500038,
                    name="Rockwell (CVE-2015-6486)",
                    owner=None,
                    source="Tot",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=5.8,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500043,
                    name="Rockwell (CVE-2015-6488)",
                    owner=None,
                    source="Tot",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=3.0,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500082,
                    name="Rockwell (CVE-2017-7901)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=4.7,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500084,
                    name="Rockwell (CVE-2017-7899)",
                    owner=None,
                    source="Tot",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=5.9,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500089,
                    name="Rockwell (CVE-2015-6492)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=3.4,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500110,
                    name="Rockwell (CVE-2017-7903)",
                    owner=None,
                    source="Tot",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=5.9,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500111,
                    name="Rockwell (CVE-2012-6440)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=13,
                    vpr_score=6.7,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500133,
                    name="Rockwell (CVE-2012-6438)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=13,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500134,
                    name="Rockwell (CVE-2015-6490)",
                    owner=None,
                    source="Tot",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=5.9,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500147,
                    name="Rockwell (CVE-2012-6441)",
                    owner=None,
                    source="Tot",
                    severity="Medium",
                    total_affected_assets=13,
                    vpr_score=3.4,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500152,
                    name="Rockwell (CVE-2015-6491)",
                    owner=None,
                    source="Tot",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500181,
                    name="Rockwell (CVE-2016-9334)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=3.4,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500198,
                    name="Rockwell (CVE-2012-6435)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=13,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500230,
                    name="Rockwell (CVE-2016-9338)",
                    owner=None,
                    source="Tot",
                    severity="Low",
                    total_affected_assets=1,
                    vpr_score=1.4,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500253,
                    name="Rockwell (CVE-2012-6437)",
                    owner=None,
                    source="Tot",
                    severity="Critical",
                    total_affected_assets=13,
                    vpr_score=6.7,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500254,
                    name="Rockwell (CVE-2012-6439)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=13,
                    vpr_score=5.3,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500278,
                    name="Rockwell (CVE-2017-7924)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500281,
                    name="Rockwell (CVE-2019-10955)",
                    owner=None,
                    source="Tot",
                    severity="Medium",
                    total_affected_assets=2,
                    vpr_score=3.0,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500283,
                    name="Rockwell (CVE-2017-7902)",
                    owner=None,
                    source="Tot",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=5.9,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500320,
                    name="Rockwell (CVE-2017-7898)",
                    owner=None,
                    source="Tot",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=5.9,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500366,
                    name="Rockwell (CVE-2020-6980)",
                    owner=None,
                    source="Tot",
                    severity="Low",
                    total_affected_assets=1,
                    vpr_score=1.4,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500367,
                    name="Rockwell (CVE-2020-6984)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500368,
                    name="Rockwell (CVE-2020-6988)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=3.6,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500369,
                    name="Rockwell (CVE-2020-6990)",
                    owner=None,
                    source="Tot",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=5.9,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500542,
                    name="Rockwell (CVE-2021-33012)",
                    owner=None,
                    source="Tot",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=4.4,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="Tenable.ot",
                    id=500693,
                    name="Rockwell (CVE-2022-2179)",
                    owner=None,
                    source="Tot",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=4.4,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720023,
                    name="Rockwell Automation Allen-Bradley "
                         "Multiple Controllers Multiple "
                         "Versions Denial of Service",
                    owner=None,
                    source="NNM",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720025,
                    name="Rockwell Automation/Allen-Bradley "
                         "Ethernet/IP Products Improper "
                         "Authentication",
                    owner=None,
                    source="NNM",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720026,
                    name="Rockwell Automation/Allen-Bradley "
                         "Ethernet/IP Products Improper Input "
                         "Validation",
                    owner=None,
                    source="NNM",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720027,
                    name="Rockwell Automation/Allen-Bradley "
                         "Ethernet/IP Products Improper Access "
                         "Control",
                    owner=None,
                    source="NNM",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720028,
                    name="Rockwell Automation/Allen-Bradley "
                         "Ethernet/IP Products Authentication "
                         "Bypass",
                    owner=None,
                    source="NNM",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720030,
                    name="Rockwell Automation/Allen-Bradley "
                         "Ethernet/IP Products Improper Access "
                         "Control",
                    owner=None,
                    source="NNM",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720068,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Multiple Devices SQL "
                         "Injection",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720069,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Multiple Devices XSS",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720070,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Multiple Devices Buffer "
                         "Overflow",
                    owner=None,
                    source="NNM",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720071,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Multiple Devices "
                         "Unrestricted Upload",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720072,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Multiple Devices Denial "
                         "of Service",
                    owner=None,
                    source="NNM",
                    severity="High",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720076,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix 1100 Multiple Devices "
                         "Buffer Overflow",
                    owner=None,
                    source="NNM",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720102,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix 1400 Series B FRN < 21.2 "
                         "Multiple Vulnerabilities "
                         "(ICSA-18-095-01)",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720123,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Controllers <= 16.00 "
                         "Improper Restriction of Excessive "
                         "Authentication Attempts",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720124,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Controllers <= 16.00 "
                         "Information Exposure",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720125,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Controllers <= 16.00 "
                         "Predictable Value Range",
                    owner=None,
                    source="NNM",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720127,
                    name="Rockwell Automation/Allen-Bradley "
                         "MicroLogix Controllers <= 16.00 Week "
                         "Password Requirements",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720209,
                    name="Rockwell Automation Micrologix 1100 "
                         "and 1400 <= 11 Unauthorized "
                         "Privilege Access or DOS",
                    owner=None,
                    source="NNM",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720251,
                    name="Rockwell Automation MicroLogix and "
                         "CompactLogix Multiple Controllers "
                         "Open Redirect",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720294,
                    name="Rockwell Automation MicroLogix 1100 "
                         "<= 16.0 and MicroLogix 1400 <= "
                         "21.003 Improper Authentication "
                         "(ICSA-18-095-01)",
                    owner=None,
                    source="NNM",
                    severity="Medium",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=720295,
                    name="Rockwell Automation MicroLogix 1100 "
                         "and 1400 <= 16.0 Improper "
                         "Information Handling "
                         "(ICSA-17-115-04)",
                    owner=None,
                    source="NNM",
                    severity="Critical",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=752975,
                    name="Rockwell Automation MicroLogix1100 "
                         "1763-L16 Communications Adapter",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=1,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
                Plugin(
                    comment=None,
                    family="SCADA",
                    id=764398,
                    name="EtherNet/IP Protocol Port Server " "Detection",
                    owner=None,
                    source="NNM",
                    severity="Info",
                    total_affected_assets=4,
                    vpr_score=None,
                    details=None,
                    affected_assets=None,
                ),
            ]
        ),
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


@pytest.mark.vcr()
def test_assets_list_vcr(api):
    """
    Tests the assets Graphql list iterator with cassettes
    """
    assets = api.assets.list(limit=2)
    assert isinstance(assets, OTGraphIterator)
    asset = assets.next()
    assert asset is not None
