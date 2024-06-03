import pytest
import responses

from tenable.apa.findings.api import FindingIterator
from tenable.apa.findings.schema import FindingsPageSchema


@pytest.fixture
def findings_page_response():
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
def test_findings_list_iterator(api, findings_page_response):

    responses.get('https://cloud.tenable.com/apa/findings-api/v1/findings',
                  json=findings_page_response)

    findings: FindingIterator = api.findings.list(sort_filed='last_updated_at', sort_order='desc', filter='value',
                                                  limit=1)

    for f in findings:
        assert f == findings_page_response['data'][0]

    assert len(responses.calls) == 28
    for i, c in enumerate(responses.calls):
        if i == 0:
            assert c.request.url == 'https://cloud.tenable.com/apa/findings-api/v1/findings?limit=1&filter=value&sort_filed=last_updated_at&sort_order=desc'
        else:
            assert c.request.url == 'https://cloud.tenable.com/apa/findings-api/v1/findings?next=eyJsYXN0X3NlcmlhbF9pZCI6IDE0MTE2NTEsICJvcmRlcl9ieV9maWVsZF9uYW1lIjogbnVsbCwgImxhc3Rfb3JkZXJfYnlfdmFsdWUiOiBudWxsfQ%3D%3D&limit=1&filter=value&sort_filed=last_updated_at&sort_order=desc'


@responses.activate
def test_findings_list_findings_page_response(api, findings_page_response):

    responses.get('https://cloud.tenable.com/apa/findings-api/v1/findings',
                  json=findings_page_response)

    findings_page: FindingsPageSchema = api.findings.list(return_iterator=False)

    assert findings_page == FindingsPageSchema().load(findings_page_response)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://cloud.tenable.com/apa/findings-api/v1/findings?limit=50"
