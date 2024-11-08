import pytest
from marshmallow import ValidationError
from tenable.ie.topology.schema import TopologySchema


@pytest.fixture
def topology_schema():
    return {'profileId': '1'}


def test_topology_schema(topology_schema):
    test_response = {
        "infrastructures": [{
            "uid": "string",
            "name": "some_name",
            "known": True,
            "directories": [{
                "uid": "string",
                "name": "string",
                "known": True,
                "id": 0
            }]
        }],
        "trusts": [{
            "from": "string",
            "to": "string",
            "hazardLevel": "regular",
            "attributes": ["string"]
        }]
    }
    schema = TopologySchema()
    req = schema.dump(schema.load(topology_schema))
    assert req['profileId'] == '1'
    assert isinstance(test_response, dict)
    assert test_response.get('infrastructures')[0]['name'] == 'some_name'
    with pytest.raises(ValidationError):
        topology_schema['new_val'] = 'something'
        schema.load(topology_schema)
