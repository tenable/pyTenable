'''
Base Endpoint
=============

The APIEndpoint class is the base class that all endpoint modules will inherit
from.  Throughout pyTenable v1, packages will be transitioning to using this
base class over the original APISession class.

.. autoclass:: APIEndpoint
    :members:
    :inherited-members:
'''
from typing import Any, List, Optional
from restfly.utils import check
from restfly import APIEndpoint as Base


class APIEndpoint(Base):  # noqa PLR0903
    '''
    Base API Endpoint class
    '''

    def _check(self,  # noqa PLR0913
               name: str,
               obj: Any,
               expected_type: Any,
               choices: Optional[List] = None,
               default: Optional[Any] = None,
               case: Optional[str] = None,
               pattern: Optional[str] = None
               ) -> Any:
        '''
        Overload for RESTfly's check function to make it behave like the old
        _check method.

        Args:
            name (str):
                The display name of the attribute to be checked
            obj (Any):
                The object to check.
            expected_type (Any):
                The object type to check against
            choices (optional, list[Any]):
                A list of valid values that `obj` must be.
            default (optional, Any):
                The default value to return if the `obj` is `None`.
            case (optional, str):
                If the expected_type is `str`, should the resp be uppercased
                or lowercased?  Valid values are `upper` and `lower`.
            pattern (optional, str):
                A regex pattern to match the `obj` against if it is of a `str`
                type.

        Raises:
            TypeError:
                If the `obj` is not the expected_type, then raise a `TypeError`
            UnexpectedValueError:
                If the `obj` fails either the regex pattern or choices checks,
                then an UnexpectedValueError is raises.

        Returns:
            Any:
                Will return the object passed if all the checks succeed.  If a
                default parameter was set and the object was a NoneType, then
                the default value will be returned instead.
        '''
        pattern_map = {
            'scanner-uuid': (r'^[a-fA-F0-9]{8}-'
                             r'[a-fA-F0-9]{4}-'
                             r'[a-fA-F0-9]{4}-'
                             r'[a-fA-F0-9]{4}-'
                             r'[a-fA-F0-9]{12,32}$'
                             )
        }
        if expected_type in ['uuid', 'scanner-uuid']:
            return check(name=name,
                         obj=obj,
                         expected_type=str,
                         pattern=expected_type,
                         case=case,
                         choices=choices,
                         default=default,
                         pattern_map=pattern_map
                         )
        return check(name=name,
                     obj=obj,
                     expected_type=expected_type,
                     regex=pattern,
                     case=case,
                     choices=choices,
                     default=default,
                     pattern_map=pattern_map
                     )
