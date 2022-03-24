'''
Policies API endpoint schema
'''
from marshmallow import Schema, fields


class PolicySchema(Schema):
    '''
    Base schema for validating Policies API
    '''
    uuid = fields.UUID()
    settings = fields.Dict()
    credentials = fields.Dict()
