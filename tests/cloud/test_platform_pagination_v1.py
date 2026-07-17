import pytest
from pydantic import ValidationError

from tenable.cloud.platform.models.pagination_v1 import (
    BaseFilterV1Resp,
    QueryFilterV1,
)


@pytest.fixture
def filter_resp():
    return BaseFilterV1Resp.model_validate(
        {
            "wildcard_fields": ["name"],
            "sort": {"max_sort_fields": 1, "sortable_fields": ["name"]},
            "filters": [
                {
                    "name": "name",
                    "readable_name": "Name",
                    "operators": ["eq", "match"],
                    "control": {
                        "readable_regex": "Uppercase only",
                        "type": "entry",
                        "regex": "^[A-Z]+$",
                    },
                }
            ],
        }
    )


def test_is_valid_filter_match(filter_resp):
    assert filter_resp.is_valid_filter("name", "eq", "TEST") is True


def test_is_valid_filter_no_match(filter_resp):
    assert filter_resp.is_valid_filter("other", "eq", "test") is False


def test_query_filter_v1_from_string():
    f = QueryFilterV1.model_validate("name:eq:test")
    assert f.field == "name"
    assert f.operator == "eq"
    assert f.value == "test"


def test_query_filter_v1_invalid_string():
    with pytest.raises(ValueError, match="not in a valid filter format"):
        QueryFilterV1.model_validate("invalid-format")


def test_query_filter_v1_from_tuple():
    f = QueryFilterV1.model_validate(("name", "eq", "test"))
    assert f.field == "name"
    assert f.operator == "eq"
    assert f.value == "test"


def test_query_filter_v1_from_dict():
    f = QueryFilterV1.model_validate({"field": "name", "operator": "eq", "value": "test"})
    assert f.field == "name"
    assert f.operator == "eq"
    assert f.value == "test"


def test_query_filter_v1_with_valid_context(filter_resp):
    f = QueryFilterV1.model_validate(
        {"field": "name", "operator": "eq", "value": "TEST"},
        context={"filters": filter_resp},
    )
    assert f.field == "name"


def test_query_filter_v1_with_invalid_context(filter_resp):
    with pytest.raises(ValidationError, match="doesn't match any valid filter schemas"):
        QueryFilterV1.model_validate(
            {"field": "other", "operator": "eq", "value": "test"},
            context={"filters": filter_resp},
        )


def test_query_filter_v1_serialize():
    f = QueryFilterV1(field="name", operator="eq", value="test")
    assert f.model_dump() == "name:eq:test"
