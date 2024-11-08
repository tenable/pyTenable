from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema, last_word_uppercase


class ApplicationSettingsSchema(CamelCaseSchema):
    class Meta:
        case_convertors = {
            'smtp_use_start_tls': last_word_uppercase
        }

    user_registration = fields.Bool()
    keep_audit_log = fields.Bool()
    log_retention_period = fields.Int()
    smtp_server_address = fields.Str(allow_none=True)
    smtp_server_port = fields.Int(allow_none=True)
    smtp_account = fields.Str(allow_none=True)
    smtp_account_password = fields.Str(allow_none=True)
    smtp_use_start_tls = fields.Bool()
    tls = fields.Bool()
    email_sender = fields.Str()
    default_role_ids = fields.List(fields.Int())
    default_profile_id = fields.Int()
    internal_certificate = fields.Str(allow_none=True)
