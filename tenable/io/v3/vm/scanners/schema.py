'''
Scanners API Endpoint Schemas
'''
from marshmallow import Schema
from marshmallow import fields as m_fields
from marshmallow import post_dump


class ScannerEditSchema(Schema):
    '''
    Schema for edit functions in api.py

    Args:

    '''

    force_plugin_update = m_fields.Bool()
    force_ui_update = m_fields.Bool()
    finish_update = m_fields.Bool()
    registration_code = m_fields.Str()
    aws_update_interval = m_fields.Int()

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = dict(
            filter(
                lambda item: item[1] not in m_fields.Bool.falsy,
                data.items()
            )
        )
        data.update(
            map(
                lambda item: (
                    item[0], 1) if item[1] in m_fields.Bool.truthy else item,
                data.items(),
            )
        )
        return data
