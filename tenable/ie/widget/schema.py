from marshmallow import fields, validate as v
from tenable.ie.base.schema import CamelCaseSchema


class WidgetDataOptionsSchema(CamelCaseSchema):
    type = fields.Str()
    duration = fields.Int()
    interval = fields.Str()
    active = fields.Bool()
    directory_ids = fields.List(fields.Int())
    profile_id = fields.Int()
    checker_ids = fields.List(fields.Str())
    reason_ids = fields.List(fields.Str())


class WidgetDisplayOptionsSchema(CamelCaseSchema):
    label = fields.Str()
    category_id = fields.Int()


class WidgetSeriesSchema(CamelCaseSchema):
    data_options = fields.Nested(WidgetDataOptionsSchema)
    display_options = fields.Nested(WidgetDisplayOptionsSchema)


class WidgetOptionSchema(CamelCaseSchema):
    type = fields.Str(
        validate=v.OneOf(['BigNumber', 'LineChart', 'BarChart',
                          'SecurityCompliance', 'StepChart']))
    series = fields.Nested(WidgetSeriesSchema, many=True)


class WidgetSchema(CamelCaseSchema):
    id = fields.Int()
    widget_id = fields.Int()
    dashboard_id = fields.Int()
    title = fields.Str()
    pos_x = fields.Int()
    pos_y = fields.Int()
    width = fields.Int()
    height = fields.Int()
