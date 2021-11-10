'''
Extended field definitions
'''
from marshmallow import fields


class BaseField(fields.Field):
    '''
    BaseField Field
    '''

    def __init__(self, inner, *args, **kwargs):
        self.inner = inner
        super().__init__(*args, **kwargs)

    def _bind_to_schema(self, field_name, parent):  # noqa PLW0221
        super()._bind_to_schema(field_name, parent)
        self.inner._bind_to_schema(field_name, parent)  # noqa PLW0212

    def _deserialize(self, value, *args, **kwargs):
        return self.inner._deserialize(value, *args, **kwargs)  # noqa PLW0212

    def _serialize(self, *args, **kwargs):
        return self.inner._serialize(*args, **kwargs)  # noqa PLW0212


class LowerCase(BaseField):
    '''
    The field value will be lower-cased with this field.
    '''

    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'lower'):
            value = value.lower()
        return super()._deserialize(value, *args, **kwargs)


class UpperCase(BaseField):
    '''
    The field value will be upper-cased with this field.
    '''

    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'upper'):
            value = value.upper()
        return super()._deserialize(value, *args, **kwargs)
