'''
Networks API Endpoint Schemas
'''
from marshmallow import Schema, fields, post_dump
from restfly.utils import dict_clean


class NetworkSchema(Schema):
    '''
    Schema for edit and create functions in networks/api.py

    Args:

    '''
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True, dump_default='')
    assets_ttl_days = fields.Int(allow_none=True, dump_default=None)
    scanner_uuids = fields.List(fields.UUID(required=True))

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        if 'description' in data.keys() and not data.get('description'):
            data['description'] = ''
        return dict_clean(data)
