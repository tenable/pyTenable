import pytest
import responses
from marshmallow import ValidationError

from tests.ie.conftest import RE_BASE


@responses.activate
def test_email_notifiers_list(api):
    '''
    test to list all email notifiers
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/email-notifiers',
                  json=[{
                      'address': 'test@domain.com',
                      'attack_types': None,
                      'checkers': [1, 2],
                      'criticity_threshold': 100,
                      'description': 'test alert',
                      'directories': [1],
                      'id': 1,
                      'input_type': 'deviances',
                      'profiles': [1],
                      'should_notify_on_initial_full_security_check': False
                  }, {
                      'address': 'test@domain.com',
                      'attack_types': [1, 2],
                      'checkers': None,
                      'criticity_threshold': 100,
                      'description': 'test alert',
                      'directories': [1],
                      'id': 2,
                      'input_type': 'attacks',
                      'profiles': [1],
                      'should_notify_on_initial_full_security_check': False
                  }]
                  )
    resp = api.email_notifiers.list()
    assert isinstance(resp, list)
    assert len(resp) == 2

    assert resp[0]['input_type'] == 'deviances'
    assert resp[0]['id'] == 1
    assert resp[0]['address'] == 'test@domain.com'
    assert resp[0]['criticity_threshold'] == 100
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test alert'
    assert resp[0]['checkers'] == [1, 2]
    assert resp[0]['attack_types'] is None
    assert resp[0]['profiles'] == [1]
    assert resp[0]['should_notify_on_initial_full_security_check'] is False

    assert resp[1]['id'] == 2
    assert resp[1]['input_type'] == 'attacks'
    assert resp[1]['address'] == 'test@domain.com'
    assert resp[1]['criticity_threshold'] == 100
    assert resp[1]['directories'] == [1]
    assert resp[1]['description'] == 'test alert'
    assert resp[1]['checkers'] is None
    assert resp[1]['attack_types'] == [1, 2]
    assert resp[1]['profiles'] == [1]
    assert resp[1]['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_email_notifiers_create_input_type_deviance(api):
    '''
    test to create email notifier with input_type as deviance
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/email-notifiers',
                  json=[{
                      'address': 'test@domain.com',
                      'attack_types': None,
                      'checkers': [1, 2],
                      'criticity_threshold': 100,
                      'description': 'test alert',
                      'directories': [1],
                      'id': 1,
                      'input_type': 'deviances',
                      'profiles': [1],
                      'should_notify_on_initial_full_security_check': False
                  }]
                  )
    resp = api.email_notifiers.create(
        input_type='deviances',
        checkers=[1, 2],
        profiles=[1],
        address='test@domain.com',
        should_notify_on_initial_full_security_check=False,
        directories=[1],
        criticity_threshold=100,
        description='test alert'
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['input_type'] == 'deviances'
    assert resp[0]['address'] == 'test@domain.com'
    assert resp[0]['criticity_threshold'] == 100
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test alert'
    assert resp[0]['checkers'] == [1, 2]
    assert resp[0]['attack_types'] is None
    assert resp[0]['profiles'] == [1]
    assert resp[0]['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_email_notifiers_create_input_type_attack(api):
    '''
    test to create email notifier with input_type as attacks
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/email-notifiers',
                  json=[{
                      'address': 'test@domain.com',
                      'attack_types': [1, 2],
                      'checkers': None,
                      'criticity_threshold': 100,
                      'description': 'test alert',
                      'directories': [1],
                      'id': 1,
                      'input_type': 'attacks',
                      'profiles': [1],
                      'should_notify_on_initial_full_security_check': False
                  }]
                  )
    resp = api.email_notifiers.create(
        input_type='attacks',
        attack_types=[1, 2],
        profiles=[1],
        address='test@domain.com',
        should_notify_on_initial_full_security_check=False,
        directories=[1],
        criticity_threshold=100,
        description='test alert'
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['input_type'] == 'attacks'
    assert resp[0]['address'] == 'test@domain.com'
    assert resp[0]['criticity_threshold'] == 100
    assert resp[0]['directories'] == [1]
    assert resp[0]['description'] == 'test alert'
    assert resp[0]['checkers'] is None
    assert resp[0]['attack_types'] == [1, 2]
    assert resp[0]['profiles'] == [1]
    assert resp[0]['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_email_notifiers_create_input_type_validationerror(api):
    '''
    test to raise exception when input_type doesn't match the expected values
    '''
    with pytest.raises(ValidationError):
        api.email_notifiers.create(
            input_type='something',
            attack_types=[1, 2],
            profiles=[1],
            address='test@domain.com',
            should_notify_on_initial_full_security_check=False,
            directories=[1],
            criticity_threshold=100,
            description='test alert'
        )


@responses.activate
def test_email_notifiers_details(api):
    '''
    test to get details of specific email-notifier
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/email-notifiers/1',
                  json={
                      'address': 'test@domain.com',
                      'attack_types': None,
                      'checkers': [1, 2],
                      'criticity_threshold': 100,
                      'description': 'test alert',
                      'directories': [1],
                      'id': 1,
                      'input_type': 'deviances',
                      'profiles': [1],
                      'should_notify_on_initial_full_security_check': False
                  }
                  )
    resp = api.email_notifiers.details(email_notifier_id='1')
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['input_type'] == 'deviances'
    assert resp['address'] == 'test@domain.com'
    assert resp['criticity_threshold'] == 100
    assert resp['directories'] == [1]
    assert resp['description'] == 'test alert'
    assert resp['checkers'] == [1, 2]
    assert resp['attack_types'] is None
    assert resp['profiles'] == [1]
    assert resp['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_email_notifiers_update(api):
    '''
    test to update email notifier
    '''
    responses.add(responses.PATCH,
                  f'{RE_BASE}/email-notifiers/1',
                  json={
                      'address': 'test@domain.com',
                      'attack_types': [1, 2],
                      'checkers': None,
                      'criticity_threshold': 100,
                      'description': 'test alert',
                      'directories': [1],
                      'id': 1,
                      'input_type': 'attacks',
                      'profiles': [1],
                      'should_notify_on_initial_full_security_check': False
                  }
                  )
    resp = api.email_notifiers.update(
        email_notifier_id='1',
        input_type='attacks',
        attack_types=[1, 2],
        profiles=[1],
        address='test@domain.com',
        should_notify_on_initial_full_security_check=False,
        directories=[1],
        criticity_threshold=100,
        description='test alert'
    )
    assert isinstance(resp, dict)
    assert resp['id'] == 1
    assert resp['input_type'] == 'attacks'
    assert resp['address'] == 'test@domain.com'
    assert resp['criticity_threshold'] == 100
    assert resp['directories'] == [1]
    assert resp['description'] == 'test alert'
    assert resp['attack_types'] == [1, 2]
    assert resp['profiles'] == [1]
    assert resp['should_notify_on_initial_full_security_check'] is False


@responses.activate
def test_email_notifiers_delete(api):
    '''
    test to delete email notifier
    '''
    responses.add(responses.DELETE,
                  f'{RE_BASE}/email-notifiers/1',
                  json=None
                  )
    resp = api.email_notifiers.delete(email_notifier_id='1')
    assert resp is None


@responses.activate
def test_email_notifiers_send_test_email_by_id(api):
    '''
    test to send email notifier by id
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/email-notifiers/test-message/1',
                  json=None
                  )
    resp = api.email_notifiers.send_test_email_by_id(email_notifier_id='1')
    assert resp is None


@responses.activate
def test_email_notifiers_send_test_email_input_type_deviance(api):
    '''
    test to send test email notifier with input_type as deviance
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/email-notifiers/test-message',
                  json=None
                  )
    resp = api.email_notifiers.send_test_email(
        input_type='deviances',
        checkers=[1, 2],
        profiles=[1],
        address='test@domain.com',
        directories=[1],
        criticity_threshold=100,
        description='test alert'
    )
    assert resp is None


@responses.activate
def test_email_notifiers_send_test_email_input_type_attack(api):
    '''
    test to send test email notifier with input_type as attacks
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/email-notifiers/test-message',
                  json=None
                  )
    resp = api.email_notifiers.send_test_email(
        input_type='attacks',
        attack_types=[1, 2],
        profiles=[1],
        address='test@domain.com',
        directories=[1],
        criticity_threshold=100,
        description='test alert'
    )
    assert resp is None


@responses.activate
def test_email_notifiers_send_test_email_input_type_validationerror(api):
    '''
    test to raise exception when input_type doesn't match the expected values
    '''
    with pytest.raises(ValidationError):
        api.email_notifiers.send_test_email(
            input_type='something',
            attack_types=[1, 2],
            profiles=[1],
            address='test@domain.com',
            directories=[1],
            criticity_threshold=100,
            description='test alert'
        )
