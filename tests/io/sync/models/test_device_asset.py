import pytest

from tenable.io.sync.models import device_asset as d


def test_device_os_type():
    assert d.DeviceOS(type=None).model_dump(exclude_none=True) == {'type': 'UNKNOWN'}
    assert d.DeviceOS(type='linux').model_dump(exclude_none=True) == {'type': 'LINUX'}


def test_device_status():
    assert d.Device(status='running').model_dump(exclude_none=True) == {
        'status': 'RUNNING'
    }


def test_device_asset_tags():
    data = d.DeviceAsset(
        device={},
        id='12345',
        tags=[
            {'name': 'a', 'value': 'b'},
            {'name': 'a', 'value': 'b'},
            {'name': 'c', 'value': 'd'},
        ],
    ).model_dump(exclude_none=True)

    # TODO: Figure out correct test here
    # assert set(data["tags"]) == set(
    #    {"name": "a", "value": "b"}, {"name": "c", "value": "d"}
    # )
    assert len(data['tags']) == 2


def test_device_asset_labels():
    data = d.DeviceAsset(device={}, id='12345', labels=['a', 'a', 'b', 'c']).model_dump(
        exclude_none=True
    )
    assert set(data['labels']) == set(['a', 'b', 'c'])
    assert len(data['labels']) == 3


def test_device_asset_external_ids():
    data = d.DeviceAsset(
        device={},
        id='12345',
        external_ids=[
            {'qualifier': 'id', 'value': 'a'},
            {'qualifier': 'id', 'value': '5'},
            {'qualifier': 'id', 'value': 'a'},
            {'qualifier': 'uuid', 'value': 'a'},
        ],
    ).model_dump(exclude_none=True)
    assert len(data['external_ids']) == 3
    assert {'qualifier': 'id', 'value': 'a'} in data['external_ids']
    assert {'qualifier': 'uuid', 'value': 'a'} in data['external_ids']
    assert {'qualifier': 'id', 'value': '5'} in data['external_ids']


def test_device_ip_equality():
    assert d.DeviceIPv4(address='192.168.1.1') == d.DeviceIPv4(address='192.168.1.1')
    assert d.DeviceIPv6(address='2345:0425:2CA1::0567:5673:23b5') == d.DeviceIPv6(
        address='2345:0425:2CA1::0567:5673:23b5'
    )


def test_list_of_addresses():
    test_set = [
        d.DeviceIPv4(address='127.0.0.1'),
        d.DeviceIPv4(address='192.168.1.1'),
        d.DeviceIPv4(address='10.0.0.1'),
        d.DeviceIPv4(address='1.2.3.4'),
        d.DeviceIPv4(address='10.0.0.1'),
    ]
    resp = d.list_of_addresses(test_set)
    assert d.DeviceIPv4(address='127.0.0.1') not in resp
    assert d.DeviceIPv4(address='192.168.1.1') in resp
    assert d.DeviceIPv4(address='10.0.0.1') in resp
    assert len(resp) == 3


def test_list_of_ipaddresses_nonetype():
    test_set = [
        d.DeviceIPv4(address='169.254.1.1'),
        d.DeviceIPv4(address='127.0.0.1'),
    ]
    assert d.list_of_addresses(test_set) is None


def test_device_networking():
    obj = d.DeviceNetworking(
        fqdns=[
            {'value': 'a.b.c.d'},
            {'value': 'something.local'},
            {'value': 'a.b.c.d'},
        ],
        ip_addresses_v4=[
            d.DeviceIPv4(address='127.0.0.1'),
            d.DeviceIPv4(address='192.168.1.1'),
        ],
        ip_addresses_v6=[
            d.DeviceIPv6(address='::1'),
            d.DeviceIPv6(address='FE80::'),
            d.DeviceIPv6(address='2001:db8::1'),
        ],
        mac_addresses=['00:de:ad:be:ef:00'],
    )
    resp = obj.model_dump(exclude_none=True, mode='json')
    assert (
        {'value': 'a.b.c.d'} in resp['fqdns']
        and {'value': 'something.local'} in resp['fqdns']
        and len(resp['fqdns']) == 2
    )

    assert (
        {'address': '127.0.0.1'} not in resp['ip_addresses_v4']
        and {'address': '192.168.1.1'} in resp['ip_addresses_v4']
        and len(resp['ip_addresses_v4']) == 1
    )

    assert (
        {'address': '::1'} not in resp['ip_addresses_v6']
        and {'address': 'FE80::'} not in resp['ip_addresses_v6']
        and {'address': '2001:db8::1'} in resp['ip_addresses_v6']
        and len(resp['ip_addresses_v6']) == 1
    )


def test_device_networking_ip_none():
    obj = d.DeviceNetworking(
        ip_addresses_v4=[
            d.DeviceIPv4(address='127.0.0.1'),
            d.DeviceIPv4(address='169.254.0.1'),
        ]
    )
    resp = obj.model_dump(exclude_none=True, mode='json')
    assert resp == {}
