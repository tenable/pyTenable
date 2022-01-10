'''
Base Explore Export Schema
'''
from marshmallow import Schema, fields


class ExportSchema(Schema):
    '''
    Schema supporting an export
    '''
    source = fields.Str(required=True)
    format = fields.Str(required=True)
    definition = fields.Dict()
    name = fields.Str()


class ExportScheduleSchema(ExportSchema):
    '''
    Schema supporting a scheduled export
    '''
    schedule = fields.Str()
