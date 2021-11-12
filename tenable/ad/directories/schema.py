from marshmallow import fields
from tenable.ad.base.schema import CamelCaseSchema


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
