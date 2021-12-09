from marshmallow import fields, Schema


class InfrastructureSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    login = fields.Str()
    password = fields.Str()
    directories = fields.List(fields.Int())
    infrastructure_id = fields.Str()
