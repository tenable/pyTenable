'''
Testing the lockout policy schemas
'''
import pytest
from tenable.ie.lockout_policy.schema import LockoutPolicySchema


@pytest.fixture()
def lockout_policy_schema():
    return {
        'enabled': True,
        'lockout_duration': 10,
        'failed_attempt_threshold': 2,
        'failed_attempt_period': 1
    }


def test_lockout_policy_schema(lockout_policy_schema):
    '''
    test lockout policy update payload input to schema
    '''
    schema = LockoutPolicySchema()
    req = schema.dump(schema.load(lockout_policy_schema))
    assert req['enabled'] is True
    assert req['lockoutDuration'] == 10
    assert req['failedAttemptThreshold'] == 2
    assert req['failedAttemptPeriod'] == 1
