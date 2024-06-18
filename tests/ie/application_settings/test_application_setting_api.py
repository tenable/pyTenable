import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_application_settings_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/application-settings',
                  json={
                      'default_profile_id': 1,
                      'default_role_ids': [2],
                      'email_sender': 'default@tenable.ad',
                      'internal_certificate': None,
                      'keep_audit_log': True,
                      'log_retention_period': 365,
                      'smtp_account': None,
                      'smtp_account_password': None,
                      'smtp_server_address': None,
                      'smtp_server_port': None,
                      'smtp_use_start_tls': True,
                      'tls': False,
                      'user_registration': False
                  }
                  )
    resp = api.application_settings.details()
    assert isinstance(resp, dict)
    assert resp['default_profile_id'] == 1
    assert resp['log_retention_period'] == 365
    assert resp['smtp_use_start_tls'] is True


@responses.activate
def test_application_settings_update(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/application-settings',
                  json={
                      'default_profile_id': 1,
                      'default_role_ids': [2],
                      'email_sender': 'default@tenable.ad',
                      'internal_certificate': None,
                      'keep_audit_log': True,
                      'log_retention_period': 300,
                      'smtp_account': None,
                      'smtp_account_password': None,
                      'smtp_server_address': None,
                      'smtp_server_port': None,
                      'smtp_use_start_tls': False,
                      'tls': False,
                      'user_registration': False
                  }
                  )
    resp = api.application_settings.update(
        smtp_use_start_tls=False,
    )
    assert isinstance(resp, dict)
    assert resp['default_profile_id'] == 1
    assert resp['smtp_use_start_tls'] is False
