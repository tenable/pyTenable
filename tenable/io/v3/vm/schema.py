'''
Scanners API Endpoint Schemas
'''
from marshmallow import Schema, fields, post_dump


class ScannerEditSchema(Schema):
    '''
    Schema for edit functions in scanners.py

    Args:

    '''

    force_plugin_update = fields.Bool()
    force_ui_update = fields.Bool()
    finish_update = fields.Bool()
    registration_code = fields.Str()
    aws_update_interval = fields.Int()

    @post_dump
    def post_serialization(self, data, **kwargs):  # noqa PLR0201 PLW0613
        data = dict(
            filter(
                lambda item: item[1] not in fields.Bool.falsy,
                data.items()
            )
        )
        data.update(
            map(
                lambda item: (
                    item[0], 1) if item[1] in fields.Bool.truthy else item,
                data.items(),
            )
        )
        return data
