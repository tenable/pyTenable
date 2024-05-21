from typing import Dict, List, Union
from restfly.utils import dict_merge
from marshmallow import Schema, fields, post_dump, pre_load, validate as v


class SettingsSchema(Schema):
    action = fields.Str(required=True,
                        validate=v.OneOf(['add', 'edit', 'remove']))
    name = fields.Str(required=True)
    id = fields.Str(required=False)
    value = fields.Str(required=False)


class SettingsListSchema(Schema):
    settings = fields.List(fields.Nested(SettingsSchema))

    @post_dump(pass_many=False)
    def reformat_settings_list(self, data, **kwargs):
        idx = 0
        resp = {}

        # Convert the settings from a standard nested object format into the
        # expected setting.{index}.{field} format that this API expects.
        for setting in data['settings']:
            resp[f'setting.{idx}.action'] = setting['action']
            resp[f'setting.{idx}.name'] = setting['name']
            if setting.get('id'):
                resp[f'setting.{idx}.id'] = setting['id']
            if setting.get('value'):
                resp[f'setting.{idx}.value'] = setting['value']
            idx += 1
        return resp
