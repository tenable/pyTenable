'''
Base Universal Workspace Filter Schema
'''
from marshmallow import Schema, ValidationError, fields, pre_load


class FilterSchema(Schema):
    '''
    Schema supporting both the Filter and FilterGroups
    '''
    property = fields.Str()
    operator = fields.Str()
    value = fields.Raw()
    and_ = fields.List(fields.Nested('FilterSchema'), data_key='and')
    or_ = fields.List(fields.Nested('FilterSchema'), data_key='or')

    @pre_load(pass_many=False)
    def validate_and_transform(self, data, **kwargs):  # noqa: PLW0613
        '''
        Handles schema validation and data transform based on the data
        presented.
        '''
        if (  # noqa: PLR1705
            (isinstance(data, dict) and ('and' in data or 'or' in data))
            or (isinstance(data, tuple) and data[0] in ['and', 'or'])
        ):
            return self.filter_group_tuple_expansion(data)
        elif (
            (isinstance(data, dict) and ('property' in data  # noqa: PLR0916
                                         and 'operator' in data
                                         and 'value' in data))
            or (isinstance(data, tuple) and len(data) == 3)
        ):
            return self.filter_tuple_expansion(data)
        else:
            raise ValidationError('Invalid Filter definition')

    def filter_group_tuple_expansion(self, data):  # noqa: PLR0201
        '''
        Handles expanding a tuple definition of a filter group into the
        dictionary equivalent.

        Example:

            >>> f = ('or', ('and', ('test', 'oper', '1'),
            ...                    ('test', 'oper', '2')
            ...             ),
            ...      'and', ('test', 'oper', 3)
            ...     )
            >>> filter.dump(filter.load(f))
            {'or': [
                {'and': [
                    {'value': '1', 'operator': 'oper', 'property': '1'},
                    {'value': '2', 'operator': 'oper', 'property': '2'}
                    ]
                }],
             'and': [
                 {'value': '3', 'operator': 'oper', 'property': 3}
                 ]
             }
        '''
        resp = {}
        errors = {}
        if isinstance(data, tuple):
            oper = None
            for elem in data:
                if (
                    isinstance(elem, str)
                    and elem in ['and', 'or']
                    and not resp.get(elem)
                ):
                    resp[elem] = []
                    oper = elem
                elif (
                    isinstance(elem, str)
                    and elem in ['and', 'or']
                    and resp.get(elem)
                ):
                    errors[elem] = [('attempting to use logical condition'
                                     f'{elem} multiple times.'
                                     )]
                elif oper is None:
                    errors['NoneOper'] = [
                        'No valid logical condition detected'
                    ]
                else:
                    resp[oper].append(elem)
        else:
            resp = data
        if errors:
            raise ValidationError(errors)
        return resp

    def filter_tuple_expansion(self, data):  # noqa: PLR0201
        '''
        Handles expanding a tuple definition of a filter into the dictionary
        equivalent.

        Example:

            >>> f = ('filter', 'oper', 'value')
            >>> filter.dump(filter.load(f))
            {'property': 'filter', 'operator': 'oper', 'value': 'value'}
        '''
        if isinstance(data, tuple):
            return {
                'property': data[0],
                'operator': data[1],
                'value': data[2]
            }
        return data
