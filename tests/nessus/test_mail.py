import pytest
import responses


MAIL = {
    'smtp_host': 'smtp.company.com',
    'smtp_port': 25,
    'smtp_from': 'no-reply@company.com',
    'smtp_www_host': 'https://nessus.company.com',
    'smtp_auth': 'LOGIN',
    'smtp_user': 'report-user',
    'smtp_pass': 's3kr3tsqu1rr3l',
    'smtp_enc': 'No Encryption'
}


@responses.activate
def test_mail_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/settings/network/mail',
                  json=MAIL
                  )
    resp = nessus.mail.details()
    assert resp == MAIL


@responses.activate
def test_mail_edit(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/settings/network/mail',
                  json=MAIL
                  )
    responses.add(responses.PUT,
                  'https://localhost:8834/settings/network/mail'
                  )
    nessus.mail.edit(smtp_user='new_user',
                     smtp_pass='updated_password',
                     smtp_auth='LOGIN',
                     )