import pytest
from marshmallow import ValidationError

from tenable.io.v3.connectors.schema import (ConnectorCreateOrEditSchema,
                                             ConnectorListTrails,
                                             ConnectorRegion,
                                             ConnectorSchedule)


def test_create():
    network_id = '00000000-0000-0000-0000-000000000000'
    resp_data = dict(
        name='test',
        type='aws_keyless',
        network_id=network_id,
        schedule={
            'units': 'days',
            'value': 2
        },
        params={
            'import_config': True,
            'sub_accounts': [{}]
        }
    )

    raw_data = {
        'name': 'test',
        'type': 'aws_keyless',
        'network_id': network_id,
        'schedule': ('days', 2),
        'params': {
            'import_config': True,
            'sub_accounts': [{}]
        }
    }

    schema = ConnectorCreateOrEditSchema()
    payload = schema.dump(schema.load(raw_data))

    assert payload == resp_data

    with pytest.raises(ValidationError):
        payload['test'] = 'test'
        schema.load(payload)


def test_schedule():
    resp_data = {
        'units': 'minutes',
        'value': 50
    }

    schema = ConnectorSchedule()
    payload = schema.dump(schema.load(resp_data))

    assert payload == resp_data

    with pytest.raises(ValidationError):
        payload['test'] = 'test'
        schema.load(payload)


def test_region():
    resp_data = {
        'name': 'All',
        'friendly_name': 'All'
    }

    schema = ConnectorRegion()
    payload = schema.dump(schema.load(resp_data))

    assert payload == resp_data

    with pytest.raises(ValidationError):
        payload['test'] = 'test'
        schema.load(payload)


def test_list_trails():
    resp_data = {
        'region':
            [{'friendly_name': 'US East (N. Virginia)', 'name': 'us-east-1'}],
        'account_id': 'sdfas7df9s8df7as87df8a7s9d',
        'credentials':
            {
                'access_key':
                    'd08c2a75517ad18da1d1d2e8f9ea70792f658674b352a9a00e7fcc4a74dcff6a', # noqa E501
                'secret_key':
                    'be13082452f57880261e8170290490026417745b8cde8a7d1e554d16eff690bf' # noqa E501
            }
    }

    raw_data = {
        'region': [('us-east-1', 'US East (N. Virginia)')],
        'credentials': {
            'access_key':
                'd08c2a75517ad18da1d1d2e8f9ea70792f658674b352a9a00e7fcc4a74dcff6a', # noqa E501
            'secret_key':
                'be13082452f57880261e8170290490026417745b8cde8a7d1e554d16eff690bf' # noqa E501
        },
        'account_id': 'sdfas7df9s8df7as87df8a7s9d'
    }

    schema = ConnectorListTrails()
    payload = schema.dump(schema.load(raw_data))
    assert payload == resp_data

    with pytest.raises(ValidationError):
        payload['test'] = 'test'
        schema.load(payload)
