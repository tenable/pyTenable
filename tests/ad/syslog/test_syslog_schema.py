'''
Testing the syslog schema
'''
import pytest
from marshmallow import ValidationError
from tenable.ad.syslog.schema import SyslogSchema


@pytest.fixture
def syslog_schema_input_type_deviances():
    return [{
        'input_type': 'deviances',
        'checkers': [1],
        'profiles': [1],
        'should_notify_on_initial_full_security_check': False,
        'directories': [1],
        'criticity_threshold': 55,
        'description': 'test_syslog',
        'ip': '127.0.0.1',
        'protocol': 'TCP',
        'tls': True,
        'port': 514,
        'filter_expression': {'OR': [{'systemOnly': 'True'}]}
    }]


def test_syslog_schema_input_type_deviance(
        syslog_schema_input_type_deviances):
    '''
    test syslog schema with create payload and input type as deviances
    '''
    test_resp = [{
        'attack_types': None,
        'checkers': [1],
        'criticity_threshold': 55,
        'description': 'test_syslog',
        'directories': [1],
        'filter_expression': {'OR': [{'systemOnly': 'True'}]},
        'id': 1,
        'input_type': 'deviances',
        'ip': '127.0.0.1',
        'port': 514,
        'profiles': [1],
        'protocol': 'TCP',
        'should_notify_on_initial_full_security_check': False,
        'tls': True
    }]

    schema = SyslogSchema()
    partial = ('attack_types',)
    req = schema.dump(
        schema.load(syslog_schema_input_type_deviances, many=True,
                    partial=partial), many=True)

    assert isinstance(req, list)
    assert test_resp[0]['port'] == req[0]['port']
    assert test_resp[0]['ip'] == req[0]['ip']
    assert test_resp[0]['protocol'] == req[0]['protocol']
    assert test_resp[0]['tls'] == req[0]['tls']
    assert test_resp[0]['criticity_threshold'] == req[0]['criticityThreshold']
    assert test_resp[0]['directories'] == req[0]['directories']
    assert test_resp[0]['description'] == req[0]['description']
    assert test_resp[0]['checkers'] == req[0]['checkers']
    assert test_resp[0]['profiles'] == req[0]['profiles']
    assert test_resp[0]['filter_expression'] == req[0]['filterExpression']
    with pytest.raises(ValidationError):
        syslog_schema_input_type_deviances[0]['some_val'] = 'something'
        schema.load(syslog_schema_input_type_deviances, many=True,
                    partial=partial)


@pytest.fixture
def syslog_schema_input_type_attack():
    return [{
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


def test_syslog_schema_input_type_attack(
        syslog_schema_input_type_attack):
    '''
    test syslog schema with create payload and input type as attacks
    '''
    test_resp = [{
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

    schema = SyslogSchema()
    partial = ('checkers',)
    req = schema.dump(
        schema.load(syslog_schema_input_type_attack, many=True,
                    partial=partial), many=True)
    assert test_resp[0]['criticity_threshold'] == req[0]['criticityThreshold']
    assert test_resp[0]['directories'] == req[0]['directories']
    assert test_resp[0]['description'] == req[0]['description']
    assert test_resp[0]['attack_types'] == req[0]['attackTypes']
    assert test_resp[0]['profiles'] == req[0]['profiles']
    assert test_resp[0]['filter_expression'] == req[0]['filterExpression']
    assert test_resp[0]['port'] == req[0]['port']
    assert test_resp[0]['ip'] == req[0]['ip']
    assert test_resp[0]['protocol'] == req[0]['protocol']
    assert test_resp[0]['tls'] == req[0]['tls']

    with pytest.raises(ValidationError):
        syslog_schema_input_type_attack[0]['some_val'] = 'something'
        schema.load(syslog_schema_input_type_attack, many=True,
                    partial=partial)


@pytest.fixture
def syslog_schema_input_type_ad_object_changes():
    return [{
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
        'should_notify_on_initial_full_security_check': True,
        'tls': False
    }]


def test_syslog_schema_input_type_ad_object_changes(
        syslog_schema_input_type_ad_object_changes):
    '''
    test syslog schema with create payload and input type as adObjectChanges
    '''
    test_resp = [{
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
        'should_notify_on_initial_full_security_check': True,
        'tls': False
    }]
    schema = SyslogSchema()
    partial = ('attack_types', 'checkers', 'profiles',)
    req = schema.dump(
        schema.load(syslog_schema_input_type_ad_object_changes, many=True,
                    partial=partial), many=True)
    assert test_resp[0]['criticity_threshold'] == req[0]['criticityThreshold']
    assert test_resp[0]['directories'] == req[0]['directories']
    assert test_resp[0]['description'] == req[0]['description']
    assert test_resp[0]['attack_types'] == req[0]['attackTypes']
    assert test_resp[0]['profiles'] == req[0]['profiles']
    assert test_resp[0]['filter_expression'] == req[0]['filterExpression']
    assert test_resp[0]['port'] == req[0]['port']
    assert test_resp[0]['ip'] == req[0]['ip']
    assert test_resp[0]['protocol'] == req[0]['protocol']
    assert test_resp[0]['tls'] == req[0]['tls']

    with pytest.raises(ValidationError):
        syslog_schema_input_type_ad_object_changes[0]['some_val'] = 'something'
        schema.load(syslog_schema_input_type_ad_object_changes, many=True,
                    partial=partial)


def test_syslog_schema_directories_validation_error():
    '''
    test to raise exception when blank list is provided in directories.
    '''
    with pytest.raises(ValidationError):
        req = [{
            'attack_types': None,
            'checkers': None,
            'criticity_threshold': 0,
            'description': 'test_syslog',
            'directories': [],  # passing empty directories
            'filter_expression': {'OR': [{'systemOnly': 'True'}]},
            'id': 1,
            'input_type': 'adObjectChanges',
            'ip': '127.0.0.1',
            'port': 8888,
            'profiles': None,
            'protocol': 'TCP',
            'should_notify_on_initial_full_security_check': True,
            'tls': False
        }]
        schema = SyslogSchema()
        schema.load(req, many=True)


def test_syslog_schema_attack_types_validation_error():
    '''
    test to raise exception when blank list is provided in attack_types
    '''
    with pytest.raises(ValidationError):
        req = [{
            'attack_types': [],  # passing empty attack_types
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
        schema = SyslogSchema()
        schema.load(req, many=True)


def test_syslog_schema_checkers_validation_error():
    '''
    test to raise exception when blank list is provided in checkers
    '''
    with pytest.raises(ValidationError):
        req = [{
            'attack_types': None,
            'checkers': [],  # passing empty checkers
            'criticity_threshold': 55,
            'description': 'test_syslog',
            'directories': [1],
            'filter_expression': {'OR': [{'systemOnly': 'True'}]},
            'id': 1,
            'input_type': 'deviances',
            'ip': '127.0.0.1',
            'port': 514,
            'profiles': [1],
            'protocol': 'TCP',
            'should_notify_on_initial_full_security_check': False,
            'tls': True
        }]
        schema = SyslogSchema()
        schema.load(req, many=True)


def test_syslog_schema_profiles_validation_error():
    '''
    test to raise exception when blank list is provided in profiles
    '''
    with pytest.raises(ValidationError):
        req = [{
            'attack_types': None,
            'checkers': [1],
            'criticity_threshold': 55,
            'description': 'test_syslog',
            'directories': [1],
            'filter_expression': {'OR': [{'systemOnly': 'True'}]},
            'id': 1,
            'input_type': 'deviances',
            'ip': '127.0.0.1',
            'port': 514,
            'profiles': [],  # passing empty profiles
            'protocol': 'TCP',
            'should_notify_on_initial_full_security_check': False,
            'tls': True
        }]
        schema = SyslogSchema()
        schema.load(req, many=True)


def test_syslog_schema_input_type_validation_error():
    '''
    test to raise exception when input_type doesn't match the expected values
    '''
    with pytest.raises(ValidationError):
        req = [{
            'attack_types': None,
            'checkers': [],
            'criticity_threshold': 55,
            'description': 'test_syslog',
            'directories': [1],
            'filter_expression': {'OR': [{'systemOnly': 'True'}]},
            'id': 1,
            'input_type': 'something',  # invalid input_type
            'ip': '127.0.0.1',
            'port': 514,
            'profiles': [1],
            'protocol': 'TCP',
            'should_notify_on_initial_full_security_check': False,
            'tls': True
        }]
        schema = SyslogSchema()
        schema.load(req, many=True)
