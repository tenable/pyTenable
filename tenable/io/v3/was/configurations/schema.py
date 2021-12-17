'''
Configurations API Endpoint Schemas
'''
from re import compile

from marshmallow import INCLUDE, Schema, fields, post_dump
from marshmallow import validate as v


class PermissionConfigurationSchema(Schema):
    '''
    Schema for validating permissions body parameter
    while creating a scan configuration.
    '''
    entity = fields.String(validate=v.OneOf(['user', 'group']))
    entity_id = fields.UUID()
    level = fields.String(validate=v.OneOf(['no_access',
                                            'view',
                                            'control',
                                            'configure']))
    permissions_id = fields.UUID()


class ScheduleSchema(Schema):
    '''
    Schema for validating schedule body parameter
    while creating or updating a scan configuration
    '''
    rrule = fields.String(required=True)
    enabled = fields.Boolean()
    starttime = fields.DateTime(required=True, format='iso')
    timezone = fields.String()


class SettingsSchema(Schema):
    '''
    Schema for validating the settings body parameter
    while creating or updating a scan configuration
    '''
    class Meta:
        unknown = INCLUDE

    description = fields.String()
    timeout = fields.String(validate=v.Regexp(
                                    regex=compile(r'^\d{2}:[0-5]\d:[0-5]\d$'),
                                    error='Invalid scan duration format'
                                )
                            )
    debug_mode = fields.Boolean()
    input_force = fields.Boolean()
    credentials = fields.Dict(keys=fields.String(validate=v.Equal('credential_ids')),  # noqa: E501
                              values=fields.List(fields.UUID()))

    scope = fields.Dict()
    plugin = fields.Dict()
    browser = fields.Dict()
    http = fields.Dict()
    assessment = fields.Dict()

    @post_dump(pass_original=True)
    def keep_unknowns(self, output, orig, **kw):
        for key in orig:
            if key not in output:
                output[key] = orig[key]
        return output


class ConfigurationSchema(Schema):
    '''
    Base Schema for Configurations API
    '''
    targets = fields.List(fields.Url())
    owner_id = fields.UUID()
    template_id = fields.UUID()
    settings = fields.Nested(SettingsSchema)
    schedule = fields.Nested(ScheduleSchema)
    notifications = fields.Dict(keys=fields.String(validate=v.Equal('emails')),
                                values=fields.List(fields.Email()))
    permissions = fields.List(fields.Nested(PermissionConfigurationSchema))
    folder_name = fields.String()
    folder_id = fields.UUID()
    user_template_id = fields.UUID()
    scanner_id = fields.UUID()
    name = fields.String()
