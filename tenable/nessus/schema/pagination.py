'''
Base schemas for pagination
'''
from typing import Dict
from marshmallow import Schema, fields, post_dump, pre_load, validate as v
from restfly.utils import dict_clean
from tenable.base.schema.fields import LowerCase


class FilterSchema(Schema):
    '''
    Base filter schema
    '''
    filter = fields.Str(required=True)
    quality = LowerCase(fields.Str(required=True, validate=v.OneOf(['eq',
                                                                    'neq',
                                                                    'match',
                                                                    'nmatch',
                                                                    'date-eq',
                                                                    'date-lt',
                                                                    'date-gt'
                                                                    ])))
    value = fields.Str(required=True)

    @pre_load(pass_many=False)
    def tuple_expansion(self, data, **kwargs) -> Dict:  # noqa PLW0613 PLR0201
        '''
        Handles expanding a tuple definition into the dictionary equivalent.
        '''
        if isinstance(data, tuple):
            return {
                'filter': data[0],
                'quality': data[1],
                'value': data[2]
            }
        return data


class FilterListSchema(Schema):
    '''
    List of filters schema
    '''
    search_type = LowerCase(fields.Str(validate=v.OneOf(['and', 'or'])),
                            load_default=None
                            )
    filters = fields.List(fields.Nested(FilterSchema), allow_none=True)

    @post_dump
    def reformat_filters(self, data, **kwargs) -> Dict:  # noqa PLW0613 PLR0201
        '''
        Reformats the response to match what the API expects to see
        '''
        filters = data.pop('filters', None)
        if data.get('search_type'):
            data['filter.search_type'] = data.pop('search_type')
        if filters:
            for f in filters:  # noqa PLC0103
                idx = filters.index(f)
                data[f'filter.{idx}.filter'] = f['filter']
                data[f'filter.{idx}.quality'] = f['quality']
                data[f'filter.{idx}.value'] = f['value']
        return dict_clean(data)


class ListSchema(FilterListSchema):
    '''
    Base List schema
    '''
    limit = fields.Int()
    offset = fields.Int()
    sort_by = fields.Str(load_default=None)
    sort_order = LowerCase(fields.Str(validate=v.OneOf(['asc', 'desc'])),
                           load_default=None
                           )
