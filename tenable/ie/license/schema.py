from marshmallow import fields
from tenable.ie.base.schema import CamelCaseSchema, last_word_uppercase


class LicenseSchema(CamelCaseSchema):
    class Meta:
        case_convertors = {
            'expiration_date_utc': last_word_uppercase
        }

    customer_name = fields.Str()
    max_active_user_count = fields.Int()
    current_active_user_count = fields.Int()
    expiration_date_utc = fields.DateTime()
    in_app_eula = fields.Bool()
    features = fields.List(fields.Str())
    license = fields.Str()
    license_type = fields.Str(data_key='type')
