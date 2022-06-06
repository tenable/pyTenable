'''
Base Explore Search Schema
'''
from enum import Enum

from marshmallow import Schema, fields, post_dump, pre_load
from marshmallow import validate as v

from tenable.io.v3.base.schema.explore.filters import FilterSchema


class SortType(Enum):
    '''
    Enum class for different types of sort
    '''
    default = 'Sort format: {FIELD:ORDER}'
    property_based = 'Sort format: {"property": FIELD, "order": ORDER}'
    name_based = 'Sort format: {"name": FIELD, "order": ORDER}'


class SortSchema(Schema):
    '''
    Schema for the sorting sub-object
    '''
    property = fields.Str()
    order = fields.Str(validate=v.OneOf(['asc', 'desc']))

    @pre_load(pass_many=True)
    def transform_data(self, data, **kwargs):
        if isinstance(data, tuple) and len(data) == 2:
            property = data[0]
            order = data[1]
            return dict(property=property, order=order)
        return data

    @post_dump(pass_many=True)
    def transform_request_data(self, data, **kwargs):
        if (
            not self.context.get("sort_type")
            or self.context.get("sort_type") == SortType.default
        ):
            return {
                data['property']: data['order']
            }
        elif self.context.get('sort_type') == SortType.name_based:
            return {
                'name': data['property'],
                'order': data['order']
            }
        elif self.context.get('sort_type') == SortType.property_based:
            return data


class SearchSchema(Schema):
    '''
    Schema supporting the search request
    '''
    fields_ = fields.List(fields.Str(), allow_none=True, data_key='fields')
    filter = fields.Nested(FilterSchema, allow_none=True)
    limit = fields.Int(dump_default=200)
    next = fields.Str(allow_none=True)
    sort = fields.List(fields.Nested(SortSchema), allow_none=True)


class SearchWASSchema(Schema):
    '''
    Schema supporting the search request for was API
    '''
    fields_ = fields.List(fields.Str(), allow_none=True, data_key='fields')
    filter = fields.Nested(FilterSchema, allow_none=True)
    limit = fields.Int(dump_default=200)
    offset = fields.Int(dump_default=0)
    num_pages = fields.Int()
    sort = fields.List(fields.Nested(SortSchema), allow_none=True)
