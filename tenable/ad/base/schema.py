from typing import Optional, List, Dict
from marshmallow import Schema, fields, pre_load


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
    start = parts.pop(0)
    last = parts.pop(-1).upper()
    middle = "".join(i.title() for i in parts)
    return f'{start}{middle}{last}'


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
        fn_mapping = getattr(self.Meta, 'case_convertors', {})
        convertor = fn_mapping.get(field_name, camelcase)
        field_obj.data_key = convertor(field_obj.data_key or field_name)

    @pre_load
    def convert_snake_to_camel(self, data, **kwargs) -> Dict:
        resp = {}
        fn_mapping = getattr(self.Meta, 'case_convertors', {})
        for key, value in data.items():
            convertor = fn_mapping.get(key, camelcase)
            resp[convertor(key)] = value
        return resp


class BoolInt(fields.Boolean):
    '''Schema to return an integer value for given boolean value'''

    def _serialize(self, value, attr, obj, **kwargs) -> int:
        return int(value) if value else 0


class BoolStr(fields.Boolean):
    '''Schema to return a string value for given boolean value'''

    def _serialize(self, value, attr, obj, **kwargs) -> str:
        return str(value).lower() if isinstance(value, bool) else None
