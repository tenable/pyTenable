from marshmallow import Schema, fields


class PolicySchema(Schema):
    '''
    Base schema for validating Policies API
    '''
    uuid = fields.Str()
    settings = fields.Dict()
    credentials = fields.Dict()
