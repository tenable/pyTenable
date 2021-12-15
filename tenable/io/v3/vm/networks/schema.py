'''
Networks API Endpoint Schemas
'''
from marshmallow import Schema, fields


class NetworkSchema(Schema):
    '''
    Schema for edit and create functions in networks/api.py

    Args:

    '''
    name = fields.Str()
    description = fields.Str(dump_default='')
    assets_ttl_days = fields.Int()
    scanner_uuids = fields.List(fields.UUID())
