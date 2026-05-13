"""
Vendored version of RESTFly 1.5.1 with some minor tweaks in order to support the subset
of the application thats needed. This is not expected to be called directly and instead
intended to be called from the platform and endpoint modules.
"""

from __future__ import annotations

import json
import logging
import platform
import re
import sys
import time
import warnings
from collections.abc import MutableMapping
from copy import copy
from typing import Any, Self
from urllib.parse import urlparse

import arrow
from box import Box, BoxList
from requests import Response, Session
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
)
from requests.exceptions import (
    RequestException as RequestsRequestException,
)

from tenable import errors


def format_json_response(
    response: Response,
    box_attrs: dict[str, Any] | None = None,
    conv_json: bool = True,
    conv_box: bool = True,
) -> Response | dict[str, Any] | list | Box | BoxList:
    """
    A simple utility to handle formatting the response object into either a
    Box object or a Python native object from the JSON response.  The function
    will prefer box over python native if both flags are set to true.  If none
    of the flags are true, or if the content-type header reports as something
    other than "application/json", then the response object is instead
    returned.

    Args:
        response:
            The response object that will be checked against.
        box_attrs:
            The optional box attributed to pass as part of instantiation.
        conv_json:
            A flag handling if we should run the JSON conversion to python
            native data-types.
        conv_box:
            A flag handling if we should convert the data to a Box object.

    Returns:
        box.Box:
            If the conv_box flag is True, and the response is a single object,
            then the response is a Box obj.
        box.BoxList:
            If the conv_box flag is True, and the response is a list of
            objects, then the response is a BoxList obj.
        dict:
            If the conv_json flag is True and the  conv_box is False, and the
            response is a single object, then the response is a dict obj.
        list:
            If the conv_json flag is True and conv_box is False, and the
            response is a list of objects, then the response is a list obj.
        requests.Response:
            If neither flag is True, or if the response isn't JSON data, then
            a response object is returned (pass-through).
    """
    content_type = response.headers.get('content-type', 'application/json')
    if (
        (conv_json or conv_box)
        and 'application/json' in content_type.lower()
        and len(response.text) > 0
    ):  # noqa: E124
        if conv_box:
            data = response.json()
            if isinstance(data, list):
                return BoxList(data, **box_attrs)
            elif isinstance(data, dict):
                return Box(data, **box_attrs)
        elif conv_json:
            return response.json()
    return response


def url_validator(url: str, validate: list[str] | None = None) -> bool:
    """
    Validates that the required URL Parts exist within the URL string.

    Args:
        url (string):
            The URL to process.
        validate (list[str], optional):
            The URL parts to validate are non-empty.

    Examples:
        >>> url_validator('https://google.com') # Returns True
        >>> url_validator('google.com') #Returns False
        >>> url_validator(
        ...     'https://httpbin.com/404',
        ...     validate=['scheme', 'netloc', 'path'])
            # Returns True
    """
    if not validate:
        validate = ['scheme', 'netloc']
    resp = urlparse(url)._asdict()
    for val in validate:
        if val not in resp or resp[val] == '':
            return False
    return True


def dict_flatten(
    dct: dict,
    sep: str = '.',
    parent_key: str | None = None,
    lower_key: bool = False,
) -> dict:
    """
    Flattens a nested dict.

    Args:
        dct (dict):
            The dictionary to flatten
        parent_key: (str, optional):
            An optional prefix key to add to all entries within the base dictionary.
        sep (str, optional):
            The separation character.  If left unspecified, the default is '.'.
        lower_key (bool, optional):
            If ``True``, will lowercase the keys.

    Examples:
        >>> x = {'a': 1, 'b': {'c': 2}}
        >>> dict_flatten(x)
            {'a': 1, 'b.c': 2}

    inspired by `this <https://stackoverflow.com/a/6027615>`_ Stackoverflow answer.
    """
    items = []
    for key, val in dct.items():
        new_key = f'{parent_key}{sep}{key}' if parent_key else key
        if lower_key:
            new_key = new_key.lower()
        if isinstance(val, MutableMapping):
            items.extend(
                dict_flatten(
                    val, parent_key=new_key, sep=sep, lower_key=lower_key
                ).items()
            )
        elif isinstance(val, list):
            items.append(
                (
                    new_key,
                    [
                        dict_flatten(i, sep=sep, lower_key=lower_key)
                        if isinstance(i, dict)
                        else i
                        for i in val
                    ],
                )
            )
        else:
            items.append((new_key, val))
    return dict(items)


def dict_clean(dct: dict) -> dict:
    """
    Recursively removes dictionary keys where the value is None

    Args:
        d (dict):
            The dictionary to clean

    Returns:
        :obj:`dict`:
            The cleaned dictionary

    Examples:
        >>> x = {'a': 1, 'b': {'c': 2, 'd': None}, 'e': None}
        >>> clean_dict(x)
            {'a': 1, 'b': {'c': 2}}
    """
    clean = {}
    for key, value in dct.items():
        # if the value is a dictionary, then we will recursively clean.
        if isinstance(value, dict):
            new_value = dict_clean(value)
            if len(new_value.keys()) > 0:
                clean[key] = new_value

        # if the value is a list, we will check for any dictionaries within
        # the list and recursively clean.
        elif isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, dict):
                    new_item = dict_clean(item)
                    if len(new_item.keys()) > 0:
                        new_value.append(new_item)
                else:
                    new_value.append(item)
            clean[key] = new_value

        # if the value isn't None, then store the value under the key.
        elif value is not None:
            clean[key] = value

    return clean


def dict_merge(master: dict, *updates: dict) -> dict:
    """
    Merge many dictionaries together  The updates dictionaries will be merged
    into sthe master, adding/updating any values as needed.

    .. warning::
        This function is no longer necessary and will be removed in a later version
        of RESTfly.  For a more pythonic approach to handle this, please refer to
        `PEP-584 <https://peps.python.org/pep-0584/>`_ for modern approaches on merging
        dictionaries.

    Args:
        master (dict):
            The master dictionary to be used as the base.
        *updates (list[dict]):
            The dictionaries that will overload the values in the master.

    Returns:
        :obj:`dict`:
            The merged dictionary

    Examples:
        >>> a = {'one': 1, 'two': 2, 'three': {'four': 4}}
        >>> b = {'a': 'a', 'three': {'b': 'b'}}
        >>> dict_merge(a, b)
        {'a': 'a', 'one': 1, 'two': 2, 'three': {'b': b, 'four': 4}}
    """
    warnings.warn(
        'This function is no longer necessary and will be removed in a later version '
        'of RESTfly.  For a more pythonic approach to handle this, please refer to '
        'PEP-584.',
        DeprecationWarning,
        stacklevel=2,
    )
    for update in updates:
        for key in update:
            if (
                key in master
                and isinstance(master[key], dict)
                and isinstance(update[key], dict)
            ):
                master[key] = dict_merge(master[key], update[key])
            else:
                master[key] = update[key]
    return master


def force_case(obj: Any, case: str | None = None) -> Any:
    """
    A simple case enforcement function.

    Args:
        obj (Object): object to attempt to enforce the case upon.

    Returns:
        :obj:`obj`:
            The modified object

    Examples:
        A list of mixed types:

        >>> a = ['a', 'list', 'of', 'strings', 'with', 'a', 1]
        >>> force_Case(a, 'upper')
        ['A', 'LIST', 'OF', 'STRINGS', 'WITH', 'A', 1]

        A simple string:

        >>> force_case('This is a TEST', 'lower')
        'this is a test'

        A non-string item that'll pass through:

        >>> force_case(1, 'upper')
        1
    """
    if case == 'lower':
        if isinstance(obj, list):
            return [i.lower() for i in obj if isinstance(i, str)]
        elif isinstance(obj, str):
            return obj.lower()

    elif case == 'upper':
        if isinstance(obj, list):
            return [i.upper() for i in obj if isinstance(i, str)]
        elif isinstance(obj, str):
            return obj.upper()

    return obj


def redact_values(
    obj: dict[str, Any], keys: list[str] | None = None, value: str = 'REDACTED'
) -> dict[str, Any]:
    """
    Redacts the values of the keys specified.  Useful in logging so that
    sensitive fields are not presented to the logs.

    Args:
        obj (dict):
            The object upon which redaction will happen.
        keys (list[str], optional):
            The list of key names that should be redacted.
        value (str, optional):
            The redacted value to use in place of the sensitive information.

    Returns:
        :obj:`obj`:
            The modified object.
    """
    if not keys:
        keys = []
    new = copy(obj)
    for key in new:
        if isinstance(new[key], dict):
            new[key] = redact_values(new[key], keys=keys)
        elif key in keys:
            new[key] = value
    return new


def trunc(text: str, limit: int, suffix: str | None = '...') -> str:
    """
    Truncates a string to a given number of characters.  If a string extends
    beyond the limit, then truncate and add an ellipses after the truncation.

    Args:
        text (str): The string to truncate
        limit (int): The maximum limit that the string can be.
        suffix (str):
            What suffix should be appended to the truncated string when we
            truncate?  If left unspecified, it will default to ``...``.


    Returns:
        :obj:`str`:
            The truncated string

    Examples:
        A simple truncation:

        >>> trunc('this is a test', 6)
        'thi...'

        Truncating with no suffix:

        >>> trunc('this is a test', 6, suffix=None)
        'this i'

        Truncating with a custom suffix:

        >>> trunc('this is a test', 6, suffix='->')
        'this->'
    """
    if len(text) >= limit:
        if isinstance(suffix, str):  # noqa: PLR1705
            # If we have a suffix, then reduce the text string length further
            # by the length of the suffix and then concatenate both the text
            # and suffix together.
            return f'{text[: limit - len(suffix)]}{suffix}'
        else:
            # If no suffix, then simply reduce the string size.
            return text[:limit]
    return text


def check(name: str, obj: Any, expected_type: Any, **kwargs) -> Any:
    """
    Check function for validating that inputs we are receiving are of the right
    type, have the expected values, and can handle defaults as necessary.

    Args:
        name (str): The name of the object (for exception reporting)
        obj (obj): The object that we will be checking
        expected_type (type):
            The expected type of object that we will check against.
        choices (list, optional):
            if the object is only expected to have a finite number of values
            then we can check to make sure that our input is one of these
            values.
        default (obj, optional):
            if we want to return a default setting if the object is None,
            we can set one here.
        case (str, optional):
            if we want to force the object values to be upper or lower case,
            then we will want to set this to either ``upper`` or ``lower``
            depending on the desired outcome.  The returned object will then
            also be in the specified case.
        pattern (str, optional):
            Specify a regex pattern from the pattern map variable.
        pattern_map (dict, optional):
            Any additional items to add to the pattern mapping.
        regex (str, optional):
            Validate that the value of the object matches this pattern.
        items_type (type, optional):
            If the expected type is an iterable, and if all of the items
            within that iterable are expected to be a given type, then
            specifying the type here will enable checking each item within
            the iterable.
            NOTE: this will traverse the iterable and return a list object.
        softcheck (bool, optional):
            If the variable is a string type

    Returns:
        :obj:`Object`:
            Either the object or the default object depending.

    Examples:
        Ensure that the value is an integer type:

        >>> check('example', val, int)

        Ensure that the value of val is within 0 and 100:

        >>> check('example', val, int, choices=list(range(100)))
    """

    def validate_regex_pattern(regex, obj):
        if isinstance(obj, str) and len(re.findall(regex, str(obj))) <= 0:
            raise errors.UnexpectedValueError(
                f'{name} has value of {obj}.  Does not match pattern {regex}'
            )

    def validate_choice_list(choices, obj):
        if obj not in choices:
            raise errors.UnexpectedValueError(
                (
                    f'{name} has value of {obj}.  Expected one of '
                    f'{",".join([str(i) for i in choices])}'
                )
            )

    def validate_expected_type(expected, obj, softcheck=True):
        # We need to conditionally set the expected name type local var based
        # on if the expected type has a __name__ attribute.
        if hasattr(expected, '__name__'):
            exp = expected_type.__name__
        else:
            exp = expected

        if isinstance(obj, expected):
            # if everything matches, then just return the object
            return obj
        elif expected == arrow.Arrow:
            return arrow.get(obj)
        elif softcheck and isinstance(obj, str) and expected not in [list, tuple]:
            # if the expected type is not a list or tuple and it is a
            # string type, then we will attempt to recast the object
            # to be the expected type.
            try:
                new_obj = expected(obj)
            except Exception as err:
                # if the recasting fails, then just pass through.
                raise TypeError(
                    (f'{name} is of type {obj.__class__.__name__}.  Expected {exp}')
                ) from err
            else:
                if expected is bool:
                    # if the expected type was boolean, then we will
                    # want to ensure that the string is one of the
                    # allowed values.  From there we will set the
                    # object to be either True or False.  in either case
                    # we will also want to make sure to set the
                    # type_pass flag to ensure we don't raise a
                    # TypeError later on.
                    if obj.lower() in ['true', 'false', 'yes', 'no']:
                        return obj.lower() in ['true', 'yes']
                else:
                    # In every other case, just set the object to be the
                    # recasted object and set the type_pass flag.
                    return new_obj
        raise TypeError(
            (f'{name} is of type {obj.__class__.__name__}.  Expected {exp}')
        )

    def validate_normalized(obj, func, arg):
        if isinstance(obj, (list, tuple)):
            # If the object is a list or tuple type, then lets ensure that
            # all of the items within the obj .
            for item in obj:
                func(arg, item)
        else:
            func(arg, obj)

    pmap = dict_merge(
        {
            'uuid': (
                r'^[0-9a-f]{8}-'
                r'[0-9a-f]{4}-'
                r'[0-9a-f]{4}-'
                r'[0-9a-f]{4}-'
                r'[0-9a-f]{12}$'
            ),
            'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'hex': r'^[a-fA-f0-9]+$',
            'url': (
                r'^(https?:\/\/)?'
                r'([\da-z\.-]+)\.'
                r'([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
            ),
            'ipv4': r'^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$',
            'ipv6': (
                r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|'
                r'([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:'
                r'[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}'
                r'(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}'
                r'(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}'
                r'(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}'
                r'(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:'
                r'((:[0-9a-fA-F]{1,4}){1,6})|:'
                r'((:[0-9a-fA-F]{1,4}){1,7}|:)|'
                r'fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::'
                r'(ffff(:0{1,4}){0,1}:){0,1}'
                r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}'
                r'(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|'
                r'([0-9a-fA-F]{1,4}:){1,4}:'
                r'((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}'
                r'(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
            ),
        },
        kwargs.get('pattern_map', {}),
    )

    # We have a simple function to convert the case of string values so that
    # we can ensure correct output.

    # Convert the case of the inputs.
    obj = force_case(obj, kwargs.get('case'))
    kwargs['choices'] = force_case(kwargs.get('choices'), kwargs.get('case'))
    kwargs['default'] = force_case(kwargs.get('default'), kwargs.get('case'))

    # If the object sent to us has a None value, then we will return None.
    # If a default was set, then we will return the default value.
    allow_none = kwargs.get('allow_none', True)
    if obj is None and allow_none:  # noqa: PLR1705
        return kwargs.get('default')

    # If the allow_none keyword was passed and set to False, we should raise an
    # unexpected value error if none was seen.
    elif obj is None and not allow_none:
        raise errors.UnexpectedValueError(f'{name} has no value.')

    # If the object is none of the right types then we want to raise a
    # TypeError as it was something we weren't expecting.
    obj = validate_expected_type(expected_type, obj, kwargs.get('softcheck', True))

    if kwargs.get('items_type'):
        # If the items within the list should also be of a specific type,
        # we can check those as well
        lobj = []
        for item in obj:
            lobj.append(
                validate_expected_type(
                    kwargs.get('items_type'), item, kwargs.get('softcheck', True)
                )
            )
        obj = lobj

    # if the object is only expected to have one of a finite set of values,
    # we should check against that and raise an exception if the the actual
    # value is outside of what we expect.
    if kwargs.get('choices'):
        validate_normalized(obj, validate_choice_list, kwargs.get('choices'))

    # If a pattern was specified, then we will want to pull the pattern from
    # the pattern map and validate that the
    if kwargs.get('pattern') and kwargs.get('pattern') in pmap:
        validate_normalized(obj, validate_regex_pattern, pmap[kwargs.get('pattern')])

    # If there wasn't a pattern matching that identifier, then throw an
    # IndexError
    elif kwargs.get('pattern') and kwargs.get('pattern') not in pmap.keys():
        raise IndexError(f'pattern name {kwargs.get("pattern")} not found in map')

    # If a raw regex pattern was provided instead, then we will pass that over
    # and validate
    elif kwargs.get('regex'):
        validate_normalized(obj, validate_regex_pattern, kwargs.get('regex'))

    # if we made it this gauntlet without an exception being raised, then
    # assume everything is good to go and return the object passed to us
    # initially.
    return obj


class APIIterator:
    """
    The API iterator provides a scalable way to work through result sets of any
    size.  The iterator will walk through each page of data, returning one
    record at a time.  If it reaches the end of a page of records, then it will
    request the next page of information and then continue to return records
    from the next page (and the next, and the next) until the counter reaches
    the total number of records that the API has reported.

    Note that this Iterator is used as a base model for all of the iterators,
    and while the mechanics of each iterator may vary, they should all behave
    to the user in a similar manner.

    Attributes:
        _api (restfly.session.APISession):
            The APISession object that will be used for querying for the
            data.
        count (int):
            The current number of records that have been returned
        max_items (int):
            The maximum number of items to return before stopping iteration.
        max_pages (int):
            The maximum number of pages to request before throwing stopping
            iteration.
        num_pages (int):
            The number of pages that have been requested.
        page (list):
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int):
            The total number of records that exist for the current request.
    """

    count: int = 0
    page_count: int = 0
    num_pages: int = 0
    max_pages: int | None = None
    max_items: int | None = None
    total: int | None = None
    page: list[Any] = []
    _api: APISession

    def __init__(self, api, **kw):
        """
        Args:
            api (restfly.session.APISession):
                The APISession object to use for this iterator.
            **kw (dict):
                The various attributes to add/overload in the iterator.

        Example:
            >>> i = APIIterator(api, max_pages=1, max_items=100)
        """
        self._api = api
        self.__dict__.update(kw)

        # Create the logging facility
        self._log = logging.getLogger(f'{self.__module__}.{self.__class__.__name__}')

    def _increment_counters(self) -> None:
        """
        Handles incrementing all of the counters that are controlling the next item
        to be retreived.
        """
        self.count += 1
        self.page_count += 1

    def _get_next_item(self) -> Any:
        """
        Returns the next item in the page
        """
        return self[self.page_count]

    def _get_page(self) -> None:
        """
        A method to be overloaded in order to instruct the iterator how to
        retrieve the next page of data.

        Example:
            >>> class ExampleIterator(APIIterator):
            ...    def _get_page(self):
            ...        self.total = 100
            ...        items = range(10)
            ...        self.page = [{'id': i + self._offset} for i in items]
            ...        self._offset += self._limit
        """

    def __getitem__(self, key: int) -> Any:
        return self.page[key]

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Any:
        return self.next()  # noqa: PLE1102

    def get(self, key: int, default: Any | None = None) -> Any:
        """
        Retrieves an item from the the current page based off of the key.

        Args:
            key (int): The index of the item to retrieve.
            default (obj): The returned object if the item does not exist.

        Examples:
            >>> a = APIIterator()
            >>> a.get(2)
            None
        """
        try:
            return self[key]
        except IndexError:
            return default

    def next(self) -> Any:
        """
        Ask for the next record
        """
        # If there are no more records to return, then we should raise a
        # StopIteration exception to break the iterator out.
        if (
            (self.total and self.count + 1 > self.total)  # noqa: PLR0916
            or (self.max_items and self.count >= self.max_items)
        ):
            raise StopIteration()

        # If we have worked through the current page of records and we still
        # haven't hit to the total number of available records, then we should
        # query the next page of records.
        if self.page_count >= len(self.page) and (
            not self.total or self.count + 1 <= self.total
        ):
            # If the number of pages requested reaches the total number of
            # pages that should be requested, then stop iteration.
            if self.max_pages and self.num_pages + 1 > self.max_pages:
                raise StopIteration()

            # Perform the _get_page call.
            self._get_page()
            self.page_count = 0
            self.num_pages += 1

            # If the length of the page is 0, then we don't have anything
            # further to do and should stop iteration.
            if len(self.page) == 0:
                raise StopIteration()

        # Get the relevant record, increment the counters, and return the
        # record.
        item = self._get_next_item()
        self._increment_counters()
        return item


class APISession:
    """
    The APISession class is the base model for APISessions for different
    products and applications.  This is the model that the APIEndpoints
    will be grafted onto and supports some basic wrapping of standard HTTP
    methods on it's own.

    Attributes:
        _box (bool):
            Should responses be converted to Box objects automatically by
            default?  If left unspecified, the default is `False`
        _build (str):
            The build number/version of the integration.
        _backoff (float):
            The default backoff timer to use when retrying.  The value is
            either a float or integer denoting the number of seconds to delay
            before the next retry attempt.  The number will be multiplied by
            the number of retries attempted.
        _base_error_map (dict):
            The error mapping detailing what HTTP response code should throw
            what kind of error.  As this is the base mapping, overloading this
            would remove any pre-set error mappings.
        _error_map (dict):
            The error mapping detailing what HTTP response code should throw
            what kind of error.  This error map will overload specific error
            mappings.
        _error_on_unexpected_input (bool):
            If unexpected keywords have been passed to the session constructor,
            should we raise an error?  Default is ``False``.
        _lib_name (str):
            The name of the library.
        _lib_version (str):
            The version of the library.
        _product (str):
            The product name for the integration.
        _proxies (dict):
            A dictionary detailing what proxy should be used for what transport
            protocol.  This value will be passed to the session object after it
            has been either attached or created.  For details on the structure
            of this dictionary, consult the
            :requests:`Requests documentation.<user/advanced/#proxies>`
        _restricted_paths (list[str]):
            A list of paths (not complete URIs) that if seen be the
            :obj:`_req` method will not pass the query params or the
            request body into the logging facility.  This should generally be
            used for paths that are sensitive in nature (such as logins).
        _retries (int):
            The number of retries to make before failing a request.  The
            default is 3.
        _session (requests.Session):
            Provide a pre-built session instead of creating a requests session
            at instantiation.
        _ssl_verify (bool):
            Should SSL verification be performed?  If not, then inform requests
            that we don't want to use SSL verification and suppress the SSL
            certificate warnings.
        _timeout (int):
            The number of seconds to wait with no data returned before
            declaring the request as stalled and timing-out the request.
        _url (str):
            The base URL path to use.  This should generally be a string value
            denoting the first half of the URI.  For example,
            ``https://httpbin.org`` or ``https://example.api.site/api/2``.  The
            :obj:`_req` method will join this string with the incoming path
            to construct the complete URI.  Note that the two strings will be
            joined with a backslash ``/``.
        _vendor (str):
            The vendor name for the integration.

    Args:
        adapter (Object, optional):
            A Requests Session adapter to bind to the session object.
        adapter_path (str, optional):
            The URL that the adapter will bind to.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.
        build (str, optional):
            The build number to put into the User-Agent string.
        product (str, optional):
            The product name to put into the User-Agent string.
        proxies (dict, optional):
            A dictionary detailing what proxy should be used for what
            transport protocol.  This value will be passed to the session
            object after it has been either attached or created.  For
            details on the structure of this dictionary, consult the
            :requests:`proxies <user/advanced/#proxies>` section of the
            Requests documentation.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is 3.
        session (requests.Session, optional):
            Provide a pre-built session instead of creating a requests
            session at instantiation.
        ssl_verify (bool, optional):
            If SSL Verification needs to be disabled (for example when using
            a self-signed certificate), then this parameter should be set to
            ``False`` to disable verification and mask the Certificate
            warnings.
        url (str, optional):
            The base URL that the paths will be appended onto.
        vendor (str, optional):
            The vendor name to put into the User-Agent string.
    """

    _url: str | None = None
    _base_path: str = ''
    _retries: int = 3
    _backoff: float = 1
    _proxies: dict | tuple | None = None
    _cert: tuple[str, str] | None = None
    _ssl_verify: bool = True
    _lib_name: str = 'Restfly'
    _lib_version: str = '1.5.2-embedded'
    _restricted_paths: list = []
    _vendor: str = 'unknown'
    _product: str = 'unknown'
    _build: str = 'unknown'
    _adapter: Any = None
    _adapter_path: str | None = None
    _timeout: int | None = None
    _conv_json: bool = False
    _box: bool = False
    _box_attrs: dict = {}
    _error_map: dict = {}
    _error_on_unexpected_input: bool = False
    _base_error_map: dict = {
        400: errors.BadRequestError,
        401: errors.UnauthorizedError,
        403: errors.ForbiddenError,
        404: errors.NotFoundError,
        405: errors.InvalidMethodError,
        406: errors.NotAcceptableError,
        407: errors.ProxyAuthenticationError,
        408: errors.RequestTimeoutError,
        409: errors.RequestConflictError,
        410: errors.NoLongerExistsError,
        411: errors.LengthRequiredError,
        412: errors.PreconditionFailedError,
        413: errors.PayloadTooLargeError,
        414: errors.URITooLongError,
        415: errors.UnsupportedMediaTypeError,
        416: errors.RangeNotSatisfiableError,
        417: errors.ExpectationFailedError,
        418: errors.TeapotResponseError,
        420: errors.TooManyRequestsError,
        421: errors.MisdirectRequestError,
        422: errors.InvalidContentError,
        425: errors.TooEarlyError,
        426: errors.UpgradeRequiredError,
        428: errors.PreconditionRequiredError,
        429: errors.TooManyRequestsError,
        431: errors.RequestHeaderFieldsTooLargeError,
        451: errors.UnavailableForLegalReasonsError,
        500: errors.ServerError,
        501: errors.MethodNotImplementedError,
        502: errors.BadGatewayError,
        503: errors.ServiceUnavailableError,
        504: errors.GatewayTimeoutError,
        510: errors.NotExtendedError,
        511: errors.NetworkAuthenticationRequiredError,
    }

    def __enter__(self):
        """
        Context Manager __enter__ built-in method. See PEP-343 for more
        details.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Context Manager __exit__ built-in method. See PEP-343 for more details.
        """
        return self._deauthenticate()

    def __init__(self, **kwargs):
        # Construct the error map from the base mapping, then overload the map
        # with anything specified in the error map parameter and then store the
        # final result in the error map parameter.  This allows for overloading
        # specific items if necessary without having to re-construct the whole
        # map.
        self._error_map = {**self._base_error_map, **self._error_map}

        # Assign the kw arguments to the private attributes.
        self._url = kwargs.pop('url', self._url)
        self._base_path = kwargs.pop('base_path', self._base_path)
        self._retries = int(kwargs.pop('retries', self._retries))
        self._backoff = float(kwargs.pop('backoff', self._backoff))
        self._proxies = kwargs.pop('proxies', self._proxies)
        self._ssl_verify = kwargs.pop('ssl_verify', self._ssl_verify)
        self._adapter_path = kwargs.pop('adapter_path', self._adapter_path)
        self._adapter = kwargs.pop('adapter', self._adapter)
        self._cert = kwargs.pop('cert', self._cert)
        self._vendor = kwargs.pop('vendor', self._vendor)
        self._product = kwargs.pop('product', self._product)
        self._build = kwargs.pop('build', self._build)
        self._error_func = kwargs.pop('error_func', errors.api_error_func)
        self._timeout = kwargs.pop('timeout', self._timeout)
        self._box = kwargs.pop('box', self._box)
        self._box_attrs = kwargs.pop('box_attrs', self._box_attrs)
        self._conv_json = kwargs.pop('conv_json', self._conv_json)

        # Create the logging facility
        self._log = logging.getLogger(f'{self.__module__}.{self.__class__.__name__}')

        # Initiate the session builder.
        self._build_session(**kwargs)
        self._authenticate(**kwargs)

        # if the _error_on_unexpected_input flag is set to True, then we will
        # check to see if any values remain in the kwargs dict, and if so, then
        # error to the caller with the remaining items.
        if self._error_on_unexpected_input and len(kwargs.keys()) > 0:
            raise errors.UnexpectedValueError(
                'The following keywords are invalid {kwargs.keys()}'
            )

    def _build_session(self, **kwargs) -> None:
        """
        The session builder.  User-agent strings, cookies, headers, etc that
        should persist for the session should be initiated here.  The session
        builder is called as part of the APISession constructor.

        Args:
            session (requests.Session, optional):
                If a session object was passed to the constructor, then this
                would contain a session, otherwise a new one is created.

        Returns:
            :obj:`None`

        Examples:
            Extending the session builder to use basic auth:

            >>> class ExampleAPI(APISession):
            ...     def _build_session(self, session=None):
            ...         super(APISession, self)._build_session(**kwargs)
            ...         self._session.auth = (self._username, self._password)
        """
        uname = platform.uname()
        # link up the session to either the one passed or create a new session.
        self._session = kwargs.pop('session', Session())

        # If proxy support is needed, update the proxies in the session.
        if self._proxies:
            self._session.proxies.update(self._proxies)

        # If the SSL verification is disabled then we will need to disable
        # verification in the requests session and we also want to mask the
        # certificate warnings.
        if self._ssl_verify is False:
            self._session.verify = self._ssl_verify
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

        # If client certificate authentication is needed, then we should inject
        # the certificate tuple into the session.
        if self._cert:
            self._session.cert = self._cert

        # if an adapter was specified for the Requests Session, then we should
        # mount that adapter on to the Session object.
        if self._adapter:
            if not self._adapter_path:
                self._adapter_path = f'{self._url}/{self._base_path}'
            self._session.mount(self._adapter_path, self._adapter)

        # Update the User-Agent string with the information necessary.
        py_version = '.'.join([str(i) for i in sys.version_info][0:3])
        opsys = uname[0]
        arch = uname[-2]
        self._session.headers.update(
            {
                'User-Agent': (
                    'Integration/1.0 '
                    f'({self._vendor}; {self._product}; Build/{self._build}) '
                    f'{self._lib_name}/{self._lib_version} '
                    f'(Restfly/1.5.2-embedded; Python/{py_version}; {opsys}/{arch})'
                )
            }
        )

    def _authenticate(self, **kwargs):  # stub
        """
        Authentication stub.  Overload this method with your authentication
        mechanism if you with to support authentication at creation and
        authentication as part of context management.  Note that this is run
        AFTER the session builder.

        Example:
            >>> class ExampleAPISession(APISession):
            ...     def _authenticate(self, username, password):
            ...         self._session.auth = (username, password)
        """

    def _deauthenticate(self, **kwargs):  # stub
        """
        De-authentication stub.  De-authentication is automatically run as part
        of leaving context within the context manager.

        Example:
            >>> class ExampleAPISession(APISession):
            ...     def _deauthenticate(self):
            ...         self.delete('session/token')
        """

    def _resp_error_check(self, response: Response, **kwargs) -> Response:
        """
        If there is a need for additional error checking (for example within
        the JSON response) then overload this method with the necessary
        checking.

        Args:
            response (request.Response):
                The response object.
            **kwargs (dict):
                The request keyword arguments.

        Returns:
            :obj:`requests.Response`:
                The response object.
        """
        return response

    def _retry_request(
        self,
        response: Response,
        retries: int,
        **kwargs,
    ) -> dict:
        """
        A method to be overloaded to return any modifications to the request
        upon retries.  By default just passes back what was send in the same
        order.

        Args:
            response (request.Response):
                The response object
            retries (int):
                The number of retries that have been performed.
            **kwargs (dict):
                The keyword arguments that were passed to the request.

        Returns:
            :obj:`dict`:
                The keyword arguments
        """
        return kwargs

    def _req(
        self, method: str, path: str, **kwargs
    ) -> Box | BoxList | Response | dict[str, Any] | list:
        """
        The requests session base request method.  This is considered internal
        as it's generally recommended to use the bespoke methods for each HTTP
        method.

        Args:
            method (str):
                The HTTP method
            path (str):
                The URI path to append to the base path.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.
            box (bool, optional):
                A request-specific override as to if the response should
                attempted to be converted into a Box object.
            box_attrs (dict, optional):
                A request-specific override with a list of key-values to
                pass to the box constructor.
            conv_json (bool, optional):
                A request-specific override to automatically convert the
                response fromJSON to native data-types.
            redact_fields (list[str], optional):
                A list of keys to redact in the response.  Redaction is used
                for the requests to the API as all of the fields are sent to
                the debug logs.  Note that redaction should be used with care
                as it basically makes a copy fo the request in order to scrub
                the values.
            redact_value (str, optional):
                The value to use to replace the redacted values with.
            retry_on (list[int], optional):
                A list of numeric response status codes to attempt retry on.
                This behavior is additive to the retry parameter in the
                exceptions.
            use_base (bool, optional):
                Should the base path be appended to the URL?  if left
                unspecified the default is `True`.

        Returns:
            :obj:`requests.Response`:
                The default behavior is to return the requests Response object.

            :obj:`box.Box` or :obj:`box.BoxList`:
                If the `box` parameter is set, then the response object will
                be converted to a Box object if the response contains a the
                content type header of "application/json"

            :obj:`dict` or :obj:`list`:
                If the ``conv_json`` parameter is set, then the response object
                will be converted using the Response objects baked-in ``json()``
                method.

            :obj:`None`:
                If either `conv_json` or `box` has been set, however the
                response object has an empty response body, then `None` will
                be returned instead.

        Examples:

            >>> api = APISession()
            >>> resp = api._req('GET', '/')
        """
        error_resp = None
        retries = 0
        kwargs['verify'] = kwargs.get('verify', self._ssl_verify)
        conv_json = kwargs.pop('conv_json', self._conv_json)

        # Ensure that the box variable is set to either Box or BoxList.  Then
        # we want to ensure that "box" is removed from the keyword list.
        conv_box = kwargs.pop('box', self._box)

        # Similarly to the box var, we will want to do the same thing with the
        # box_attrs keyword.
        box_attrs = kwargs.pop('box_attrs', self._box_attrs)

        # If retry_on is specified, then we will populate the retry_codes
        # variable with a list of numeric status codes to additionally retry
        # on.  This is helpful if the API in question doesn't always behave in
        # a consistent manner.
        retry_codes = kwargs.pop('retry_on', [])

        # While the number of retries is less than the retry limit, loop.  As
        # we will be returning from within the loop if we receive a successful
        # response or a non-retryable error, the loop should only be handling
        # the retries themselves.
        while retries <= self._retries:
            # Check to see if the path is a relative path or a full path  If
            # we were able to successfully parse a network location using
            # urlparse, then we will assume that this is a full path and pass
            # the URL as-is.  If it's a relative path, then we will append the
            # baseurl to the path.  In either case, the constructed uri string
            # is what we will be using for the rest of the method for making
            # the actual calls.
            if len(urlparse(path).netloc) > 0:
                uri = path
            elif kwargs.pop('use_base', True) and self._base_path:
                uri = f'{self._url}/{self._base_path}/{path}'
            else:
                uri = f'{self._url}/{path}'

            # Here we will generate the debug log.  As some of the values that
            # may be sent to us could be sensitive in nature, we have multiple
            # ways for the developer to inform us that the data may be
            # sensitive, and to screen out that data from the debug logs.  We
            # will be working through that below.
            rkeys = kwargs.pop('redact_fields', None)
            rval = kwargs.pop('redact_value', 'REDACTED')

            # if the path itself is in the _restricted_paths list, then we will
            # simply replace the body and params
            if path in self._restricted_paths:
                body, params = rval, rval

            # if the redact_fields keyword was passed, then we will make a
            # shallow copy of the body and params and pass those to the
            # redact_values utility function to replace the values for any
            # matching keys to the redact_value.
            elif rkeys:
                body = redact_values(kwargs.get('json', {}), rkeys, rval)
                params = redact_values(kwargs.get('params', {}), rkeys, rval)

            # if no redaction happens, then we will simply store the
            # reference of the body and params in the body and params vars.
            else:
                body = kwargs.get('json', {})
                params = kwargs.get('params', {})

            # And now we generate the log based on body and params that we have
            # sanitized (or not).
            self._log.debug(
                'Request: %s'
                % json.dumps(
                    {'method': method, 'url': uri, 'params': params, 'body': body}
                )
            )

            # Make the call to the API and pull the status code.
            try:
                resp = self._session.request(
                    method, uri, timeout=self._timeout, **kwargs
                )
                status = resp.status_code

            # Here we will catch any underlying exceptions thrown from the
            # requests library, log them, iterate the retry counter, then
            # release the attempt for the next iteration.
            except (RequestsConnectionError, RequestsRequestException) as ereq:
                self._log.error('Requests Library Error: %s', str(ereq))
                time.sleep(1)
                retries += 1
                error_resp = ereq

            # The following code will run when a request successfully returned.
            else:
                if status in self._error_map:
                    # If a status code that we know about has returned, then we
                    # will want to raise the appropriate Error.
                    err = self._error_map[status]
                    error_resp = err(resp, retries=retries, func=self._error_func)
                    if err.retryable or status in retry_codes:
                        # If the APIError fetched is retryable, we will want to
                        # attempt to retry our call.  If we see the
                        # "Retry-After" header, then we will respect that.  If
                        # no "Retry-After" header exists, then we will use the
                        # _backoff attribute to build a back-off timer based on
                        # the number of retries we have already performed.
                        retries += 1
                        time.sleep(
                            float(
                                resp.headers.get('retry-after', retries * self._backoff)
                            )
                        )

                        # The need to potentially modify the request for
                        # subsequent calls is the whole reason that we aren't
                        # using the default Retry logic that urllib3 supports.
                        kwargs = self._retry_request(resp, retries, **kwargs)
                        continue
                    else:
                        raise error_resp

                elif status in range(200, 299):
                    # As everything looks ok, lets pass the response on to the
                    # error checker and then return the response.
                    resp = self._resp_error_check(resp, **kwargs)
                    return format_json_response(
                        response=resp,
                        box_attrs=box_attrs,
                        conv_json=conv_json,
                        conv_box=conv_box,
                    )
                else:
                    # If all else fails, raise an error stating that we don't
                    # even know whats happening.
                    raise errors.APIError(resp, retries=retries, func=self._error_func)
        raise error_resp

    def get(
        self, path: str, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        Initiates an HTTP GET request using the specified path.  Refer to
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to
                :py:meth:`restfly.session.APISession._req`.

        Returns:
            :obj:`requests.Response` or :obj:`box.Box`
                If the request was informed to attempt to "boxify" the response
                and the response was JSON data, then a Box will be returned.
                In all other scenarios, a Response object will be returned.

        Examples:
            >>> api = APISession()
            >>> resp = api.get('/')
        """
        return self._req('GET', path, **kwargs)

    def post(
        self, path: str, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        Initiates an HTTP POST request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to
                :py:meth:`restfly.session.APISession._req`.

        Returns:
            :obj:`requests.Response` or :obj:`box.Box`
                If the request was informed to attempt to "boxify" the response
                and the response was JSON data, then a Box will be returned.
                In all other scenarios, a Response object will be returned.

        Examples:
            >>> api = APISession()
            >>> resp = api.post('/')
        """
        return self._req('POST', path, **kwargs)

    def put(
        self, path: str, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        Initiates an HTTP PUT request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to
                :py:meth:`restfly.session.APISession._req`.

        Returns:
            :obj:`requests.Response` or :obj:`box.Box`
                If the request was informed to attempt to "boxify" the response
                and the response was JSON data, then a Box will be returned.
                In all other scenarios, a Response object will be returned.

        Examples:
            >>> api = APISession()
            >>> resp = api.put('/')
        """
        return self._req('PUT', path, **kwargs)

    def patch(
        self, path: str, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        Initiates an HTTP PATCH request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to
                :py:meth:`restfly.session.APISession._req`.

        Returns:
            :obj:`requests.Response` or :obj:`box.Box`
                If the request was informed to attempt to "boxify" the response
                and the response was JSON data, then a Box will be returned.
                In all other scenarios, a Response object will be returned.

        Examples:
            >>> api = APISession()
            >>> resp = api.patch('/')
        """
        return self._req('PATCH', path, **kwargs)

    def delete(
        self, path: str, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        Initiates an HTTP DELETE request using the specified path.  Refer to
        the :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to
                :py:meth:`restfly.session.APISession._req`.

        Returns:
            :obj:`requests.Response` or :obj:`box.Box`
                If the request was informed to attempt to "boxify" the response
                and the response was JSON data, then a Box will be returned.
                In all other scenarios, a Response object will be returned.

        Examples:
            >>> api = APISession()
            >>> resp = api.delete('/')
        """
        return self._req('DELETE', path, **kwargs)

    def head(
        self, path: str, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        Initiates an HTTP HEAD request using the specified path.  Refer to the
        :obj:`requests.request` for more detailed information on what
        keyword arguments can be passed:

        Args:
            path (str):
                The path to be appended onto the base URL for the request.
            **kwargs (dict):
                Keyword arguments to be passed to
                :py:meth:`restfly.session.APISession._req`.

        Returns:
            :obj:`requests.Response` or :obj:`box.Box`
                If the request was informed to attempt to "boxify" the response
                and the response was JSON data, then a Box will be returned.
                In all other scenarios, a Response object will be returned.

        Examples:
            >>> api = APISession()
            >>> resp = api.head('/')
        """
        return self._req('HEAD', path, **kwargs)


class APIEndpoint:  # noqa: PLR0903
    """
    APIEndpoint is the base model for which all API endpoint classes are
    sired from.  The main benefit is the ability to use the http request methods that
    are attached to this base class.  This allows for keeping common CRUD-type calls
    together with minimal manual URL munging.

    Attributes:
        _path (str):
            The URI path to append to the base path as is specified in the
            APISession object.  This can become quite useful if most of the
            CRUD follows the same pathing.  It is only used when using the
            APIEndpoint verbs (_get, _post, _put, etc.).
        _box (bool):
            An endpoint-specific version of `APISession._box`.
        _box_attrs (bool):
            An endpoint-specific version of `APISession._box_attrs`.
        _conv_json (bool):
            An endpoint-specific version of `APISession._conv_json`.

    Args:
        api (APISession):
            The APISession (or sired child) instance that the endpoint will
            be using to perform calls to the API.
    """

    _path: str | None = None
    _box: bool | None = None
    _conv_json: bool | None = None
    _box_attrs: dict | None = None

    def __init__(self, api: APISession):
        self._api = api
        self._log = api._log

    def _req(
        self, method: str, path: str | None = None, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        An abstraction of the APISession._req method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api._req``.

        Args:
            method (str):
                The HTTP method
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._req('GET', **kwargs)
        """
        if self._box:
            kwargs['box'] = kwargs.get('box', self._box)
        if self._box_attrs:
            kwargs['box_attrs'] = kwargs.get('box_attrs', self._box_attrs)
        if self._conv_json:
            kwargs['conv_json'] = kwargs.get('conv_json', self._conv_json)
        new_path = '/'.join([p for p in [self._path, path] if p])
        return self._api._req(method, new_path, **kwargs)

    def _delete(
        self, path: str | None = None, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        An abstraction of the APISession.delete method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.delete``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._delete(**kwargs)
        """
        return self._req('DELETE', path, **kwargs)

    def _get(
        self, path: str | None = None, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        An abstraction of the APISession.get method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.get``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._get(**kwargs)
        """
        return self._req('GET', path, **kwargs)

    def _head(
        self, path: str | None = None, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        An abstraction of the APISession.head method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.head``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._head(**kwargs)
        """
        return self._req('HEAD', path, **kwargs)

    def _patch(
        self, path: str | None = None, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        An abstraction of the APISession.patch method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.patch``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._patch(**kwargs)
        """
        return self._req('PATCH', path, **kwargs)

    def _post(
        self, path: str | None = None, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        An abstraction of the APISession.post method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.post``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._post(**kwargs)
        """
        return self._req('POST', path, **kwargs)

    def _put(
        self, path: str | None = None, **kwargs
    ) -> list | dict[str, Any] | Box | BoxList | Response:
        """
        An abstraction of the APISession.put method leveraging the local
        APIEndpoint _path attribute as well.  This isn't intended to be called
        directly, and instead is offered as a shortcut for methods within the
        endpoint to use instead of ``self._api.put``.

        Args:
            path (str, optional):
                The URI path to append to the base path and _path attribute.
            **kwargs (dict):
                The keyword arguments to pass to the requests lib.

        Examples:
            >>> class Endpoint(APIEndpoint):
            ...     _path = 'test'
            ...     def list(**kwargs):
            ...         return self._put(**kwargs)
        """
        return self._req('PUT', path, **kwargs)
