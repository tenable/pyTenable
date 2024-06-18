from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema, BoolInt


class DevianceAttributesSchema(CamelCaseSchema):
    name = fields.Str()
    value = fields.Str()


class DevianceReplacementsSchema(CamelCaseSchema):
    name = fields.Str()
    value = fields.Str()
    value_type = fields.Str()


class DevianceDescriptionSchema(CamelCaseSchema):
    template = fields.Str()
    replacements = fields.Nested(DevianceReplacementsSchema, many=True)


class DevianceSchema(CamelCaseSchema):
    id = fields.Int()
    directory_id = fields.Int()
    checker_id = fields.Int()
    profile_id = fields.Int()
    ad_object_id = fields.Int()
    reason_id = fields.Int()
    resolved_at = fields.DateTime(allow_none=True)
    event_date = fields.DateTime()
    ignore_until = fields.DateTime(allow_none=True)
    deviance_provider_id = fields.Str()
    attributes = fields.Nested(DevianceAttributesSchema, many=True)
    description = fields.Nested(DevianceDescriptionSchema)
    createdEventId = fields.Int()
    resolvedEventId = fields.Int(allow_none=True)
    page = fields.Int(allow_none=True)
    per_page = fields.Int(allow_none=True)
    batch_size = fields.Int(allow_none=True)
    max_pages = fields.Int(allow_none=True)
    max_items = fields.Int(allow_none=True)
    last_identifier_seen = fields.Int()
    resolved = BoolInt()
    expression = fields.Mapping()
    show_ignored = fields.Bool()
    checkers = fields.List(fields.Int())
    reasons = fields.List(fields.Int())
    date_start = fields.DateTime()
    date_end = fields.DateTime()
