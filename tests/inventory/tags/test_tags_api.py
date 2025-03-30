import json

import pytest
import responses

from tenable.inventory.schema import Field, Properties


@pytest.fixture
def tags_properties_response() -> dict[str, list[dict]]:
    return {"properties": [{"key": "tag_id", "readable_name": "Tag ID",
                            "control": {"type": "STRING", "multiple_allowed": True,
                                        "regex": {"hint": "01234567-abcd-ef01-2345-6789abcdef01",
                                                  "expression": "[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*"}},
                            "operators": ["=", "!=", "exists", "not exists"], "sortable": True, "filterable": True,
                            "weight": 0.0, "object_types": [],
                            "description": "# Tag ID \n\n## A way to group assets\n\nIn Exposure Management, a Tag ID is a unique identifier associated with a Tag. Tags are user-defined labels or markers applied to assets to categorize and organize them based on specific criteria, such as function, location, department, or risk level. \n\nHere's how Tag IDs are used:\n\n- **Grouping and Filtering:** Tag IDs enable you to easily group and filter assets based on shared characteristics. For example, you could use a Tag ID for \"High Risk\" to quickly identify all assets tagged with that specific risk level.\n- **Automation and Reporting:** Tag IDs can be used in automated workflows and reporting to streamline asset management tasks. You can generate reports on assets with specific Tag IDs to gain insights into their security posture or compliance status.\n- **Dynamic Grouping:** Tags and their associated IDs provide a flexible way to group assets dynamically. As asset attributes or risk profiles change, you can easily update their tags to reflect their current status. \n"}]}


@responses.activate
def test_properties_list(api, tags_properties_response):
    # Arrange
    responses.get('https://cloud.tenable.com/inventory/api/v1/tags/properties',
                  json=tags_properties_response,
                  match=[responses.matchers.query_param_matcher({})])
    # Act
    tags_properties_result: list[Field] = api.tags.list_properties()
    # Assert
    assert tags_properties_result == Properties(**tags_properties_response).properties
