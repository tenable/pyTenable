from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class AttackerKnownToolSchema(CamelCaseSchema):
    name = fields.Str()
    url = fields.Str(allow_none=True)
    author = fields.Str(allow_none=True)
    link = fields.Str(allow_none=True)
    type = fields.Str()


class ResourcesSchema(CamelCaseSchema):
    name = fields.Str()
    url = fields.Str()
    type = fields.Str()


class VulnerabilityDetailSchema(CamelCaseSchema):
    detail = fields.Str(allow_none=True)


class RecommendationSchema(CamelCaseSchema):
    name = fields.Str()
    description = fields.Str()
    exec_summary = fields.Str(allow_none=True)
    detail = fields.Str(allow_none=True)
    resources = fields.Nested(ResourcesSchema, many=True)
    attacker_known_tools = fields.Nested(AttackerKnownToolSchema,
                                         allow_none=True, many=True)


class CheckerSchema(CamelCaseSchema):
    id = fields.Int()
    codename = fields.Str()
    remediation_cost = fields.Int()
    category_id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    exec_summary = fields.Str(allow_none=True)
    vulnerability_detail = fields.Nested(VulnerabilityDetailSchema)
    attacker_known_tools = fields.Nested(AttackerKnownToolSchema,
                                         allow_none=True, many=True)
    resources = fields.Nested(ResourcesSchema, many=True)
    recommendation = fields.Nested(RecommendationSchema)
