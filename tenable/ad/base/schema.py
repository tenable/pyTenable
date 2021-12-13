from typing import Optional, List
from marshmallow import Schema


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def last_word_uppercase(s):
    '''
    converts last word to uppercase

    Example:
        example_field -> exampleFIELD
    '''
    parts = s.split("_")
    return parts[0] + "".join(i.title() for i in parts[1:len(parts) - 1]) + \
           parts[-1].upper()


def convert_keys_to_camel(data: dict,
                          special: Optional[List[str]] = None
                          ) -> dict:
    '''
    Convert dictionary keys to camel case

    Example:
        example_field -> exampleField

    and for special field names
    will convert last word to uppercase.

    Example:
        example_field -> exampleFIELD

    Args:
        data (dict):
            The data dictionary.
        special (optional, list[str]):
            The list of special field for converting last word to uppercase.
    '''
    if special is None:
        special = []

    resp = {}
    for key, value in data.items():
        if key in special:
            resp[last_word_uppercase(key)] = value
        else:
            resp[camelcase(key)] = value
    return resp


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    def on_bind_field(self, field_name, field_obj):
        last_word_uppercase_field_names = ['search_user_dn']

        if field_name in last_word_uppercase_field_names:
            field_obj.data_key = last_word_uppercase(
                field_obj.data_key or field_name)
        else:
            field_obj.data_key = camelcase(field_obj.data_key or field_name)
