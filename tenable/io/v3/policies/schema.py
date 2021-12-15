from marshmallow import Schema, fields


class PoliciesSchema(Schema):
    uuid = fields.Str()
    settings = fields.Dict()
    credentials = fields.Dict()
