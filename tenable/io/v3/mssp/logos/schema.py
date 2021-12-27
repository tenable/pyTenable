'''
Logos API Endpoint Schemas
'''
import io

from marshmallow import Schema, ValidationError, fields


class FileField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, io.BufferedIOBase):
            return value
        else:
            raise ValidationError('Invalid value')


class LogoSchema(Schema):
    '''
    Schema for actions in logos/api.py
    '''
    account_ids = fields.List(fields.Str())
    logo_id = fields.Str()
    logo = FileField()
    name = fields.Str()
