from marshmallow import fields, Schema


class ControlSchema(Schema):
    type = fields.Str()
    multiple_allowed = fields.Bool()
    regex = fields.Dict(allow_none=True)
    selection = fields.List(fields.Dict(), allow_none=True)


class AssetFieldSchema(Schema):
    key = fields.Str()
    readable_name = fields.Str()
    control = fields.Nested(ControlSchema)
    operators = fields.List(fields.Str())
    sortable = fields.Bool()
    filterable = fields.Bool()
    weight = fields.Float()
    object_types = fields.List(fields.Str())
    description = fields.Str()


class AssetsPropertiesSchema(Schema):
    asset_id = fields.Nested(AssetFieldSchema)
    asset_class = fields.Nested(AssetFieldSchema)
    asset_name = fields.Nested(AssetFieldSchema)
    sources = fields.Nested(AssetFieldSchema)
    created_at = fields.Nested(AssetFieldSchema)
    first_observed_at = fields.Nested(AssetFieldSchema)
    acr = fields.Nested(AssetFieldSchema)
    is_licensed = fields.Nested(AssetFieldSchema)
