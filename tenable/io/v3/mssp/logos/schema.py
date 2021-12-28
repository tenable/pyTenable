'''
Logos API Endpoint Schemas
'''
from marshmallow import Schema, fields


class LogoSchema(Schema):
    '''
    Schema for actions in logos/api.py
    '''
    account_ids = fields.List(fields.Str())
    logo_id = fields.Str()
