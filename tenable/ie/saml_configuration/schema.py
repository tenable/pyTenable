from marshmallow import fields, validate as v
from tenable.ie.base.schema import CamelCaseSchema


class AllowedGroupSchema(CamelCaseSchema):
    name = fields.Str(required=True)
    default_profile_id = fields.Int(required=True)
    default_role_ids = fields.List(fields.Int(required=True),
                                   validate=v.Length(min=1))


class SAMLConfigurationSchema(CamelCaseSchema):
    enabled = fields.Bool()
    provider_login_url = fields.Str(allow_none=True)
    encryption_certificate = fields.Str()
    signature_certificate = fields.Str(allow_none=True)
    service_provider_url = fields.Str()
    assert_endpoint = fields.Str()
    activate_created_users = fields.Bool()
    allowed_groups = fields.Nested(AllowedGroupSchema, many=True)