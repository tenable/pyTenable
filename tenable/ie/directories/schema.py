from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema


class DirectorySchema(CamelCaseSchema):
    infrastructure_id = fields.Int()
    id = fields.Int()
    name = fields.Str()
    ip = fields.Str()
    dns = fields.Str()
    type = fields.Str()
    ldap_port = fields.Int()
    global_catalog_port = fields.Int()
    smb_port = fields.Int()
    ldap_crawling_status = fields.Str()
    sysvol_crawling_status = fields.Str()
    honey_account_ad_object_id = fields.Str(allow_none=True)
    honey_account_distinguished_name = fields.Str(allow_none=True)
    honey_account_configuration_status = fields.Str()
    ldap_initialized = fields.Int(allow_none=True)
    sysvol_initialized = fields.Int(allow_none=True)
