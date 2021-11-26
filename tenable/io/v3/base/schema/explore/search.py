'''
Base Explore Search Schema
'''
from marshmallow import Schema
from marshmallow import fields as marshm_fields
from marshmallow import validate as v

from .filters import FilterSchema


class SortSchema(Schema):
    '''
    Schema for the sorting sub-object
    '''
    property = marshm_fields.Str()
    order = marshm_fields.Str(validates=v.OneOf(['asc', 'desc']))


class SearchSchema(Schema):
    '''
    Schema supporting the search request
    '''
    fields = marshm_fields.List(marshm_fields.Str())
    filter = marshm_fields.Nested(FilterSchema)
    limit = marshm_fields.Int()
    next = marshm_fields.Int()
    sort = marshm_fields.List(marshm_fields.Nested(SortSchema))
