'''
Base Explore Search Schema
'''
from marshmallow import Schema, fields, post_dump, pre_load
from marshmallow import validate as v

from tenable.io.v3.base.schema.explore.filters import FilterSchema


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
        if not self.context['is_sort_with_prop']:
            return {
                data['property']: data['order']
            }
        return data


class SearchSchema(Schema):
    '''
    Schema supporting the search request
    '''
    fields_ = fields.List(fields.Str(), allow_none=True, data_key='fields')
    filter = fields.Nested(FilterSchema, allow_none=True)
    limit = fields.Int(default=1000)
    next = fields.Str(allow_none=True)
    sort = fields.List(fields.Nested(SortSchema), allow_none=True)
