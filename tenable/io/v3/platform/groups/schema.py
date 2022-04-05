'''
Platform Groups API Endpoint Schemas
'''
from marshmallow import Schema, fields


class PlatformGroupSchema(Schema):
    '''
    Schema for platform_groups API
    '''
    name = fields.Str()
    group_id = fields.UUID()
    user_id = fields.UUID()
