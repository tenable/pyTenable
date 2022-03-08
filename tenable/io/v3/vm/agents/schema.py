'''
Agents API Endpoint Schemas
'''
from marshmallow import Schema, fields, validate

from tenable.io.v3.base.schema.explore.filters import ParseFilterSchema


class CriteriaSchema(Schema):
    '''
    Supportive Schema for AgentSchema
    '''
    all_agents = fields.Bool()
    wildcard = fields.Str()
    filters = fields.List(fields.Str())
    filter_type = fields.Str(
        validate=validate.OneOf(['and', 'or'])
    )
    hardcoded_filters = fields.List(fields.Str())


class DirectiveSchema(Schema):
    '''
    Supportive schema for AgentSchema
    '''
    type = fields.Str(
        validate=validate.OneOf(['restart', 'settings']),
        required=True
    )
    option = fields.Dict()


class AgentFilterSchema(ParseFilterSchema):
    '''
    Validate filters using ParseFilterSchema
    '''
    _filters = None


class AgentSchema(Schema):
    '''
    Schema for agents API endpoint
    '''
    filters = fields.List(fields.Nested(AgentFilterSchema))
    wildcard = fields.Str()
    filter_type = fields.Str(
        validate=validate.OneOf(['and', 'or'])
    )
    wildcard_fields = fields.List(fields.Str())
    sort = fields.List(
        fields.Tuple(
            (
                fields.Str(),
                fields.Str(validate=validate.OneOf(['asc', 'desc']))
            )
        )
    )
    limit = fields.Int()
    offset = fields.Int()
    agent_ids = fields.List(fields.UUID(), data_key='items')
    not_items = fields.List(fields.UUID())
    criteria = fields.Nested(CriteriaSchema)
    directive = fields.Nested(DirectiveSchema)
