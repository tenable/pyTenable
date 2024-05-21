from typing import Optional, Dict, List
from marshmallow import Schema, ValidationError
import re


class BaseFilterSchema(Schema):
    '''
    Base filter schema for the Tenable Vulnerability Management package.  As different APIs use
    different filter formats, we start with this common base schema that has
    the scaffolding needed to interact with the different API endpoints.
    '''
    _filters = None

    @classmethod
    def populate_filters(cls,
                         tio,
                         path: str,
                         envelope: str = 'filters',
                         force: bool = False,
                         filters: Optional[List[Dict]] = None
                         ) -> None:
        '''
        Populates the filters to be used for validation of the filter data.

        Args:
            tio:
                The TenableIO object to use to query the filter API
            path:
                The URL path to query to get the filter validation set.
            envelope:
                The envelope name to use to unpack the filters.  The default is
                `filters`.
            force:
                Should we force a reload of the filters, regardless of if we
                already have a filter-set loaded?  The default is `False`.
            filters:
                The filter-set to use instead of calling the api.
        '''
        # we only want to run the filter population if we need to, or if we
        # were told to forcibly do so.
        if not cls._filters or force:
            # if no filters were passed as part of calling the method, we will
            # then call the API using the TenableIO object provided and pull
            # down the filters.
            if not filters:
                filters = tio.get(path)[envelope]

            # Reset the _filters dictionary to an empty dict object.
            cls._filters = {}

            # Now we will iterate through all of the filters in the filters
            # definitions and reformat them in a way thats easier to reference
            # for our own purposes.  We will be using the following format:
            #
            # {
            #    'FILTER_NAME': {
            #        'pattern': 'REGEX PATTERN' or None,
            #        'operators': ['OPERATOR', 'OPERATOR', 'OPERATOR'],
            #        'choices': ['LIST', 'OF', 'VALID', 'VALUES'] or None
            #    }
            # }
            for filter in filters:
                control = filter.get('control', {})
                name = filter.get('name')
                item = {
                    'pattern': control.get('regex'),
                    'operators': filter.get('operators'),
                    'choices': None,
                }

                clist = control.get('list')
                if clist:
                    if isinstance(clist[0], dict):
                        key = 'value' if 'value' in clist[0] else 'id'
                        item['choices'] = [str(i[key]) for i in clist]
                    elif isinstance(clist, list):
                        item['choices'] = [str(i) for i in clist]
                cls._filters[name] = item

    def validate_filter(self, name, operator, value):
        '''
        Validate the information presented against the stored filter validation
        set within the class.  If any failures were noted, we will then raise a
        ValidationError at the end.
        '''
        errors = {}

        def pattern_check(val, ptn, key='value'):
            '''
            Checks to see if the value matches the regex pattern provided
            (assuming a pattern exists).  If a failure occurs, then add the
            error message to the error list under the appropriate key.
            '''
            if ptn and not re.match(ptn, val):
                errors[key] = errors.get(key, [])
                errors[key].append(f'"{val}" does not match pattern {ptn}')

        def choice_check(val, choices, key='value'):
            '''
            Checks to see if the value is a valid choice (if a list of choices
            exists).  If a failure occurs, then add the error message to the
            appropriate key
            '''
            if choices and val not in choices:
                errors[key] = errors.get(key, [])
                errors[key].append(f'"{val}" must be one of {choices}')

        if self._filters:
            vfilter = self._filters.get(name)
            if vfilter:
                choice_check(operator, vfilter['operators'], 'operator')
                if isinstance(value, str):
                    choice_check(value, vfilter['choices'])
                    pattern_check(value, vfilter['pattern'])
                elif isinstance(value, list):
                    for item in value:
                        choice_check(item, vfilter['choices'])
                        pattern_check(item, vfilter['pattern'])
            else:
                errors['name'] = [f'"{name}" is not a valid filter']
        if errors:
            raise ValidationError(errors)
