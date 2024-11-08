from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class AttackTypesResourceSchema(CamelCaseSchema):
    name = fields.Str()
    url = fields.URL()
    type = fields.Str()


class AttackTypesVectorTemplateReplacementsSchema(CamelCaseSchema):
    name = fields.Str()
    value_type = fields.Str()


class AttackTypesSchema(CamelCaseSchema):
    id = fields.Int()
    name = fields.Str()
    yara_rules = fields.Str()
    description = fields.Str()
    workload_quota = fields.Int()
    mitre_attack_description = fields.Str()
    criticity = fields.Str()
    resources = fields.Nested(AttackTypesResourceSchema, many=True)
    vector_template = fields.Str()
    vector_template_replacements = fields.Nested(
        AttackTypesVectorTemplateReplacementsSchema, many=True)
