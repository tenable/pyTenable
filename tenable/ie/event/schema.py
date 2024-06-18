from marshmallow import fields, validate as v
from tenable.ie.base.schema import CamelCaseSchema


class SearchDirectionSchema(CamelCaseSchema):
    column = fields.Str()
    direction = fields.Str(validate=v.OneOf(['asc', 'desc']),
                           dump_default='desc')


class EventSchema(CamelCaseSchema):
    directory_id = fields.Int()
    id = fields.Int()
    expression = fields.Mapping()
    order = fields.Nested(SearchDirectionSchema)
    directory_ids = fields.List(fields.Int())
    profile_id = fields.Int()
    date_start = fields.DateTime()
    date_end = fields.DateTime()
    ad_object_id = fields.Int()
    type = fields.Str()
    date = fields.DateTime()
