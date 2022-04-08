'''
Agent Config API Endpoint Schema
'''
from marshmallow import Schema, fields, pre_load, validate


class AutoLinkSchema(Schema):
    '''
    Supporting schema for AgentConfigSchema
    '''
    enabled = fields.Bool()
    expiration = fields.Int(
        validate=validate.OneOf([False] + list(range(1, 366)))
    )

    @pre_load
    def pre_serialization(self, data, **kwarg):
        if 0 < data['expiration'] < 366:
            data['enabled'] = True
        elif data['expiration'] in [False, 0]:
            data['enabled'] = False
            data.pop('expiration', '')

        return data


class AgentsConfigSchema(Schema):
    '''
    Schema for Agent Config API
    '''
    software_update = fields.Bool()
    auto_unlink = fields.Nested(AutoLinkSchema)
