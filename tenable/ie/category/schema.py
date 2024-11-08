from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
