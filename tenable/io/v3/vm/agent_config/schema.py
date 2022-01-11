'''
Agent Config API Endpoint Schema
'''
from marshmallow import Schema, fields, pre_load


class AutoLinkSchema(Schema):
    '''
    Supporting schema for AgentConfigSchema
    '''
    enabled = fields.Bool()
    expiration = fields.Int()

    @pre_load
    def pre_searilization(self, data, **kwarg):
        if 0 < data['expiration'] < 366:
            data['enabled'] = True
        elif data['expiration'] in [False, 0]:
            data['enabled'] = False
            data.pop('expiration', '')

        return data


class AgentConfigSchema(Schema):
    '''
    Schema for Agent Config API
    '''
    software_update = fields.Bool()
    auto_unlink = fields.Nested(AutoLinkSchema)
