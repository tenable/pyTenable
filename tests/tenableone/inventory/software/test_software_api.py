import json

import pytest
import responses

from tenable.tenableone.inventory.schema import Field, Properties, QueryMode, PropertyFilter, Operator, \
    SortDirection
from tenable.tenableone.inventory.software.schema import SoftwareValues


@pytest.fixture
def software_properties_response() -> dict[str, list[dict]]:
    return {"data": [{"key": "cpe", "readable_name": "Common Platform Enumeration",
                            "control": {"type": "STRING", "multiple_allowed": False,
                                        "regex": {"hint": "cpe:2.3:o:microsoft:windows_7:-:sp2:*:*:*:*:*:*",
                                                  "expression": ".*"}},
                            "operators": ["contains", "not contains", "=", "!=", "exists", "not exists"],
                            "sortable": True, "filterable": True,
                            "description": "# Common Platform Enumeration\n## A software inventory technique\n\nCommon Platform Enumeration (CPE) is a software inventory technique that identifies the software installed on a device. CPE uses a standardized format to identify software, which makes it easier to track and manage software assets.\n\nHere are some key points to understand about CPE:\n- **CPE is a standard format for identifying software**. The CPE format consists of a vendor name, product name, version, and edition. This makes it easy to identify software and track changes over time.\n- **CPE can be used to identify both installed and uninstalled software**. This makes it a valuable tool for software inventory and asset management.\n- **CPE can be used to generate reports on software usage**. This information can be used to make decisions about software licensing and usage.\n\n## Example:\n```\nCPE:2.3:Microsoft:Windows_Server:2012_R2:SP1\n```\n\nThis CPE identifies Microsoft Windows Server 2012 R2 Service Pack 1.\n"}]}


@pytest.fixture
def software_response() -> dict:
    return {"data": [{"application": ".net_framework", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 2}},
                       {"application": "edge", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}},
                       {"application": "onedrive", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 3}},
                       {"application": "remote_desktop_connection", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}},
                       {"application": "sql_server", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}},
                       {"application": "windows_defender", "publisher": "microsoft", "type": ["APPLICATION"],
                        "extra_properties": {"asset_sources": ["T.IO"], "cpe_count": 1}}], 
            "pagination": {
                "total": 6,
                "offset": 0, 
                "limit": 100,
                "sort": {
                    "name": "application",
                    "order": "desc"
                }
            }
            }


@responses.activate
def test_properties_list(tenable_one_api, software_properties_response):
    # Arrange
    responses.get('https://cloud.tenable.com/api/v1/t1/inventory/software/properties',
                  json=software_properties_response,
                  match=[responses.matchers.query_param_matcher({})])
    # Act
    software_properties_result: list[Field] = tenable_one_api.inventory.software.list_properties()
    # Assert
    assert software_properties_result == Properties(**software_properties_response).data


@responses.activate
def test_list(tenable_one_api, software_response):
    query_text = "accurics"
    query_mode = QueryMode.SIMPLE
    filters = [PropertyFilter(property="property", operator=Operator.EQUAL, value=["value"])]

    extra_properties = ["apa_asset_total_paths_count"]
    offset = 0
    limit = 100
    sort_by = "application"
    sort_direction = SortDirection.DESC

    # Expected query parameters
    expected_params = {
        "extra_properties": "apa_asset_total_paths_count",
        "offset": 0,
        "limit": 100,
        "sort": "application:desc"
    }

    # Expected request body with query structure
    expected_body = {
        "query": {
            "text": query_text,
            "mode": query_mode.value
        },
        "filters": [filter.model_dump(mode='json') for filter in filters]
    }

    responses.add(responses.POST,
                  'https://cloud.tenable.com/api/v1/t1/inventory/software/search',
                  json=software_response,
                  match=[
                      responses.matchers.body_matcher(params=json.dumps(expected_body)),
                      responses.matchers.query_param_matcher(expected_params)
                  ])
    # Act
    software: SoftwareValues = tenable_one_api.inventory.software.list(
        query_text=query_text,
        query_mode=query_mode,
        filters=filters,
        extra_properties=extra_properties,
        offset=offset, 
        limit=limit,
        sort_by=sort_by,
        sort_direction=sort_direction
    )
    # Assert
    assert software == SoftwareValues(**software_response)
