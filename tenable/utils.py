import logging
import string
import warnings
from typing import Any

from tenable.base._restfly_v1 import (
    check,
    dict_clean,
    dict_flatten,
    force_case,
    redact_values,
    trunc,
    url_validator,
)
from tenable.base._restfly_v1 import dict_merge as _dm

logger = logging.getLogger(__name__)


__all__ = [
    'check',
    'dict_clean',
    'dict_flatten',
    'dict_merge',
    'force_case',
    'redact_values',
    'url_validator',
    'policy_settings',
    'scrub',
    'trunc',
]


def dict_merge(m, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        return _dm(m, *args, **kwargs)


def policy_settings(item):
    """
    Recursive function to attempt to pull out the various settings from scan
    policy settings in the editor format.
    """
    resp = dict()
    if 'id' in item and (
        'default' in item
        or (
            'type' in item
            and item['type']
            in [
                'file',
                'checkbox',
                'entry',
                'textarea',
                'medium-fixed-entry',
                'password',
            ]
        )
    ):
        # if we find both an 'id' and a 'default' attribute, or if we find
        # a 'type' attribute matching one of the known attribute types, then
        # we will parse out the data and append it to the response dictionary
        if 'default' not in item:
            item['default'] = ''
        resp[item['id']] = item['default']

    for key in item.keys():
        # here we will attempt to recurse down both a list of sub-
        # documents and an explicitly defined sub-document within the
        # editor data-structure.
        if key == 'modes':
            continue
        if (
            isinstance(item[key], list)
            and len(item[key]) > 0
            and isinstance(item[key][0], dict)
        ):
            for i in item[key]:
                resp = dict_merge(resp, policy_settings(i))
        if isinstance(item[key], dict):
            resp = dict_merge(resp, policy_settings(item[key]))

    # Return the key-value pair.
    return resp


def scrub(value: Any) -> str:
    """
    Scrubs converts the value to a string and then scrubs out any illegal characters.
    """
    value = str(value)
    safe_chars = string.ascii_letters + string.digits + '-_%@:'
    scrubbed_value = ''.join([c for c in value if c in safe_chars])
    if value != scrubbed_value:
        logger.warning(
            f"Value '{value}' has unsafe chars, scrubbing to '{scrubbed_value}'"
        )
    return scrubbed_value
