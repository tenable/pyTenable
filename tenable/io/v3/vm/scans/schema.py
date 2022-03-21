'''
Schema for scans
'''
from datetime import datetime, timedelta

from marshmallow import Schema, ValidationError, fields, post_dump, pre_load
from marshmallow import validate as v
from marshmallow import validates

from tenable.constants import IOConstants

# todo => history iterator schema => pending


class ScanSchema(Schema):
    '''
    Common class for all schema
    '''

    key = fields.Str()
    name = fields.Str()
    folder_id = fields.Str()
    history_id = fields.Str()
    password = fields.Str()
    aggregate = fields.Bool()
    alt_targets = fields.List(fields.Str())
    read_status = fields.Bool()
    enabled = fields.Bool()
    limit = fields.Int()
    matched_resource_limit = fields.Int()


class ScanCheckAutoTargetSchema(Schema):
    '''
    Schema for check auto targets method
    '''
    network_id = fields.UUID(
        dump_default='00000000-0000-0000-0000-000000000000'
    )
    tags = fields.List(fields.UUID())
    target_list = fields.List(fields.Str())

    @post_dump
    def transform_data(self, data, **kwargs):
        if 'target_list' in data:
            target_list = data.pop('target_list')
            target_list = ','.join(target_list)
            data['target_list'] = target_list
        return data


class ScanDocumentCreateSchema(Schema):
    '''
    Schema for create scan document method
    '''
    name = fields.Str()
    template = fields.Str()
    scanner = fields.Str()
    targets = fields.List(fields.Str())
    file_targets = fields.Str()
    credentials = fields.Dict()
    compliance = fields.Dict()
    plugins = fields.Dict()
    schedule_scan = fields.Dict()

    @validates('template')
    def validate_template(self, value):
        if self.context.get('templates_choices'):
            if value not in self.context['templates_choices']:
                raise ValueError('Template does not matches with choices')

    @validates('scanner')
    def validate_scanner(self, value):
        if self.context.get('scanners_choices'):
            if value not in self.context['scanners_choices']:
                raise ValueError('Scanner does not matches with choices')

    @post_dump
    def transform_data(self, data, **kwargs):
        if 'targets' in data:
            target_list = data.pop('targets')
            target_list = ','.join(target_list)
            data['targets'] = target_list
        return data


class ScanConfigureScheduleSchema(Schema):
    '''
    Schema for configure schedule method
    '''
    schedule_const = IOConstants.ScanScheduleConst
    frequency = fields.Str(validate=v.OneOf(schedule_const.frequency_choice))
    interval = fields.Int()
    weekdays = fields.List(fields.Str(
        validate=v.OneOf(schedule_const.weekdays_default)
    ))
    day_of_month = fields.Int(validate=v.OneOf(
        schedule_const.day_of_month_choice
    ))
    starttime = fields.DateTime(format='iso')
    timezone = fields.Str()

    def validate_freq(self, value):
        if value is None:
            value = self.context['existing_rules'].get(
                self.schedule_const.frequency,
                self.schedule_const.frequency_default
            )
        return value.upper()

    def validate_interval(self, value):
        if value is None:
            value = self.context['existing_rules'].get(
                self.schedule_const.interval,
                self.schedule_const.interval_default
            )
        return value

    def validate_weekdays(self, value):
        if value is None:
            return self.context['existing_rules'].get(
                self.schedule_const.weekdays,
                self.schedule_const.weekdays_default
            )
        else:
            return [val.upper() for val in value]

    def validate_dayofmonth(self, value):
        if value is None:
            value = self.context['existing_rules'].get(
                self.schedule_const.day_of_month,
                self.schedule_const.day_of_month_default
            )
        return value

    def validate_starttime(self, value):
        if value is None:
            value = self.context['existing_rules'].get(
                self.schedule_const.start_time,
                self.schedule_const.start_time_default
            )
        return self.update_starttime_structure(value)

    def update_starttime_structure(self, value):
        secs = timedelta(minutes=30).total_seconds()
        value = datetime.fromtimestamp(
            value.timestamp() + secs - value.timestamp() % secs)
        return value.strftime('%Y-%m-%dT%H:%M:%SZ')

    def validate_timezone(self, value):
        if value is None:
            return self.context['existing_rules'].get(
                self.schedule_const.timezone,
                self.schedule_const.timezone_default
            )
        elif value in self.context['timezone_choices']:
            return value
        else:
            raise ValueError('Timezone does not matches with choices')

    @pre_load
    def pre_process_data(self, data, **kwargs):
        data['frequency'] = self.validate_freq(data.pop('frequency'))
        data['interval'] = self.validate_interval(data.pop('interval'))
        data['weekdays'] = self.validate_weekdays(data.pop('weekdays'))
        data['day_of_month'] = self.validate_dayofmonth(
            data.pop('day_of_month')
        )
        data['starttime'] = self.validate_starttime(data.pop('starttime'))
        data['timezone'] = self.validate_timezone(data.pop('timezone'))
        return data

    @post_dump
    def transform_data(self, data, **kwargs):
        if 'weekdays' in data:
            weekdays = data.pop('weekdays')
            weekdays = ','.join(weekdays)
            data['weekdays'] = weekdays
        return data


class ScanExportSchema(Schema):
    '''
    Schema for export method
    '''
    history_id = fields.Str()
    scan_type = fields.Str(validate=v.OneOf(['web-app']))
    password = fields.Str()
    filter_type = fields.Str(validate=v.OneOf(['and', 'or']))
    format = fields.Str(
        dump_default='nessus',
        validate=v.OneOf(['nessus', 'html', 'pdf', 'csv', 'db'])
    )
    chapters = fields.List(
        fields.Str(
            validate=v.OneOf([
                'vuln_hosts_summary',
                'vuln_by_host',
                'vuln_by_plugin',
                'compliance_exec',
                'compliance',
                'remediations',
            ])
        ),
        dump_default=['vuln_by_host']
    )

    @post_dump
    def transform_data(self, data, **kwargs):
        if 'chapters' in data:
            chapters_list = data.pop('chapters')
            chapters_list = ','.join(chapters_list)
            data['chapters'] = chapters_list
        return data


class ScanConvertCredPermission(Schema):
    '''
    Schema for credentials permissions in scans
    '''

    type = fields.Str(validate=v.OneOf(['user', 'group']))
    permissions = fields.Int(validate=v.OneOf([32, 64]))
    grantee_id = fields.UUID()

    @pre_load
    def validate_and_transform(self, data, **kwargs):
        '''
        Handles schema validation and data transform based on the data
        presented.
        '''

        if isinstance(data, dict) and len(data) == 3 and \
                ('type' and 'permissions' and 'grantee_id' in data.keys()):
            return data
        elif isinstance(data, tuple) and len(data) == 3:
            return self.permissions_tuple_expansion(data)
        else:
            return ValidationError('Invalid Permissions definition')

    def permissions_tuple_expansion(self, data: tuple) -> dict:
        '''
        Handles expanding a tuple definition of a filter into the dictionary
        equivalent.

        Example:

            >>> f = ('user', 64, '00000000-0000-0000-0000-000000000000')
            >>> filter.dump(filter.load(f))
            {'type': 'filter', 'permissions': 64, 'grantee_id':
            'value'}
        '''
        permission_val = data[1]
        if isinstance(permission_val, str):
            if permission_val == 'use':
                permission_val = 32
            elif permission_val == 'edit':
                permission_val = 64

        return {
            'type': data[0], 'permissions': permission_val,
            'grantee_id': data[2]
        }


class ScanConvertCredSchema(Schema):
    '''
    Schema for convert_credentials function in scans
    '''

    name = fields.Str()
    type = fields.Str()
    ad_hoc = fields.Bool()
    settings = fields.Dict()
    category = fields.Str()
    permissions = fields.List(fields.Nested(ScanConvertCredPermission))
