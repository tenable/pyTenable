import pytest

from tenable.ot.graphql.definitions import SchemaBase
from tenable.ot.schema.base import AssetInfo


def test_schema_missing_data_class():
    schema = SchemaBase()
    with pytest.raises(ValueError, match="dataclass must be set for"):
        schema.to_object({})


def test_schema_invalid_data():
    schema = SchemaBase()
    schema.dataclass = AssetInfo
    with pytest.raises(ValueError, match="data must be of type dict"):
        schema.to_object(None)
