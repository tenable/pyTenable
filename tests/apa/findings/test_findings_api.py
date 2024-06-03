import pytest
import responses

@pytest.fixture
def finding():
    return {
        "data": [
            {
                "mitre_id": "attack-pattern--1ecfdab8-7d59-4c98-95d4-dc41970f57fc",
                "mitigations": [
                    "Privileged Account Management",
                    "User Training",
                    "Password Policies"
                ],
                "malwares": [
                    "CosmicDuke",
                    "IceApple"
                ],
                "tools": [
                    "Impacket",
                    "Pupy",
                    "CrackMapExec",
                    "gsecdump",
                    "Mimikatz",
                    "LaZagne",
                    "AADInternals"
                ],
                "groups": [
                    "APT29",
                    "Ke3chang",
                    "OilRig",
                    "Threat Group-3390",
                    "menuPass",
                    "Dragonfly",
                    "MuddyWater",
                    "Leafminer",
                    "APT33"
                ],
                "name": "LSA Secrets",
                "priority": "low",
                "procedureName": "LSA Secrets-11552",
                "relatedNodes": {
                    "sources": [
                        {
                            "name": "MSSQLSERVER",
                            "fullname": "sql1.cymptom.labs\\MSSQLSERVER",
                            "id": "11552",
                            "labels": [
                                "Service"
                            ],
                            "isCrownJewel": False,
                            "vulnerability_id": None,
                            "asset_id": None
                        }
                    ],
                    "targets": [
                        {
                            "name": "Administrator",
                            "fullname": "CYMPTOM\\administrator",
                            "id": "3738",
                            "labels": [
                                "User",
                                "WindowsObject",
                                "Domain",
                                "DomainAdmin"
                            ],
                            "isCrownJewel": False,
                            "vulnerability_id": None,
                            "asset_id": None
                        }
                    ],
                    "cause": {
                        "name": "MSSQLSERVER",
                        "fullname": "sql1.cymptom.labs\\MSSQLSERVER",
                        "id": "11552",
                        "labels": [
                            "Service"
                        ],
                        "isCrownJewel": False,
                        "vulnerability_id": None,
                        "asset_id": None
                    }
                },
                "tactics": [
                    "Credential Access"
                ],
                "critical_assets_count": 1,
                "total_critical_assets_count": 44,
                "totalVectorCount": 58,
                "vectorCount": 1,
                "state": "open",
                "status": "to_do",
                "created": 1712659006,
                "is_active": True,
                "has_history": None,
                "last_updated_at": "2024-06-01T00:53:53.513328",
                "source_information": [
                    {
                        "id": "nessus:72684",
                        "asset_id": "e118d26d-ada9-492f-a3b9-e6cc5d9bbca7",
                        "type": "nessus plugin",
                        "provider_detection_id": "72684",
                        "provider_code": "NESSUS",
                        "reason_id": None,
                        "reason_code_name": None,
                        "detection_code": "Enumerate Users via WMI"
                    },
                    {
                        "id": "nessus:44401",
                        "asset_id": "e118d26d-ada9-492f-a3b9-e6cc5d9bbca7",
                        "type": "nessus plugin",
                        "provider_detection_id": "44401",
                        "provider_code": "NESSUS",
                        "reason_id": None,
                        "reason_code_name": None,
                        "detection_code": "Microsoft Windows SMB Service Config Enumeration"
                    },
                    {
                        "id": "nessus:71246",
                        "asset_id": "e118d26d-ada9-492f-a3b9-e6cc5d9bbca7",
                        "type": "nessus plugin",
                        "provider_detection_id": "71246",
                        "provider_code": "NESSUS",
                        "reason_id": None,
                        "reason_code_name": None,
                        "detection_code": "Enumerate Local Group Memberships"
                    }
                ],
                "weaknesses_ids": [],
                "assets_ids": [],
                "detection_ids": [
                    "NESSUS:72684",
                    "NESSUS:44401",
                    "NESSUS:71246"
                ],
                "serial_id": 1411651
            }
        ],
        "next": "eyJsYXN0X3NlcmlhbF9pZCI6IDE0MTE2NTEsICJvcmRlcl9ieV9maWVsZF9uYW1lIjogbnVsbCwgImxhc3Rfb3JkZXJfYnlfdmFsdWUiOiBudWxsfQ==",
        "page_number": None,
        "count": 1,
        "total": 28
    }


@responses.activate
def test_findings_list_iterator(api, finding):
    pass
    # resp = {
    #     'data': [{}],
    #     'next': "",
    #     'page_number': "",
    #     'total': "",
    #     'count': ""
    # }
    # responses.get('https://cloud.tenable.com/apa/findings-api/v1/findings',
    #               json=resp)
    # resp = api.findings.list(
    #     profile_id=1,
    #     resource_type='infrastructure',
    #     resource_value='1'
    # )
    # assert isinstance(resp, list)
    # assert len(resp) == 1
    # assert resp[0]['id'] == 1
    # assert resp[0]['directory_id'] == 1
    # assert resp[0]['attack_type_id'] == 1


@responses.activate
def test_attack_list_parameterized(api):
    pass
    # responses.add(responses.GET,
    #               f'{RE_BASE}/profiles/1/attacks'
    #               f'?resourceValue=1'
    #               f'&includeClosed=false'
    #               f'&dateEnd=2022-12-31T18%3A30%3A00%2B00%3A00'
    #               f'&limit=10'
    #               f'&search=Something'
    #               f'&attackTypeIds=1'
    #               f'&attackTypeIds=2'
    #               f'&dateStart=2021-12-31T18%3A30%3A00%2B00%3A00'
    #               f'&resourceType=infrastructure'
    #               f'&order=desc',
    #               json=[{
    #                   'attackTypeId': 1,
    #                   'date': '2022-01-14T07:24:50.424Z',
    #                   'dc': 'dc',
    #                   'destination': {
    #                       'hostname': 'test',
    #                       'ip': '192.168.1.1',
    #                       'type': 'computer'
    #                   },
    #                   'directoryId': 1,
    #                   'id': 1,
    #                   'isClosed': False,
    #                   'source': {
    #                       'hostname': 'Unknown',
    #                       'ip': '127.0.0.1',
    #                       'type': 'computer'
    #                   },
    #                   'vector': {
    #                       'attributes': [{
    #                           'name': 'source_hostname',
    #                           'value': 'Unknown',
    #                           'valueType': 'string'
    #                       }],
    #                       'template': 'template'
    #                   }
    #               }]
    #               )
    # resp = api.attacks.list(
    #     profile_id=1,
    #     resource_type='infrastructure',
    #     resource_value='1',
    #     attack_type_ids=[1, 2],
    #     include_closed='false',
    #     limit='10',
    #     order='desc',
    #     search='Something',
    #     date_end='2022-12-31T18:30:00.000Z',
    #     date_start='2021-12-31T18:30:00.000Z'
    # )
    # assert isinstance(resp, list)
    # assert len(resp) == 1
    # assert resp[0]['id'] == 1
    # assert resp[0]['directory_id'] == 1
    # assert resp[0]['attack_type_id'] == 1
    # assert resp[0]['is_closed'] is False
