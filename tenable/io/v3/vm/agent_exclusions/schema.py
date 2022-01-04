'''
Agent Exclusion API Endpoint Schemas
'''
from datetime import datetime, timedelta

from marshmallow import Schema, fields, post_dump, validate, pre_load
from marshmallow.exceptions import ValidationError


class RulesSchema(Schema):
    '''
    Schema for rrules field for ScheduleSchema class 
    '''
    frequency = fields.Str(
        data_key='freq',
        default='ONETIME',
        validate=validate.OneOf(
            ['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
        ),
    )
    interval = fields.Int(default=1)
    byweekday = fields.List(
        fields.Str(validate=validate.OneOf(
            ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])
        )
    )
    bymonthday = fields.Int(
        validate=validate.OneOf(list(range(1, 32)))
    )

    @post_dump
    def post_serialization(self, data, **kwargs):
        if 'byweekday' in list(data.keys()):
            if data['byweekday']:
                data['byweekday'] = ','.join(data['byweekday'])

        return data


class ScheduleSchema(Schema):
    '''
    Schema for schedule field for AgentExclusionSchema class 
    '''
    enabled = fields.Boolean(default=True)
    starttime = fields.DateTime(
        format='%Y-%m-%dT%H:%M:%SZ',
        required=True
    )
    endtime = fields.DateTime(
        format='%Y-%m-%dT%H:%M:%SZ',
        required=True
    )
    timezone = fields.Str(default='Etc/UTC')
    rrules = fields.Nested(RulesSchema, required=True)

    @pre_load
    def pre_serialization(self, data, **kwargs):
        if not data['enabled']:
            data['starttime'] = (
                datetime.utcnow()
            ).strftime('%Y-%m-%dT%H:%M:%SZ')

            data['endtime'] = (
                datetime.utcnow() + timedelta(hours=1)
            ).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        if data['timezone'] not in self.context['valid_timezone']:
            raise ValidationError('Invalid Timezone Field.')

        return data


class AgentExclusionSchema(Schema):
    '''
    Schema for Agent Exclusion API
    '''
    name = fields.Str(required=True)
    description = fields.Str(default='')
    schedule = fields.Nested(
        ScheduleSchema,
        required=True
    )
