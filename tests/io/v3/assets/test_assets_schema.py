'''
Test for assets schema
'''
import pytest
from marshmallow import ValidationError

from tenable.io.v3.assets.schema import (AssignTagsAssetSchema,
                                         ImportAssetSchema, MoveAssetSchema)


def test_assign_tags_schema():
    '''
    Test the assign tags schema
    '''

    assign_tag_data = {
        'assets': ['00000000-0000-0000-0000-000000000000'],
        'tags': ['00000000-0000-0000-0000-000000000000'],
        'action': 'add'
    }
    schema = AssignTagsAssetSchema()
    data = schema.dump(schema.load(assign_tag_data))
    assert data == assign_tag_data

    with pytest.raises(ValidationError):
        data = 'something'
        schema.load(data)


def test_import_assets_schema():
    '''
    Test the import assets schema
    '''

    import_asset_data = {'source': 'example_source',
                         'assets': [{
                             'fqdn': ['example.py.test'],
                             'ipv4': ['192.168.254.1'],
                             'netbios_name': 'example',
                             'mac_address': ['00:00:00:00:00:00']
                         }]}
    schema = ImportAssetSchema()
    data = schema.dump(schema.load(import_asset_data))
    assert data == import_asset_data

    with pytest.raises(ValidationError):
        data['fqdn'] = 'something'
        schema.load(data)


def test_move_assets_schema():
    '''
    Test the move assets schema
    '''

    move_asset_data = {'source': '00000000-0000-0000-0000-000000000000',
                       'destination': '00000000-0000-0000-0000-000000000000',
                       'targets': ['127.0.0.1']
                       }
    move_asset_resp = {'source': '00000000-0000-0000-0000-000000000000',
                       'destination': '00000000-0000-0000-0000-000000000000',
                       'targets': '127.0.0.1'
                       }
    schema = MoveAssetSchema()
    data = schema.dump(schema.load(move_asset_data))
    assert data == move_asset_resp

    with pytest.raises(ValidationError):
        data['fqdn'] = 'something'
        schema.load(data)
