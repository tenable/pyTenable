from tenable.base.schemas.filters import BaseFilterRuleSchema
from .filter_dict import filters
from marshmallow import (
    Schema,
    fields,
    pre_load,
    post_load,
    validate as v,
    validates_schema,
    ValidationError,
)


class PaginationFilterSchema(BaseFilterRuleSchema):
    '''
    The Tenable.ot Pagination Filter schema.

    This schema will output the data in a format typically seen from the
    Tenable.ot REST API.  It's serialized in the following format:

    .. code-block:: javascript

        {
            "filters"; {
                "FILTER_NAME": {"FILTER_OPERATOR": "FILTER_VALUE"}
            }
        }

    This format is then passed as part of a body request.
    '''
    value = fields.Raw()

    def load_filters(self, model):
        self.filters = filters[model]

    @post_load(pass_many=True)
    def reformat_many_filters(self, data, **kwargs):
        '''
        Performs the conversion of 1 or many filter rules.
        '''
        rules = dict()

        # if only a single filter was passed, then wrap it in a list as we will
        # be using the index of the list.
        if not kwargs.get('many'):
            data = [data]

        # process each rule and then merge the results into the rules dict.
        for idx, rule in enumerate(data):
            # if a name parameter exists, then we will use the filter name
            # specified within the the filter specification.  If none exists,
            # then we will simply use the name we have on hand.
            rules[self.filters[rule['name']].get('name', rule['name'])] = {
                rule['oper']: rule['value']
            }

        # return the rules dict back to the caller.
        return rules


class PaginationOrderSchema(Schema):
    field = fields.String()
    direction = fields.String(validate=v.OneOf(['ASC', 'DESC']))

    @pre_load
    def upcase_direction(self, data, **kwargs):
        if isinstance(data.get('direction'), str):
            # We want to ensure that the sort direction is uppercased.
            data['direction'] = data.get('direction').upper()
        return data


class PaginationSchema(Schema):
    filters = fields.Dict()
    orderBy = fields.Nested(PaginationOrderSchema)
    offset = fields.Integer()
    limit = fields.Integer()
    search = fields.String()

    @pre_load
    def process_filters(self, data, **kwargs):
        model = data.pop('model', None)
        if data.get('order_by'):
            data['orderBy'] = data.pop('order_by')
        if data.get('filters'):
            filters = PaginationFilterSchema()
            if model:
                filters.load_filters(model)
            f = filters.load(data.get('filters'), many=True)
            data['filters'] = f
        return data