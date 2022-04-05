'''
Test for assets schema
'''
import pytest
from marshmallow import ValidationError

from tenable.io.v3.vm.assets.schema import (AssetUpdateACRSchema,
                                            AssignTagsAssetSchema,
                                            ImportAssetSchema, MoveAssetSchema)
from tests.io.v3.vm.assets.objects import (NEGATIVE_ASSIGN_TAGS_SCHEMA,
                                           NEGATIVE_IMPORT_ASSET_SCHEMA,
                                           NEGATIVE_MOVE_ASSET_SCHEMA,
                                           NEGATIVE_UPDATE_ACR_SCHEMA)


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


@pytest.mark.parametrize("test_input", NEGATIVE_ASSIGN_TAGS_SCHEMA)
def test_tags_category_negative(test_input):
    '''
    Test for negative cases for assign tags schema
    '''
    schema = AssignTagsAssetSchema()
    with pytest.raises(ValidationError):
        schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_IMPORT_ASSET_SCHEMA)
def test_import_asset_negative(test_input):
    '''
    Test for negative cases for import asset schema
    '''
    schema = ImportAssetSchema()
    with pytest.raises(ValidationError):
        schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_MOVE_ASSET_SCHEMA)
def test_move_asset_negative(test_input):
    '''
    Test for negative cases for move asset schema
    '''
    schema = MoveAssetSchema()
    with pytest.raises(ValidationError):
        schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_UPDATE_ACR_SCHEMA)
def test_update_acr_negative(test_input):
    '''
    Test for negative cases for update acr schema
    '''
    schema = AssetUpdateACRSchema()
    with pytest.raises(ValidationError):
        schema.load(test_input)


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


def test_update_acr_schema():
    '''
    Test the update acr schema
    '''

    acr_data = {'reason': ['Business Critical'],
                'asset': [{
                    'fqdn': ['example.py.test'],
                    'ipv4': ['192.168.254.1'],
                    'netbios_name': 'SCCM',
                    'mac_address': ['00:00:00:00:00:00']
                }]}
    schema = AssetUpdateACRSchema()
    data = schema.dump(schema.load(acr_data))
    assert data == acr_data


def test_move_assets_schema():
    '''
    Test the move assets schema
    '''

    move_asset_data = {'source': '00000000-0000-0000-0000-000000000000',
                       'destination': 'b7584671-68e6-426b-a67c-6373778b8a0a',
                       'targets': ['127.0.0.1']
                       }
    move_asset_resp = {'source': '00000000-0000-0000-0000-000000000000',
                       'destination': 'b7584671-68e6-426b-a67c-6373778b8a0a',
                       'targets': '127.0.0.1'
                       }
    schema = MoveAssetSchema()
    data = schema.dump(schema.load(move_asset_data))
    assert data == move_asset_resp

    with pytest.raises(ValidationError):
        data['fqdn'] = 'something'
        schema.load(data)
