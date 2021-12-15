from marshmallow import Schema, fields


class PoliciesSchema(Schema):
    '''
    Base schema for validating Policies API
    '''
    uuid = fields.Str()
    settings = fields.Dict()
    credentials = fields.Dict()
