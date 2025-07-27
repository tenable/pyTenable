import json
from urllib.parse import urljoin

import pytest
import responses

from tenable.tenableone.inventory.findings.schema import Findings
from tenable.tenableone.inventory.schema import (
    Field,
    Properties,
    QueryMode,
    PropertyFilter,
    Operator,
    SortDirection,
)

BASE_URL = "https://cloud.tenable.com/"


@pytest.fixture
def findings_properties_response() -> dict[str, list[dict]]:
    return {
        "data": [
            {
                "key": "finding_id",
                "readable_name": "Finding ID",
                "is_extra_property": True,
                "control": {
                    "type": "STRING",
                    "multiple_allowed": False,
                    "regex": {
                        "hint": "01234567-abcd-ef01-2345-6789abcdef01",
                        "expression": "[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*"
                    }
                },
                "operators": [
                    "=",
                    "!="
                ],
                "displayable": True,
                "sortable": True,
                "filterable": True,
                "deprecated": False,
                "is_key_property": False,
                "description": """# Finding ID\n## A unique identifier for a security issue\nEach security issue identified by Exposure Management is assigned a unique Finding ID. This ID helps to track and manage individual findings throughout their lifecycle.\n\nHere"s why Finding IDs are important:\n- **Unique Identification:** Each finding receives a distinct ID, preventing confusion when dealing with multiple security issues.\n- **Tracking and Management:** The ID helps track a finding"s status, remediation efforts, and history over time.\n- **Reporting and Analysis:** Finding IDs enable efficient reporting and analysis of security issues, allowing you to identify trends and patterns.\n- **Integration:** Finding IDs can be integrated with other security tools and systems for streamlined workflows.\n"""
            }
        ]
    }


@pytest.fixture
def findings_response() -> dict:
    return {
        "data": [
            {
                "id": "000caf26-c44f-5db1-891f-4d98383812b9",
                "name": "Dangerous SYSVOL share path",
                "severity": "HIGH",
                "state": "ACTIVE",
                "asset_id": "ea3305bf-6067-4f5d-a381-ffbd9eda2296",
            }
        ],
        "pagination": {
            "total": 1,
            "offset": 0,
            "limit": 100,
            "sort": {
                "name": "name",
                "order": "asc"
            }
        },
    }

@responses.activate
def test_properties_list(tenable_one_api, findings_properties_response):
    # Arrange
    endpoint = "/api/v1/t1/inventory/findings/properties"
    full_url = urljoin(BASE_URL, endpoint)

    responses.get(full_url, json=findings_properties_response, match=[responses.matchers.query_param_matcher({})])
    # Act
    finding_properties_result: list[Field] = tenable_one_api.inventory.findings.list_properties()
    # Assert
    assert finding_properties_result == Properties(**findings_properties_response).data


# @responses.activate
# def test_list(tenable_one_api, findings_response):
#     query_text = "Dangerous SYSVOL share path"
#     query_mode = QueryMode.SIMPLE
#     filters = [PropertyFilter(property="name", operator=Operator.EQUAL, value=["Dangerous SYSVOL share path"])]
#     extra_properties = ["product_code"]
#     offset = 0
#     limit = 100
#     sort_by = "name"
#     sort_direction = SortDirection.ASC
#
#     # Expected query parameters
#     expected_params = {
#         "extra_properties": ",".join(extra_properties),
#         "offset": offset,
#         "limit": limit,
#         "sort": f"{sort_by}:{sort_direction}"
#     }
#
#     payload = {
#         "query": {
#             "text": query_text,
#             "mode": query_mode.value
#         },
#         "filters": [filter_.model_dump(mode="json") for filter_ in filters]
#     }
#     endpoint = "/api/v1/t1/inventory/findings/search"
#     full_url = urljoin(BASE_URL, endpoint)
#     responses.add(
#         responses.POST,
#         full_url,
#         json=findings_response,
#         match=[
#             responses.matchers.body_matcher(params=json.dumps(payload)),
#             responses.matchers.query_param_matcher(expected_params)
#         ]
#     )
#     # Act
#     findings: Findings = tenable_one_api.inventory.findings.list(
#         query_text=query_text,
#         query_mode=query_mode,
#         filters=filters,
#         extra_properties=extra_properties,
#         offset=offset,
#         limit=limit,
#         sort_by=sort_by,
#         sort_direction=sort_direction,
#     )
#     # Assert
#     assert findings == Findings(**findings_response)
