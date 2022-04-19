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
    fqdn = fields.List(fields.Str())
    ipv4 = fields.List(fields.Str())
    netbios_name = fields.Str()
    mac_address = fields.List(fields.Str())
    id = fields.Str()

    class Meta:
        unknown = INCLUDE

    @validates_schema(pass_many=True)
    def validate_required_attributes_exist(self, data, **kwargs):
        if not (data.get('fqdn')
                or data.get('ipv4')
                or data.get('netbios_name')
                or data.get('mac_address')):
            raise ValidationError('Each asset object requires a value for at '
                                  'least one of the following properties: '
                                  'fqdn, ipv4, netbios_name, mac_address.'
                                  )

    @post_dump(pass_original=True)
    def keep_unknowns(self, output, orig, **kwargs):
        for key in orig:
            if key not in output:
                output[key] = orig[key]
        return output


class AssetUpdateACRSchema(Schema):
    '''
    Update ACR API Schema
    '''
    REASON_LIST = ['Business Critical', 'In Scope For Compliance',
                   'Existing Mitigation Control', 'Dev only',
                   'Key drivers does not match', 'Other']

    reason = fields.List(fields.Str(validate=v.OneOf(REASON_LIST)))
    asset = fields.List(fields.Nested(AssetSchema))
    acr_score = fields.Int(validate=v.Range(min=1, max=10))
    note = fields.Str()


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
    def post_serialization(self, data, **kwargs):
        '''
        Convert a list of target assets into a comma-separated string.
        '''
        data['targets'] = ','.join(data.get('targets', []))
        return data


class BulkDeleteSchema(Schema):
    '''
    Bulk Delete Asset API Schema
    '''
    hard_delete = fields.Str()
    query = fields.Dict()
