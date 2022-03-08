'''
Exclusion API Endpoint Schemas
'''

from datetime import datetime

from marshmallow import Schema, fields, validate
from marshmallow.decorators import post_dump, pre_load, validates_schema


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
        if 'freq' in data:
            data['freq'] = str(data['freq']).upper()

        if data.get('freq') == 'WEEKLY':
            if 'byweekday' not in data:
                data['byweekday'] = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']
            data['byweekday'] = [str(i).upper() for i in data['byweekday']]
            data.pop('bymonthday', None)
        elif data.get('freq') == 'MONTHLY':
            if 'bymonthday' not in data:
                data['bymonthday'] = datetime.today().day
            data.pop('byweekday', None)
        else:
            data.pop('bymonthday', None)
            data.pop('byweekday', None)
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
    starttime = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    endtime = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    timezone = fields.Str()
    rrules = fields.Nested(RulesSchema)

    @validates_schema
    def validate_timezone(self, data, **kwargs):
        if data['enabled'] is True:
            if 'starttime' not in data:
                raise ValueError('starttime field is required.')

        if data['enabled'] is True:
            if 'endtime' not in data:
                raise ValueError('endtime field is required.')

        if 'timezone' in data:
            if data['timezone'] not in self.context['timezones']:
                raise ValueError('Invalid timezone field')


class ExclusionSchema(Schema):
    '''
    Schema for Exclusion API
    '''
    name = fields.Str(required=True)
    description = fields.Str()
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
