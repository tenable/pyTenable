'''
Tests for scanner groups schema
'''
import pytest
from marshmallow import ValidationError

from tenable.io.v3.vm.scanner_groups.schema import ScannerGroupSchema


def test_scanner_group_base():
    data_req = {
        'name': 'test1',
        'type': 'load_balancing',
        'routes': ['127.0.0.1']
    }
    schema = ScannerGroupSchema()
    data = schema.dump(schema.load(data_req))
    assert data == data_req

    with pytest.raises(ValidationError):
        data['test'] = 'test'
        schema.load(data)
