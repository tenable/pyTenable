'''
V3 API Endpoints Schemas
'''
from marshmallow import INCLUDE, Schema, ValidationError, fields
from marshmallow import validate as v
from marshmallow.decorators import post_dump, validates_schema


class AssignTagsAssetSchema(Schema):
    '''
    Assign Tags API Schema
    '''

    assets = fields.List(fields.UUID())
    tags = fields.List(fields.UUID())
    action = fields.String(validate=v.OneOf(['add', 'remove']))


class AssetSchema(Schema):
    '''
    Asset API Schema
    '''
    class Meta:
        unknown = INCLUDE

    @validates_schema
    def validate_required_attributes_exist(self, data, **kwargs):
        if not (data.get('fqdn')
                or data.get('ipv4')
                or data.get('netbios_name')
                or data.get('mac_address')):
            raise ValidationError('Each asset object requires a value for at '
                                  'least one of the following properties: '
                                  'fqdn, ipv4, netbios_name, mac_address.'
                                  )


class ImportAssetSchema(Schema):
    '''
    Import Asset API Schema
    '''
    assets = fields.List(fields.Nested(AssetSchema),
                         validate=v.Length(min=1),
                         required=True
                         )
    source = fields.Str(required=True)


class MoveAssetSchema(Schema):
    '''
    Move Asset API Schema
    '''

    source = fields.UUID()
    destination = fields.UUID()
    targets = fields.List(fields.IPv4())

    @post_dump
    def post_serialization(
        self, data, **kwargs
    ):
        '''
        Convert a list of target assets into a comma-separated string.
        '''
        data['targets'] = ','.join(data.get('targets', []))
        return data
