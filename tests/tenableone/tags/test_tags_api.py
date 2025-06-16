import json

import pytest
import responses

from tenable.tenableone.inventory.schema import Field, Properties, SortDirection, Operator, PropertyFilter, QueryMode
from tenable.tenableone.tags.schema import Tags


@pytest.fixture
def tags_properties_response() -> dict[str, list[dict]]:
    return {"properties": [{"key": "tag_id", "readable_name": "Tag ID",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "regex": {"hint": "01234567-abcd-ef01-2345-6789abcdef01",
                                                  "expression": "[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*"}},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0, "object_types": [],
                            "description": "# Tag ID \n\n## A way to group assets\n\nIn Exposure Management, a Tag ID is a unique identifier associated with a Tag. Tags are user-defined labels or markers applied to assets to categorize and organize them based on specific criteria, such as function, location, department, or risk level. \n\nHere's how Tag IDs are used:\n\n- **Grouping and Filtering:** Tag IDs enable you to easily group and filter assets based on shared characteristics. For example, you could use a Tag ID for \"High Risk\" to quickly identify all assets tagged with that specific risk level.\n- **Automation and Reporting:** Tag IDs can be used in automated workflows and reporting to streamline asset management tasks. You can generate reports on assets with specific Tag IDs to gain insights into their security posture or compliance status.\n- **Dynamic Grouping:** Tags and their associated IDs provide a flexible way to group assets dynamically. As asset attributes or risk profiles change, you can easily update their tags to reflect their current status. \n"}]}


@pytest.fixture
def tags_response() -> dict:
    return {
        "values": [
            {
                "id": "d33ae4f1-cc87-42c0-956a-045aa73c33a6",
                "name": "neq-ap",
                "product": "TENABLE_IO",
                "asset_count": 5870,
                "weakness_severity_counts": {
                    "low": 892,
                    "medium": 4597,
                    "high": 923,
                    "critical": 168,
                    "total": 6580
                },
                "total_weakness_count": 6580,
                "tag": "DYNAMIC",
                "extra_properties": {
                    "tag_category_name": "AWS Custom",
                    "aes_average": 148
                }
            }
        ],
        "total_count": 1,
        "offset": 0,
        "limit": 100,
        "sort_by": "tag_name",
        "sort_direction": "asc"
    }


@responses.activate
def test_properties_list(tenable_one_api, tags_properties_response):
    # Arrange
    responses.get('https://cloud.tenable.com/api/v1/t1/tags/properties',
                  json=tags_properties_response,
                  match=[responses.matchers.query_param_matcher({})])
    # Act
    tags_properties_result: list[Field] = tenable_one_api.tags.list_properties()
    # Assert
    assert tags_properties_result == Properties(**tags_properties_response).properties


@responses.activate
def test_list(tenable_one_api, tags_response):
    query_text = "neq-ap"
    query_mode = QueryMode.SIMPLE
    filters = [PropertyFilter(property="tag_name", operator=Operator.EQUAL, value=["neq-ap"])]
    extra_properties = ["tag_category_name"]
    offset = 0
    limit = 100
    sort_by = "tag_name"
    sort_direction = SortDirection.ASC
    timezone = "UTC"

    payload = {
        "search": {
            "query": {
                "text": query_text,
                "mode": query_mode.value
            },
            "filters": [filter.model_dump(mode='json') for filter in filters]
        },
        "extra_properties": extra_properties,
        "offset": offset,
        "limit": limit,
        "sort_by": sort_by,
        "sort_direction": sort_direction.value,
        "timezone": timezone
    }
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/tags',
        json=tags_response,
        match=[responses.matchers.body_matcher(params=json.dumps(payload))]
    )
    # Act
    tags: Tags = tenable_one_api.tags.list(
        query_text=query_text,
        query_mode=query_mode,
        filters=filters,
        extra_properties=extra_properties,
        offset=offset,
        limit=limit,
        sort_by=sort_by,
        sort_direction=sort_direction,
        timezone=timezone
    )
    # Assert
    assert tags == Tags(**tags_response)
