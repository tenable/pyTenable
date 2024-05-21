'''
API tests for syslog endpoints
'''
import pytest
import responses
from marshmallow import ValidationError

from tests.ad.conftest import RE_BASE


@responses.activate
def test_syslog_list(api):
    '''
    test to list all the syslogs
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/syslogs',
                  json=[{
                      'attack_types': None,
                      'checkers': [1],
                      'criticity_threshold': 10,
                      'description': 'test_syslog',
                      'directories': [1],
                      'filter_expression': {'OR': [{'systemOnly': 'True'}]},
                      'id': 1,
                      'input_type': 'deviances',
                      'ip': '127.0.0.1',
                      'port': 8888,
                      'profiles': [1],
                      'protocol': 'UDP',
                      'should_notify_on_initial_full_security_check': True,
                      'tls': False
                  }, {
                      'attack_types': [1, 2],
                      'checkers': None,
                      'criticity_threshold': 70,
                      'description': 'test_syslog',
                      'directories': [1],
                      'filter_expression': None,
                      'id': 2,
                      'input_type': 'attacks',
                      'ip': '127.0.0.1',
                      'port': 8889,
                      'profiles': [1],
                      'protocol': 'TCP',
                      'should_notify_on_initial_full_security_check':
                          True,
                      'tls': True
                  }, {
                      'attack_types': None,
                      'checkers': None,
                      'criticity_threshold': 0,
                      'description': 'syslog_test_desc',
                      'directories': [1],
                      'filter_expression': {
                          'AND': [{'systemOnly': 'TRUE'}]},
                      'id': 3,
                      'input_type': 'adObjectChanges',
                      'ip': '127.0.0.1',
                      'port': 514,
                      'profiles': None,
                      'protocol': 'TCP',
                      'should_notify_on_initial_full_security_check':
                          False,
                      'tls': False
                  }]
                  )
    resp = api.syslog.list()
    assert isinstance(resp, list)
    assert len(resp) == 3

    assert resp[0]['id'] == 1
    assert resp[0]['input_type'] == 'deviances'
    assert resp[0]['criticity_threshold'] == 10
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test_syslog'
    assert resp[0]['checkers'] == [1]
    assert resp[0]['attack_types'] is None
    assert resp[0]['profiles'] == [1]
    assert resp[0]['should_notify_on_initial_full_security_check'] is True
    assert resp[0]['protocol'] == 'UDP'
    assert resp[0]['tls'] is False

    assert resp[1]['id'] == 2
    assert resp[1]['input_type'] == 'attacks'
    assert resp[1]['criticity_threshold'] == 70
    assert resp[1]['directories'] == [1]
    assert resp[1]['description'] == 'test_syslog'
    assert resp[1]['checkers'] is None
    assert resp[1]['attack_types'] == [1, 2]
    assert resp[1]['profiles'] == [1]
    assert resp[1]['should_notify_on_initial_full_security_check'] is True

    assert resp[2]['id'] == 3
    assert resp[2]['input_type'] == 'adObjectChanges'
    assert resp[2]['criticity_threshold'] == 0
    assert resp[2]['directories'] == [1]
    assert resp[2]['description'] == 'syslog_test_desc'
    assert resp[2]['checkers'] is None
    assert resp[2]['attack_types'] is None
    assert resp[2]['profiles'] is None
    assert resp[2]['filter_expression'] == {'AND': [{'systemOnly': 'TRUE'}]}
    assert resp[2]['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_syslog_create_input_type_deviance(api):
    '''
    test to create a syslog with input_type as deviance
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/syslogs',
                  json=[{
                      'attack_types': None,
                      'checkers': [1],
                      'criticity_threshold': 55,
                      'description': 'test_syslog',
                      'directories': [1],
                      'filter_expression': {'OR': [{'systemOnly': 'True'}]},
                      'id': 1,
                      'input_type': 'deviances',
                      'ip': '127.0.0.1',
                      'port': 8888,
                      'profiles': [1],
                      'protocol': 'TCP',
                      'should_notify_on_initial_full_security_check': False,
                      'tls': True
                  }]
                  )
    resp = api.syslog.create(
        description='test_syslog',
        input_type="deviances",
        profiles=[1],
        checkers=[1],
        ip='127.0.0.1',
        port=8888,
        protocol="TCP",
        tls=True,
        criticity_threshold=55,
        directories=[1],
        should_notify_on_initial_full_security_check=False,
        filter_expression={'OR': [{'systemOnly': 'True'}]}
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['input_type'] == 'deviances'
    assert resp[0]['criticity_threshold'] == 55
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test_syslog'
    assert resp[0]['checkers'] == [1]
    assert resp[0]['attack_types'] is None
    assert resp[0]['profiles'] == [1]
    assert resp[0]['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_syslog_create_input_type_attack(api):
    '''
    test to create a syslog with input_type as attacks
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/syslogs',
                  json=[{
                      'attack_types': [1],
                      'checkers': None,
                      'criticity_threshold': 70,
                      'description': 'test_syslog',
                      'directories': [1],
                      'filter_expression': {'OR': [{'systemOnly': 'True'}]},
                      'id': 1,
                      'input_type': 'attacks',
                      'ip': '127.0.0.1',
                      'port': 8888,
                      'profiles': [1],
                      'protocol': 'UDP',
                      'should_notify_on_initial_full_security_check': True,
                      'tls': False
                  }]
                  )
    resp = api.syslog.create(
        description='test_syslog',
        input_type="attacks",
        profiles=[1],
        attack_types=[1],
        ip='127.0.0.1',
        port=8888,
        protocol="UDP",
        criticity_threshold=70,
        directories=[1],
        should_notify_on_initial_full_security_check=True,
        filter_expression={'OR': [{'systemOnly': 'True'}]}
    )

    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['input_type'] == 'attacks'
    assert resp[0]['criticity_threshold'] == 70
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test_syslog'
    assert resp[0]['checkers'] is None
    assert resp[0]['attack_types'] == [1]
    assert resp[0]['profiles'] == [1]
    assert resp[0]['protocol'] == 'UDP'
    assert resp[0]['tls'] is False
    assert resp[0]['should_notify_on_initial_full_security_check'] is True


@responses.activate
def test_syslog_create_input_type_ad_object_changes(api):
    '''
    test to create a syslog with input_type as ad_object_changes
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/syslogs',
                  json=[{
                      'attack_types': None,
                      'checkers': None,
                      'criticity_threshold': 0,
                      'description': 'test_syslog',
                      'directories': [1],
                      'filter_expression': {'OR': [{'systemOnly': 'True'}]},
                      'id': 1,
                      'input_type': 'adObjectChanges',
                      'ip': '127.0.0.1',
                      'port': 8888,
                      'profiles': None,
                      'protocol': 'TCP',
                      'should_notify_on_initial_full_security_check': False,
                      'tls': False
                  }]
                  )
    resp = api.syslog.create(
        description='test_syslog',
        input_type="ad_object_changes",
        ip='127.0.0.1',
        port=8888,
        protocol="TCP",
        tls=False,
        directories=[1],
        should_notify_on_initial_full_security_check=False,
        filter_expression={'OR': [{'systemOnly': 'True'}]}
    )

    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['input_type'] == 'adObjectChanges'
    assert resp[0]['criticity_threshold'] == 0
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test_syslog'
    assert resp[0]['checkers'] is None
    assert resp[0]['attack_types'] is None
    assert resp[0]['profiles'] is None
    assert resp[0]['protocol'] == 'TCP'
    assert resp[0]['tls'] is False
    assert resp[0]['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_syslog_passing_protocol_in_lower_case(api):
    '''
    test to create a syslog when protocol is passed in lower case.
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/syslogs',
                  json=[{
                      'attack_types': None,
                      'checkers': None,
                      'criticity_threshold': 0,
                      'description': 'test_syslog',
                      'directories': [1],
                      'filter_expression': {'OR': [{'systemOnly': 'True'}]},
                      'id': 1,
                      'input_type': 'adObjectChanges',
                      'ip': '127.0.0.1',
                      'port': 8888,
                      'profiles': None,
                      'protocol': 'TCP',
                      'should_notify_on_initial_full_security_check': False,
                      'tls': False
                  }]
                  )
    resp = api.syslog.create(
        description='test_syslog',
        input_type="ad_object_changes",
        ip='127.0.0.1',
        port=8888,
        protocol="tcp",  # passed in lower case
        tls=False,
        directories=[1],
        should_notify_on_initial_full_security_check=False,
        filter_expression={'OR': [{'systemOnly': 'True'}]}
    )

    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['input_type'] == 'adObjectChanges'
    assert resp[0]['criticity_threshold'] == 0
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test_syslog'
    assert resp[0]['checkers'] is None
    assert resp[0]['attack_types'] is None
    assert resp[0]['profiles'] is None
    assert resp[0]['protocol'] == 'TCP'
    assert resp[0]['tls'] is False
    assert resp[0]['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_syslog_create_input_type_validation_error(api):
    '''
    test to raise exception when input_type doesn't match the expected values
    '''
    with pytest.raises(ValidationError):
        api.syslog.create(
            input_type='something',  # invalid input_type
            attack_types=[1],
            profiles=[1],
            should_notify_on_initial_full_security_check=False,
            directories=[1],
            criticity_threshold=50,
            description='test_syslog'
        )


@responses.activate
def test_syslog_details(api):
    '''
    test to get details of specific syslog object.
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/syslogs/1',
                  json={
                      'attack_types': [1],
                      'checkers': None,
                      'criticity_threshold': 0,
                      'description': 'test_syslog',
                      'directories': [1],
                      'filter_expression': None,
                      'id': 1,
                      'input_type': 'attacks',
                      'ip': '127.0.0.1',
                      'port': 8889,
                      'profiles': [1],
                      'protocol': 'TCP',
                      'should_notify_on_initial_full_security_check': True,
                      'tls': True
                  }
                  )
    resp = api.syslog.details(syslog_id='1')
    assert isinstance(resp, dict)
    assert resp['attack_types'] == [1]
    assert resp['checkers'] is None
    assert resp['criticity_threshold'] == 0
    assert resp['description'] == 'test_syslog'
    assert resp['directories'] == [1]
    assert resp['filter_expression'] is None
    assert resp['id'] == 1
    assert resp['input_type'] == 'attacks'
    assert resp['ip'] == '127.0.0.1'
    assert resp['port'] == 8889
    assert resp['profiles'] == [1]
    assert resp['protocol'] == 'TCP'
    assert resp['should_notify_on_initial_full_security_check'] is True
    assert resp['tls'] is True


@responses.activate
def test_syslog_update(api):
    '''
    test to update syslog object.
    '''
    responses.add(responses.PATCH,
                  f'{RE_BASE}/syslogs/1',
                  json={
                      'attack_types': [1, 2],
                      'checkers': None,
                      'criticity_threshold': 100,
                      'description': 'test_updated_syslog',
                      'directories': [2],
                      'id': 1,
                      'input_type': 'attacks',
                      'ip': '127.0.0.1',
                      'profiles': [2],
                      'should_notify_on_initial_full_security_check': True,
                      'port': 514,
                      'protocol': 'UDP',
                      'tls': False,
                      'filter_expression': {'OR': [{'systemOnly': 'True'}]},
                  }
                  )
    resp = api.syslog.update(
        syslog_id='1',
        input_type='attacks',
        attack_types=[1, 2],
        profiles=[2],
        checkers=[1],
        should_notify_on_initial_full_security_check=True,
        directories=[2],
        criticity_threshold=100,
        description='test_updated_syslog',
        port=514,
        protocol='UDP',
        filter_expression={'OR': [{'systemOnly': 'True'}]}
    )
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['input_type'] == 'attacks'
    assert resp['criticity_threshold'] == 100
    assert resp['directories'] == [2]
    assert resp['description'] == 'test_updated_syslog'
    assert resp['attack_types'] == [1, 2]
    assert resp['profiles'] == [2]
    assert resp['checkers'] is None
    assert resp['should_notify_on_initial_full_security_check'] is True
    assert resp['protocol'] == 'UDP'
    assert resp['filter_expression'] == {'OR': [{'systemOnly': 'True'}]}


@responses.activate
def test_syslog_delete(api):
    '''
    test to delete a syslog object.
    '''
    responses.add(responses.DELETE,
                  f'{RE_BASE}/syslogs/1',
                  json=None
                  )
    resp = api.syslog.delete(syslog_id='1')
    assert resp is None


@responses.activate
def test_syslog_send_notification_by_id(api):
    '''
    test to send syslog notification by id
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/syslogs/test-message/1',
                  json=None
                  )
    resp = api.syslog.send_syslog_notification_by_id(syslog_id='1')
    assert resp is None


@responses.activate
def test_syslog_notification_input_type_deviance(api):
    '''
    test to send test syslog notification with input_type as deviance
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/syslogs/test-message',
                  json=None
                  )
    resp = api.syslog.send_notification(
        input_type="deviances",
        ip='127.0.0.1',
        port=8888,
        protocol="TCP",
        tls=True,
        directories=[2],
        profiles=[1],
        checkers=[1],
        criticity_threshold=0
    )
    assert resp is None


@responses.activate
def test_syslog_notification_input_type_attacks(api):
    '''
    test to send test syslog notification with input_type as attacks
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/syslogs/test-message',
                  json=None
                  )
    resp = api.syslog.send_notification(
        checkers=[1],
        profiles=[1],
        input_type="attacks",
        attack_types=[1],
        ip='127.0.0.1',
        port=8888,
        protocol="TCP",
        tls=True,
        criticity_threshold=10,
        directories=[2]
    )
    assert resp is None


@responses.activate
def test_syslog_notification_input_type_ad_object_changes(api):
    '''
    test to send test syslog notification with input_type as ad_object_changes
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/syslogs/test-message',
                  json=None
                  )
    resp = api.syslog.send_notification(
        input_type="ad_object_changes",
        ip='127.0.0.1',
        port=8888,
        protocol="TCP",
        tls=True,
        directories=[2],
    )
    assert resp is None


@responses.activate
def test_syslog_notification_input_type_validation_error(api):
    '''
    test to raise exception when input_type doesn't match the expected values
    '''
    with pytest.raises(ValidationError):
        api.syslog.send_notification(
            input_type="something",  # invalid input_type
            ip='127.0.0.1',
            port=8888,
            protocol="TCP",
            tls=True,
            directories=[2],
            criticity_threshold=0,
            attack_types=[1]
        )
