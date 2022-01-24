'''
Exclusion API Endpoint Schemas
'''

from marshmallow import Schema, fields, post_dump, pre_load, validate
from marshmallow.exceptions import ValidationError


class RulesSchema(Schema):
    '''
    Schema for rrules field for ScheduleSchema class
    '''
    freq = fields.Str(
        validate=validate.OneOf(
            ['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
        ),
    )
    interval = fields.Int()
    byweekday = fields.List(
        fields.Str(validate=validate.OneOf(
            ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])
        )
    )
    bymonthday = fields.Int(
        validate=validate.OneOf(list(range(1, 32)))
    )

    @pre_load
    def pre_serialization(self, data, **kwargs):
        if 'byweekday' in data:
            for idx, val in enumerate(data['byweekday']):
                if isinstance(val, str):
                    data['byweekday'][idx] = val.upper()
                else:
                    ValidationError(
                        f'{val} is not the valid input for weekdays'
                    )
        return data

    @post_dump
    def post_serialization(self, data, **kwargs):
        if 'byweekday' in data:
            if data['byweekday']:
                data['byweekday'] = ','.join(data['byweekday'])

        return data


class ScheduleSchema(Schema):
    '''
    Schema for schedule field for AgentExclusionSchema class
    '''
    enabled = fields.Boolean()
    starttime = fields.DateTime(format='%Y-%m-%dT%H:%M:%SZ')
    endtime = fields.DateTime(format='%Y-%m-%dT%H:%M:%SZ')
    timezone = fields.Str()
    rrules = fields.Nested(RulesSchema)


class ExclusionSchema(Schema):
    '''
    Schema for Exclusion API
    '''
    name = fields.Str(required=True)
    description = fields.Str(dump_default='')
    members = fields.List(fields.Str(), required=True)
    schedule = fields.Nested(
        ScheduleSchema,
        required=True
    )
    network_id = fields.UUID(
        dump_default='00000000-0000-0000-0000-000000000000'
    )

    @post_dump
    def post_serialization(self, data, **kwargs):
        data['members'] = ','.join(data['members'])
        return data
