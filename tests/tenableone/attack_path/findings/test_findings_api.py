import json

import pytest
import responses

from tenable.tenableone.attack_path.findings.api import FindingIterator
from tenable.tenableone.attack_path.findings.schema import (
    FindingsPageSchema,
    TopAttackTechnique,
)


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
            "status": "accepted",
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


@pytest.mark.parametrize('filter_value', [
    {'operator': '==', 'key': 'priority', 'value': 'high'},
    '{"operator": "==", "key": "priority", "value": "high"}',
])
@responses.activate
def test_attack_path_findings_list_filter_sent_as_json(
    filter_value, tenable_one_api, finding
):
    """
    The API expects the filter as a JSON string; a dict must be serialized.
    """
    expected = json.dumps({'operator': '==', 'key': 'priority', 'value': 'high'})
    responses.get(
        'https://cloud.tenable.com/api/v1/t1/apa/findings',
        json={
            'page_number': 1, 'count': 1, 'total': 1, 'next': None,
            'data': [finding],
        },
        match=[responses.matchers.query_param_matcher(
            {'limit': 50, 'filter': expected}, strict_match=False
        )],
    )
    items = tenable_one_api.attack_path.findings.list(filter=filter_value, limit=50)
    assert next(items) == finding


TECHNIQUES_URL = 'https://cloud.tenable.com/api/v1/t1/apa/top-attack-techniques/search'
TECHNIQUE = {
    'mitre_id': 'T1021.001',
    'name': 'Remote Desktop Protocol',
    'technique_name': 'Remote Services',
    'priority': 'high',
    'state': 'open',
    'status': 'to_do',
    'tactics': ['Lateral Movement'],
    'mitigations': [],
    'malwares': [],
    'tools': [],
    'created': '2026-10-26T12:37:59Z',
    'last_updated_at': '2026-10-27T08:00:00Z',
    'serial_id': 1001,
    'vector_count': 3,
    'total_vector_count': 5,
    'critical_assets_count': 1,
    'total_critical_assets_count': 2,
    'assets_ids': [],
    'detection_ids': [],
    'weaknesses_ids': [],
    'groups': [],
    'source_information': [],
    'related_nodes': {'sources': [], 'targets': [], 'cause': {}},
}
TECHNIQUES_PAGINATION = {
    'total': 550,
    'offset': 100,
    'limit': 100,
    'sort': {'name': 'priority', 'order': 'desc'},
}


@responses.activate
def test_top_attack_techniques_search_defaults(tenable_one_api):
    responses.post(
        TECHNIQUES_URL,
        json={'data': [TECHNIQUE], 'pagination': TECHNIQUES_PAGINATION},
        match=[responses.matchers.query_param_matcher({})],
    )
    response = tenable_one_api.attack_path.findings.top_attack_techniques_search()
    assert responses.calls[0].request.body is None
    assert response.total == 550
    assert response.pagination.sort.name == 'priority'
    assert isinstance(response.data[0], TopAttackTechnique)
    assert response.data[0].mitre_id == 'T1021.001'
    assert response.data[0].related_nodes == {'sources': [], 'targets': [], 'cause': {}}


@responses.activate
@pytest.mark.parametrize('exclude_resolved, sent', [(True, 'true'), (False, 'false')])
def test_top_attack_techniques_search_params(tenable_one_api, exclude_resolved, sent):
    responses.post(
        TECHNIQUES_URL,
        json={'data': [], 'pagination': TECHNIQUES_PAGINATION},
        match=[
            responses.matchers.query_param_matcher(
                {
                    'limit': 100,
                    'offset': 100,
                    'sort': 'priority:desc',
                    'exclude_resolved': sent,
                }
            )
        ],
    )
    tenable_one_api.attack_path.findings.top_attack_techniques_search(
        limit=100, offset=100, sort='priority:desc', exclude_resolved=exclude_resolved
    )


@responses.activate
def test_top_attack_techniques_search_filter_body(tenable_one_api):
    filter_data = {
        'operator': 'and',
        'value': [
            {'property': 'priority', 'operator': 'eq', 'value': 'high'},
            {'property': 'status', 'operator': 'eq', 'value': 'to_do'},
        ],
    }
    responses.post(
        TECHNIQUES_URL,
        json={'data': [], 'pagination': TECHNIQUES_PAGINATION},
        match=[responses.matchers.json_params_matcher(filter_data, strict_match=True)],
    )
    tenable_one_api.attack_path.findings.top_attack_techniques_search(filter=filter_data)


@responses.activate
@pytest.mark.parametrize('value', ['false', 0])
def test_top_attack_techniques_search_exclude_resolved_typeerror(tenable_one_api, value):
    with pytest.raises(TypeError):
        tenable_one_api.attack_path.findings.top_attack_techniques_search(
            exclude_resolved=value
        )
    assert len(responses.calls) == 0


def test_top_attack_techniques_search_keyword_only(tenable_one_api):
    with pytest.raises(TypeError):
        tenable_one_api.attack_path.findings.top_attack_techniques_search(100)
