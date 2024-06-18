'''Syslog schema'''
from marshmallow import fields, validate as v, validates_schema
from tenable.ie.base.schema import CamelCaseSchema, camelcase


class SyslogSchema(CamelCaseSchema):
    id = fields.Int()
    ip = fields.Str(required=True, validate=v.Length(min=1))
    port = fields.Int(required=True, dump_default=514)
    protocol = fields.Str(dump_default='UDP')
    tls = fields.Bool()
    criticity_threshold = fields.Int(required=True)
    description = fields.Str(allow_none=True)
    filter_expression = fields.Mapping(allow_none=True)
    input_type = fields.Str()
    directories = fields.List(fields.Int(), required=True, allow_none=True,
                              validate=v.Length(min=1))
    checkers = fields.List(fields.Int(), required=True, allow_none=True,
                           validate=v.Length(min=1))
    attack_types = fields.List(fields.Int(), required=True, allow_none=True,
                               validate=v.Length(min=1))
    profiles = fields.List(fields.Int(), required=True, allow_none=True,
                           validate=v.Length(min=1))
    should_notify_on_initial_full_security_check = fields.Bool(required=True)

    @validates_schema
    def validate_fields(self, data, **kwargs):
        if data.get('protocol'):
            data['protocol'] = data.get('protocol').upper()
            if data['protocol'] == 'UDP':
                data['tls'] = False
        if data.get('input_type'):
            if data['input_type'] == 'ad_object_changes':
                data['input_type'] = camelcase('ad_object_changes')
                data['criticity_threshold'] = 0
