from marshmallow import (
    Schema,
    fields,
    pre_load,
    validate as v,
    validates_schema,
    ValidationError,
)
from copy import copy


class BaseFilterRuleSchema(Schema):
    '''
    The basic filter rule validator and processor.

    Because in many cases we will be using the filter definitions passed from
    the filters API endpoints, we need a common way to process and validate that
    the filters that are being passed are indeed valid filters before converting
    them into the appropriate format for the specified endpoint.  This base
    schema lacks the output formatting necessary for use within the endpoints
    themselves and instead serves as starting point for subclassing.

    Attributes:
        filters (dict):
            The filter ruleset (to be loaded by load_filters)
        filter_check (bool):
            The flag determining if we should be checking against the filter
            ruleset.  There are cases where we simply want to pass the data
            through into the desired format, and not validate the content aside
            from basic formatting.
        name (str):
            The name of the filter.
        oper (str):
            The filter operator.
        value (str):
            The filter value.

    Examples:
        Performing a validation with a given filter definition ruleset:

        >>> schema = BaseFilterRuleSchema()
        >>> schema.load_filters(filterset)
        >>> schema.load(('port.port', 'eq', '137'))

        Performing a validation without a ruleset:

        >>> schema = BaseFilterRuleSchema()
        >>> schema.load(('port.port', 'eq', '137'))

        Performing a validation against multiple filters at the same time:

        >>> schema = BaseFilterRuleSchema()
        >>> schema.load_filters(filterset)
        >>> s.load((
        ...     ('port.port', 'eq', '137'),
        ...     ('port.port', 'eq', '443')),
        ...     many=True
        ... )
    '''
    filters = False
    name = fields.String()
    oper = fields.String()
    value = fields.String()

    def load_filters(self, f):
        '''
        Handles loading the filter dictionary and setting the filter_check
        flag to true.
        '''
        self.filters = f

    @pre_load
    def serialize_tuple(self, rule, **kwargs):
        '''
        Handles serializing the standardized tuple format into a dictionary that
        can then be validated and processed.
        '''
        if isinstance(rule, tuple):
            rule = {
                'name': rule[0],
                'oper': rule[1],
                'value': rule[2]
            }
        return self.convert_input(rule)

    def convert_input(self, rule):
        '''
        Handles any additional conversion if necessary.
        '''
        return rule

    def get_filter(self, value):
        '''
        Retrieves a filter definition ruleset from the stored definitions and
        then returns a copy with the appropriate validators.
        '''
        # We don't want to modify the original filter data, so we will be
        # performing a shallow copy instead of the default ref assignment.
        if self.filters:
            f = copy(self.filters.get(value, dict()))

            # If no filter was returned and filter checking was enabled, then we
            # should throw an error informing the caller that the filter wasn't
            # a supported filter.
            if f == dict():
                raise ValidationError('not a supported filter')

            # Convert the pattern, choices, and operators into the expected
            # validators, overloading the original data.
            if f.get('pattern'):
                f['pattern'] = v.Regexp(f['pattern'])
            if f.get('choices'):
                f['choices'] = v.OneOf(f['choices'])
            if f.get('operators'):
                f['operators'] = v.OneOf(f['operators'])

            # Return the modified filter to the caller.
            return f
        return dict()

    @validates_schema
    def validate_against_filter(self, item, **kwargs):
        '''
        Performs the necessary validations against the filter item.
        '''
        f = self.get_filter(item['name'])
        if f.get('operators'):
            f['operators'](item['oper'])
        if f.get('pattern'):
            f['pattern'](item['value'])
        if f.get('choices'):
            f['choices'](item['value'])
