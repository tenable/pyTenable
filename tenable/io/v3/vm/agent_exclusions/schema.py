'''
Agent Exclusion API Endpoint Schemas
'''
from datetime import datetime, timedelta

from marshmallow import Schema, fields, post_dump, validate
from marshmallow.exceptions import ValidationError


class RulesSchema(Schema):
    frequency = fields.Str(
        data_key='freq',
        default='ONETIME',
        validate=validate.OneOf(
            ['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
        ),
    )
    interval = fields.Int(data_key='interval', default=1)
    weekdays = fields.List(
        fields.Str(validate=validate.OneOf(
            ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])
        ),
        data_key='byweekday',
    )
    day_of_month = fields.Int(
        data_key='bymonthday',
        validate=validate.OneOf(list(range(1, 32)))
    )

    @post_dump
    def post_serialization(self, data, **kwargs):
        if 'byweekday' in list(data.keys()):
            if data['byweekday']:
                data['byweekday'] = ','.join(data['byweekday'])

        return data


class ScheduleSchema(Schema):
    enabled = fields.Boolean(data_key='enabled', default=True)
    start_time = fields.DateTime(
        data_key='starttime',
        format='%Y-%m-%dT%H:%M:%SZ',
        required=True
    )
    end_time = fields.DateTime(
        data_key='endtime',
        format='%Y-%m-%dT%H:%M:%SZ',
        required=True
    )
    timezone = fields.Str(
        default='Etc/UTC',
        data_key='timezone'
    )
    rrules = fields.Nested(RulesSchema, data_key='rrules', required=True)

    @post_dump
    def post_serialization(self, data, **kwargs):
        if not data['enabled']:
            data['starttime'] = (
                datetime.utcnow()
            ).strftime('%Y-%m-%dT%H:%M:%SZ')

        if not data['enabled']:
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
    name = fields.Str(data_key='name', required=True)
    description = fields.Str(data_key='description', default='')
    schedule = fields.Nested(
        ScheduleSchema,
        data_key='schedule',
        required=True
    )
