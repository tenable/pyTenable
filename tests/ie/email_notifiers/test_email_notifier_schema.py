'''
Testing the email notifier schemas
'''
import pytest
from marshmallow import ValidationError

from tenable.ie.email_notifiers.schema import EmailNotifierSchema


@pytest.fixture()
def email_notifier_schema_input_type_deviance():
    return [{
        'input_type': 'deviances',
        'checkers': [1, 2],
        'profiles': [1],
        'address': 'test@domain.com',
        'should_notify_on_initial_full_security_check': False,
        'directories': [1],
        'criticity_threshold': 100,
        'description': 'test alert'
    }]


def test_email_notifier_schema_input_type_deviance_success(
        email_notifier_schema_input_type_deviance):
    '''
    test email notifier schema with create payload and input type as deviances
    '''
    test_resp = [{
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

    schema = EmailNotifierSchema()
    partial = ('attack_types',)
    req = schema.dump(
        schema.load(email_notifier_schema_input_type_deviance, many=True,
                    partial=partial), many=True)

    assert test_resp[0]['address'] == req[0]['address']
    assert test_resp[0]['criticity_threshold'] == req[0]['criticityThreshold']
    assert test_resp[0]['directories'] == req[0]['directories']
    assert test_resp[0]['description'] == req[0]['description']
    assert test_resp[0]['checkers'] == req[0]['checkers']
    assert test_resp[0]['profiles'] == req[0]['profiles']

    with pytest.raises(ValidationError):
        email_notifier_schema_input_type_deviance[0]['some_val'] = 'something'
        schema.load(email_notifier_schema_input_type_deviance, many=True,
                    partial=partial)


@pytest.fixture()
def email_notifier_schema_input_type_attack():
    return [{
        'input_type': 'attacks',
        'attack_types': [1, 2],
        'profiles': [1],
        'address': 'test@domain.com',
        'should_notify_on_initial_full_security_check': False,
        'directories': [1],
        'criticity_threshold': 100,
        'description': 'test alert'
    }]


def test_email_notifier_schema_input_type_attack_success(
        email_notifier_schema_input_type_attack):
    '''
    test email notifier schema with create payload and input type as attacks
    '''
    test_resp = [{
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

    schema = EmailNotifierSchema()
    partial = ('checkers',)
    req = schema.dump(
        schema.load(email_notifier_schema_input_type_attack, many=True,
                    partial=partial), many=True)

    assert test_resp[0]['address'] == req[0]['address']
    assert test_resp[0]['criticity_threshold'] == req[0]['criticityThreshold']
    assert test_resp[0]['directories'] == req[0]['directories']
    assert test_resp[0]['description'] == req[0]['description']
    assert test_resp[0]['attack_types'] == req[0]['attackTypes']
    assert test_resp[0]['profiles'] == req[0]['profiles']

    with pytest.raises(ValidationError):
        email_notifier_schema_input_type_attack[0]['some_val'] = 'something'
        schema.load(email_notifier_schema_input_type_attack, many=True,
                    partial=partial)


def test_email_notifier_schema_directories_validationerror():
    '''
    test to raise exception when blank list is provided in directories
    '''
    with pytest.raises(ValidationError):
        req = [{
            'input_type': 'attacks',
            'attack_types': [1, 2],
            'profiles': [1],
            'address': 'test@domain.com',
            'should_notify_on_initial_full_security_check': False,
            'directories': [],  # no input provided
            'criticity_threshold': 100,
            'description': 'test alert'
        }]
        schema = EmailNotifierSchema()
        schema.load(req, many=True)


def test_email_notifier_schema_attack_types_validationerror():
    '''
    test to raise exception when blank list is provided in attack_types
    '''
    with pytest.raises(ValidationError):
        req = [{
            'input_type': 'attacks',
            'attack_types': [],  # no input provided
            'profiles': [1],
            'address': 'test@domain.com',
            'should_notify_on_initial_full_security_check': False,
            'directories': [1],
            'criticity_threshold': 100,
            'description': 'test alert'
        }]
        schema = EmailNotifierSchema()
        schema.load(req, many=True)


def test_email_notifier_schema_checkers_validationerror():
    '''
    test to raise exception when blank list is provided in checkers
    '''
    with pytest.raises(ValidationError):
        req = [{
            'input_type': 'attacks',
            'checkers': [],  # no input provided
            'profiles': [1],
            'address': 'test@domain.com',
            'should_notify_on_initial_full_security_check': False,
            'directories': [1],
            'criticity_threshold': 100,
            'description': 'test alert'
        }]
        schema = EmailNotifierSchema()
        schema.load(req, many=True)


def test_email_notifier_schema_profiles_validationerror():
    '''
    test to raise exception when blank list is provided in profiles
    '''
    with pytest.raises(ValidationError):
        req = [{
            'input_type': 'attacks',
            'checkers': [1, 2],
            'profiles': [],  # no input provided
            'address': 'test@domain.com',
            'should_notify_on_initial_full_security_check': False,
            'directories': [1],
            'criticity_threshold': 100,
            'description': 'test alert'
        }]
        schema = EmailNotifierSchema()
        schema.load(req, many=True)


def test_email_notifier_schema_input_type_validationerror():
    '''
    test to raise exception when input_type doesn't match the expected values
    '''
    with pytest.raises(ValidationError):
        req = [{
            'input_type': 'something',
            'checkers': [1, 2],
            'profiles': [1],
            'address': 'test@domain.com',
            'should_notify_on_initial_full_security_check': False,
            'directories': [1],
            'criticity_threshold': 100,
            'description': 'test alert'
        }]
        schema = EmailNotifierSchema()
        schema.load(req, many=True)
