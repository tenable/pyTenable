import pytest
import responses

from tenable.tenableone.attack_path.findings.api import FindingIterator
from tenable.tenableone.attack_path.findings.schema import FindingsPageSchema


@pytest.fixture
def finding():
    return {"mitre_id": "attack-pattern--1ecfdab8-7d59-4c98-95d4-dc41970f57fc",
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


@responses.activate
def test_findings_list_iterator(tenable_one_api, finding):
    responses.get('https://cloud.tenable.com/api/v1/t1/apa/findings',
                  json={"page_number": 1, "count": 50, "total": 100,
                        "next": "123",
                        "data": [finding for _ in range(50)]},
                  match=[responses.matchers.query_param_matcher({"limit": 50})])

    responses.get('https://cloud.tenable.com/api/v1/t1/apa/findings',
                  json={"page_number": 2, "count": 50, "total": 100,
                        "next": "123",
                        "data": [finding for _ in range(50)]},
                  match=[responses.matchers.query_param_matcher(
                      {"limit": 50,
                       "next": "123"})])

    responses.get('https://cloud.tenable.com/api/v1/t1/apa/findings',
                  json={"page_number": None, "count": 0, "total": 0,
                        "next": None,
                        "data": []},
                  match=[responses.matchers.query_param_matcher(
                      {"limit": 50,
                       "next": "123"})])

    findings: FindingIterator = tenable_one_api.attack_path.findings.list()

    for f in findings:
        assert f == finding
    assert findings.total == 100
    assert findings.count == 100


@responses.activate
def test_findings_list_findings_page_response(tenable_one_api, finding):
    findings_page_response = {"page_number": 1, "count": 50, "total": 100,
                              "next": "123",
                              "data": [finding for _ in range(50)]}
    responses.get('https://cloud.tenable.com/api/v1/t1/apa/findings',
                  json=findings_page_response,
                  match=[responses.matchers.query_param_matcher({"limit": 50})])

    responses.get('https://cloud.tenable.com/api/v1/t1/apa/findings',
                  json={"page_number": None, "count": 0, "total": 0,
                        "next": None,
                        "data": []},
                  match=[responses.matchers.query_param_matcher({"limit": 50, "next": "123"})])

    findings_page: FindingsPageSchema = tenable_one_api.attack_path.findings.list(return_iterator=False)

    assert findings_page == FindingsPageSchema(**findings_page_response)
