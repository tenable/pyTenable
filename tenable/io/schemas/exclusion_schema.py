from datetime import datetime
from marshmallow import fields, validate as v, pre_load, Schema, post_load
from restfly.utils import dict_clean


def check_value(data: dict, key: str, instance: type) -> bool:
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


class ExclusionRRulesSchema(Schema):
    '''
    Exclusion rrules dictionary schema
    '''
    freq = fields.Str(
        load_default='ONETIME',
        validate=v.OneOf(['ONETIME', 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']))
    interval = fields.Int(load_default=1)
    byweekday = fields.List(
        fields.Str(validate=v.OneOf(['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])),
        load_default=['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'])
    bymonthday = fields.Int(
        load_default=datetime.today().day,
        validate=v.OneOf(list(range(1, 32))))

    @pre_load()
    def transform(self, data: dict, **kwargs) -> dict:
        '''
        transforms values to required case or type
        '''
        # transform frequency to uppercase
        if check_value(data, 'freq', str):
            data['freq'] = data.get('freq').upper()

        # transform weekdays to uppercase
        if check_value(data, 'byweekday', list):
            data['byweekday'] = list(map(str.upper, data.get('byweekday')))
        elif check_value(data, 'byweekday', str):
            data['byweekday'] = data.get('byweekday').split(',')

        return data

    @post_load()
    def combine(self, data: dict, **kwargs) -> dict:
        """
        convert values in list to single string
        """
        # join list of weekdays and members to single string
        keys = ['byweekday']
        for key in keys:
            if check_value(data, key, list):
                data[key] = ','.join(data[key])
        return data


class ExclusionScheduleSchema(Schema):
    '''
    Exclusion schedule dictionary schema
    '''
    enabled = fields.Bool(load_default=True)
    starttime = fields.DateTime()
    endtime = fields.DateTime()
    timezone = fields.Str(load_default='Etc/UTC')
    rrules = fields.Nested(
        ExclusionRRulesSchema(),
        load_default=ExclusionRRulesSchema().load({}))

    @pre_load()
    def transform(self, data: dict, **kwargs) -> dict:
        '''
        transform datetime value to string for fields.DateTime
        '''
        # transform start_time datetime object to string
        if check_value(data, 'starttime', datetime):
            data['starttime'] = str(data.get('starttime'))

        # transform end_time datetime object to string
        if check_value(data, 'endtime', datetime):
            data['endtime'] = str(data.get('endtime'))

        return data

    @post_load()
    def convert(self, data: dict, **kwargs) -> dict:
        '''
        convert datetime values API required format
        '''
        # transform start_time datetime object to string
        if check_value(data, 'starttime', datetime):
            data['starttime'] = data.get('starttime').strftime('%Y-%m-%d %H:%M:%S')

        # transform end_time datetime object to string
        if check_value(data, 'endtime', datetime):
            data['endtime'] = data.get('endtime').strftime('%Y-%m-%d %H:%M:%S')

        return data


class ExclusionSchema(Schema):
    '''
    Exclusion payload dictionary schema
    '''
    name = fields.Str(required=True)
    members = fields.List(
        fields.Str(),
        validate=v.Length(min=1))
    description = fields.Str(load_default='')
    network_id = fields.Str(
        load_default='00000000-0000-0000-0000-000000000000',
        validate=v.Regexp(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'))
    schedule = fields.Nested(ExclusionScheduleSchema())

    @pre_load()
    def clean(self, data: dict, **kwargs) -> dict:
        '''
        remove None keys from data
        '''
        data = dict_clean(data)

        # we need to convert string members to list as required by schema
        # this is used for edit method
        if check_value(data, 'members', str):
            data['members'] = data.get('members').split(',')

        return data

    @post_load()
    def combine(self, data: dict, **kwargs) -> dict:
        '''
        combine members value to single string for API call
        '''
        # join list of weekdays and members to single string
        keys = ['members']
        for key in keys:
            if check_value(data, key, list):
                data[key] = ','.join(data[key])
        return data
