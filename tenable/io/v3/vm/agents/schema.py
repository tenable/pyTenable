'''
Agents API Endpoint Schemas
'''
from marshmallow import Schema, fields


class AgentSchema(Schema):
    '''
    Schema for agents API
    '''
    items = fields.List(fields.UUID)
