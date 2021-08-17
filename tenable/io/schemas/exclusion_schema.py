from datetime import datetime
from marshmallow import fields, validate as v, pre_load, Schema, post_load


class ExclusionSchema(Schema):
    '''
    This class is for validation of inputs for exclusion endpoints
    '''
    name = fields.Str()
    members = fields.List(fields.Str())
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    timezone = fields.Str()
    description = fields.Str()
    frequency = fields.Str(validate=v.OneOf(['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']))
    interval = fields.Int()
    weekdays = fields.List(fields.Str(validate=v.OneOf(['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])))
    day_of_month = fields.Int(validate=v.OneOf(list(range(1, 32))))
    enabled = fields.Bool()
    network_id = fields.Str(
        validate=v.Regexp(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'))

    def check(self, data: dict, key: str, instance: type) -> bool:
        '''
        check if key is in data and isinstance of type

        Args:
            data (dict): Dictionary of items
            key (str): check presence of key in data
            instance (type): to check if value in key of data is instance of provided type

        Returns: `bool`
        '''
        if data.get(key) and isinstance(data.get(key), instance):
            return True
        return False

    @pre_load()
    def transform(self, data: dict, **kwargs) -> dict:
        '''
        transform values to required case/type
        '''
        # transform frequency to uppercase
        if self.check(data, 'frequency', str):
            data['frequency'] = data.get('frequency').upper()

        # transform weekdays to uppercase
        if self.check(data, 'weekdays', list):
            data['weekdays'] = list(map(str.upper, data.get('weekdays')))

        # transform start_time datetime object to string
        if self.check(data, 'start_time', datetime):
            data['start_time'] = str(data.get('start_time'))

        # transform end_time datetime object to string
        if self.check(data, 'end_time', datetime):
            data['end_time'] = str(data.get('end_time'))

        return data

    @post_load()
    def combine(self, data: dict, **kwargs) -> dict:
        # join list of weekdays and members to single string
        keys = ['weekdays', 'members']
        for key in keys:
            if self.check(data, key, list):
                data[key] = ','.join(data[key])
        return data


