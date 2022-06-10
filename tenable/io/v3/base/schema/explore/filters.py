'''
Base explore filter schema for V3 endpoints
'''
from typing import Dict, Tuple, Union

from marshmallow import Schema, ValidationError, fields
from marshmallow.decorators import pre_load


class FilterSchemaV3(Schema):
    '''
    Schema supporting both the Filter and FilterGroups for V3 endpoints
    '''

    property = fields.Str()
    operator = fields.Str()
    value = fields.Raw()
    and_ = fields.List(fields.Nested('FilterSchemaV3'), data_key='and')
    or_ = fields.List(fields.Nested('FilterSchemaV3'), data_key='or')

    @pre_load(pass_many=False)
    def validate_and_transform(self, data, **kwargs):  # noqa: PLW0613
        '''
        Handles schema validation and data transform based on the data presented.
        '''
        if (  # noqa: PLR1705
                isinstance(data, dict) and ('and' in data or 'or' in data)
        ) or (isinstance(data, tuple) and data[0] in ['and', 'or']):
            # We need to check to see if the data dictionary
            # is a group of filters. To do so we will check to see
            # if the following conditions are met:
            #
            # 1. The data obj is a dictionary and has either an 'and' key
            #    or an 'or' key.
            # 2. The data obj is a tuple and the first element is a string
            #    with a value of 'and' or 'or'
            #
            # If either condition is met, then we will pass the data obj
            # to the filter_group_transform method for validation
            # and transformation
            return self.filter_group_transform(data)
        elif (
                isinstance(data, dict)
                and (
                        'property' in data  # noqa: PLR0916
                        and 'operator' in data
                        and 'value' in data
                )
        ) or (isinstance(data, tuple) and len(data) == 3):
            return self.filter_tuple_expansion(data)
        else:
            raise ValidationError('Invalid Filter definition')

    def filter_group_transform(
            self, data: Union[Tuple, Dict]) -> Dict:  # noqa: PLR0201
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
        if isinstance(data, tuple):
            # if the data object is a tuple, then we will need to pass it to
            # the tuple -> dict transformer.
            return self.filter_group_tuple_expansion(data)
        else:
            # pass the data object right through if it's not a tuple and rely
            # on the schema to validate the data object.
            return data

    def filter_group_tuple_expansion(self, data: Tuple) -> Dict:
        '''
        Transforms a logical group tuple into a logical group dictionary.

        '''
        resp = {}
        oper = None
        errors = {}
        for element in data:
            # If the element is either 'and' or 'or' and doesn't already exist
            # within the response dict, then we will store the operator and
            # create the list within the response to store this logical
            # grouping.
            if (
                    isinstance(element, str)
                    and element in ['and', 'or']
                    and not resp.get(element)
            ):
                resp[element] = []
                oper = element
            # if the element is a logical condition that we have already seen
            # before, we should assume that this is a malformed tuple and log
            # the error into the errors dict.
            elif (
                    isinstance(element, str)
                    and element in ['and', 'or']
                    and resp.get(element)
            ):
                errors[element] = [
                    (
                        f'attempted to use logical condition {element}\
                        multiple times'
                    )
                ]
            # If there is no stored operator, when we will log a 'NoneOper'
            # validation error.
            elif oper is None:
                errors['NoneOper'] = ['No valid logical condition detected']
            # If none of the above conditions have been met, then we can safely
            # assume that the element is a filter and we should append it to
            # the current logical grouping.
            else:
                resp[oper].append(element)
        if errors:
            raise ValidationError(errors)
        return resp

    def filter_tuple_expansion(self, data) -> Dict:  # noqa: PLR0201
        '''
        Handles expanding a tuple definition of a filter into the dictionary
        equivalent.

        Example:

            >>> f = ('filter', 'oper', 'value')
            >>> filter.dump(filter.load(f))
            {'property': 'filter', 'operator': 'oper', 'value': 'value'}
        '''
        if isinstance(data, tuple):
            return {'property': data[0], 'operator': data[1], 'value': data[2]}
        return data
