from marshmallow import fields, validate as v
from tenable.ie.base.schema import CamelCaseSchema, last_word_uppercase


class LDAPConfigurationAllowedGroupsSchema(CamelCaseSchema):
    name = fields.Str(required=True)
    default_role_ids = fields.List(fields.Int(), required=True,
                                   validate=v.Length(min=1))
    default_profile_id = fields.Int(required=True)


class LDAPConfigurationSchema(CamelCaseSchema):
    class Meta:
        case_convertors = {
            'search_user_dn': last_word_uppercase
        }
    enabled = fields.Bool()
    url = fields.Str()
    search_user_dn = fields.Str()
    search_user_password = fields.Str(allow_none=True)
    user_search_base = fields.Str()
    user_search_filter = fields.Str()
    allowed_groups = fields.Nested(
        LDAPConfigurationAllowedGroupsSchema, many=True)
    enable_sasl_binding = fields.Bool()
