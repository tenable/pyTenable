from marshmallow import fields, pre_load, validate as v
from tenable.ad.base.schema import CamelCaseSchema, convert_keys_to_camel


class LDAPConfigurationAllowedGroupsSchema(CamelCaseSchema):
    name = fields.Str(required=True)
    default_role_ids = fields.List(fields.Int(), required=True,
                                   validate=v.Length(min=1))
    default_profile_id = fields.Int(required=True)

    @pre_load
    def convert(self, data, **kwargs):
        return convert_keys_to_camel(data)


class LDAPConfigurationSchema(CamelCaseSchema):
    enabled = fields.Bool()
    url = fields.Str()
    search_user_dn = fields.Str()
    search_user_password = fields.Str(allow_none=True)
    user_search_base = fields.Str()
    user_search_filter = fields.Str()
    allowed_groups = fields.Nested(
        LDAPConfigurationAllowedGroupsSchema, many=True)

    @pre_load
    def convert(self, data, **kwargs):
        return convert_keys_to_camel(data, special=['search_user_dn'])
