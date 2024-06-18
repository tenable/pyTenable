'''
Testing the application setting schema
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.application_settings.schema import ApplicationSettingsSchema


@pytest.fixture()
def application_setting_schema():
    return {
        'default_profile_id': 1,
        'default_role_ids': [2],
        'email_sender': 'default@tenable.ad',
        'internal_certificate': None,
        'smtp_account': None,
        'smtp_account_password': None,
        'smtp_server_address': None,
        'smtp_server_port': None,
        'smtp_use_start_tls': False,
        'tls': False
    }


def test_application_setting_schema(application_setting_schema):
    '''
    test application setting schema
    '''
    test_resp = {
        'defaultProfileId': 1,
        'defaultRoleIds': [2],
        'emailSender': 'default@tenable.ad',
        'internalCertificate': None,
        'keepAuditLog': True,
        'logRetentionPeriod': 300,
        'smtpAccount': None,
        'smtpAccountPassword': None,
        'smtpServerAddress': None,
        'smtpServerPort': None,
        'smtpUseStartTLS': False,
        'tls': False,
        'userRegistration': False
    }

    schema = ApplicationSettingsSchema()
    req = schema.dump(schema.load(application_setting_schema))
    assert test_resp['defaultProfileId'] == req['defaultProfileId']
    assert test_resp['emailSender'] == req['emailSender']
    assert test_resp['smtpUseStartTLS'] == req['smtpUseStartTLS']

    with pytest.raises(ValidationError):
        application_setting_schema['some_val'] = 'something'
        schema.load(application_setting_schema)
