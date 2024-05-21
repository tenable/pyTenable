import pytest
from tenable.nessus.schema.settings import SettingsSchema, SettingsListSchema


def test_settings_schema():
    schema = SettingsSchema()
    data = {'action': 'add', 'name': 'name', 'id': 'id-val', 'value': '123'}
    assert schema.dump(schema.load(data)) == data


def test_setting_list():
    schema = SettingsListSchema()
    setting = {'action': 'add', 'name': 'name', 'id': 'id-val', 'value': '123'}
    resp = schema.dump(schema.load({'settings': [setting for _ in range(3)]}))
    assert resp == {'setting.0.action': 'add',
                    'setting.0.name': 'name',
                    'setting.0.id': 'id-val',
                    'setting.0.value': '123',
                    'setting.1.action': 'add',
                    'setting.1.name': 'name',
                    'setting.1.id': 'id-val',
                    'setting.1.value': '123',
                    'setting.2.action': 'add',
                    'setting.2.name': 'name',
                    'setting.2.id': 'id-val',
                    'setting.2.value': '123',
                    }
