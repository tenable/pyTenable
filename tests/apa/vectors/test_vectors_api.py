import pytest
import responses

from tenable.apa.vectors.api import VectorIterator
from tenable.apa.vectors.schema import VectorsPageSchema


@pytest.fixture
def vector():
    return {
        "is_new": False,
        "vector_id": "FFF93960363C0755F8C9D93E241DD26E",
        "path": None,
        "techniques": [
            {
                "source_information": "[{\"provider_detection_id\":\"71246\",\"detection_code\":\"Enumerate Local Group Memberships\",\"reason_code_name\":null,\"asset_id\":\"0bd1382d-8ba7-41d7-bc27-0e874c655737\",\"id\":\"nessus:71246\",\"provider_code\":\"NESSUS\",\"type\":\"nessus plugin\",\"reason_id\":null},{\"provider_detection_id\":\"44401\",\"detection_code\":\"Microsoft Windows SMB Service Config Enumeration\",\"reason_code_name\":null,\"asset_id\":\"0bd1382d-8ba7-41d7-bc27-0e874c655737\",\"id\":\"nessus:44401\",\"provider_code\":\"NESSUS\",\"type\":\"nessus plugin\",\"reason_id\":null},{\"provider_detection_id\":\"64582\",\"detection_code\":\"Netstat Connection Information\",\"reason_code_name\":null,\"asset_id\":\"0bd1382d-8ba7-41d7-bc27-0e874c655737\",\"id\":\"nessus:64582\",\"provider_code\":\"NESSUS\",\"type\":\"nessus plugin\",\"reason_id\":null}]",
                "name": "Remote Desktop Protocol-251714",
                "full_name": "Remote Desktop Protocol-251714",
                "asset_id": "",
                "id": 82656,
                "labels": [
                    "Procedure"
                ],
                "procedure_uuid": "b5277de3-2f05-4cf0-96a3-6764c3d230e1"
            },
            {
                "source_information": "[{\"provider_detection_id\":\"64582\",\"detection_code\":\"Netstat Connection Information\",\"reason_code_name\":null,\"asset_id\":\"fa6ed6d3-9426-4f7e-b414-373eace37f5f\",\"id\":\"nessus:64582\",\"provider_code\":\"NESSUS\",\"type\":\"nessus plugin\",\"reason_id\":null},{\"provider_detection_id\":\"191947\",\"detection_code\":null,\"reason_code_name\":null,\"asset_id\":\"fa6ed6d3-9426-4f7e-b414-373eace37f5f\",\"id\":\"nessus:191947\",\"provider_code\":\"NESSUS\",\"plugin_name\":\"\",\"type\":\"nessus plugin\",\"reason_id\":null},{\"provider_detection_id\":\"191947\",\"detection_code\":null,\"reason_code_name\":null,\"asset_id\":\"fa6ed6d3-9426-4f7e-b414-373eace37f5f\",\"id\":\"nessus:191947\",\"provider_code\":\"NESSUS\",\"plugin_name\":\"KB5035857: Windows 2022 / Azure Stack HCI 22H2 Security Update (March 2024)\",\"type\":\"nessus plugin\",\"reason_id\":null},{\"provider_detection_id\":\"CVE-2024-21444\",\"detection_code\":\"CVE-2024-21444\",\"reason_code_name\":null,\"id\":\"CVE-2024-21444\",\"provider_code\":\"NVD\",\"type\":\"CVE\",\"reason_id\":null}]",
                "name": "Exploitation of Remote Services-20940:251097",
                "full_name": "Exploitation of Remote Services-20940:251097",
                "asset_id": "",
                "id": 117132,
                "labels": [
                    "Procedure"
                ],
                "procedure_uuid": "6b2c9d79-3e10-4a6b-b5c2-0c60c453533b"
            },
            {
                "source_information": "[{\"provider_detection_id\":\"64582\",\"detection_code\":\"Netstat Connection Information\",\"reason_code_name\":null,\"asset_id\":\"037cb20a-5b0a-40d2-b5cc-3306ee005429\",\"id\":\"nessus:64582\",\"provider_code\":\"NESSUS\",\"type\":\"nessus plugin\",\"reason_id\":null},{\"provider_detection_id\":\"160937\",\"detection_code\":null,\"reason_code_name\":null,\"asset_id\":\"037cb20a-5b0a-40d2-b5cc-3306ee005429\",\"id\":\"nessus:160937\",\"provider_code\":\"NESSUS\",\"plugin_name\":\"\",\"type\":\"nessus plugin\",\"reason_id\":null},{\"provider_detection_id\":\"CVE-2022-26936\",\"detection_code\":\"CVE-2022-26936\",\"reason_code_name\":null,\"id\":\"CVE-2022-26936\",\"provider_code\":\"NVD\",\"type\":\"CVE\",\"reason_id\":null}]",
                "name": "Exploitation of Remote Services-12298:19222",
                "full_name": "Exploitation of Remote Services-12298:19222",
                "asset_id": "",
                "id": 27049,
                "labels": [
                    "Procedure"
                ],
                "procedure_uuid": "eb10d48d-9d4d-4ca2-bfa4-3ec6d76cbec5"
            }
        ],
        "nodes": [
            {
                "name": "Domain Users",
                "full_name": "APADOMAIN\\domain users",
                "asset_id": "",
                "id": 252949,
                "labels": [
                    "WindowsObject",
                    "Domain",
                    "Group"
                ]
            },
            {
                "name": "APAENG",
                "full_name": "apaeng.apadomain.internal",
                "asset_id": "0bd1382d-8ba7-41d7-bc27-0e874c655737",
                "id": 251098,
                "labels": [
                    "WindowsObject",
                    "Domain",
                    "Computer",
                    "WindowsServer"
                ]
            },
            {
                "name": "APADC",
                "full_name": "apadc.apadomain.internal",
                "asset_id": "fa6ed6d3-9426-4f7e-b414-373eace37f5f",
                "id": 251097,
                "labels": [
                    "WindowsObject",
                    "Domain",
                    "Computer",
                    "WindowsServer",
                    "DomainController"
                ]
            },
            {
                "name": "baaaaacnet",
                "full_name": "baaaaacnet.indegy.local",
                "asset_id": "037cb20a-5b0a-40d2-b5cc-3306ee005429",
                "id": 19222,
                "labels": [
                    "Computer",
                    "WindowsServer"
                ]
            }
        ],
        "findings_names": [],
        "name": "Domain Users can reach baaaaacnet by exploiting CVE-2024-21444 and CVE-2022-26936",
        "summary": "An attacker can use Domain Users to access baaaaacnet by exploiting two vulnerabilities. First, the attacker exploits CVE-2024-21444 on APAENG to gain access to APADC. Then, the attacker exploits CVE-2022-26936 on APADC to gain access to baaaaacnet. This attack path is possible because Domain Users is a member of Remote Desktop Users, which has remote desktop access to APAENG. This attack path is dangerous because it allows an attacker to gain access to a critical asset, baaaaacnet, by exploiting two vulnerabilities.",
        "first_aes": None,
        "last_acr": 9
    }


@responses.activate
def test_vectors_list_iterator(api, vector):
    responses.get('https://cloud.tenable.com/apa/api/discover/v1/vectors',
                  json={"page_number": 1, "count": 10, "total": 21,
                        "data": [vector for _ in range(10)]},
                  match=[responses.matchers.query_param_matcher({"limit": 10})])

    responses.get('https://cloud.tenable.com/apa/api/discover/v1/vectors',
                  json={"page_number": 2, "count": 10, "total": 21,
                        "data": [vector for _ in range(10)]},
                  match=[responses.matchers.query_param_matcher({"limit": 10, "page_number": 2})])

    responses.get('https://cloud.tenable.com/apa/api/discover/v1/vectors',
                  json={"page_number": 3, "count": 10, "total": 21,
                        "data": [vector for _ in range(1)]},
                  match=[responses.matchers.query_param_matcher({"limit": 10, "page_number": 3})])

    vectors: VectorIterator = api.vectors.list()

    for v in vectors:
        assert v == vector
    assert vectors.total == 21
    assert vectors.count == 21


@responses.activate
def test_vectors_list_vector_page_response(api, vector):
    vectors_page_response = {"page_number": 1, "count": 10, "total": 10,
                             "data": [vector for _ in range(10)]}
    responses.get('https://cloud.tenable.com/apa/api/discover/v1/vectors',
                  json=vectors_page_response,
                  match=[responses.matchers.query_param_matcher({"limit": 10})])

    vectors_page: VectorsPageSchema = api.vectors.list(return_iterator=False)

    assert vectors_page == VectorsPageSchema().load(vectors_page_response)
