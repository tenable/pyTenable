from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class DashboardSchema(CamelCaseSchema):
    name = fields.Str()
    order = fields.Int()
    id = fields.Int()
    user_id = fields.Int()
    dashboard_id = fields.Str()
