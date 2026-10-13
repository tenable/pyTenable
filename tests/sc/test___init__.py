"""
test file to test various scenarios in init.py
"""

import pytest
import responses
from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.models import Response

from tenable.errors import ConnectionError
from tenable.sc import TenableSC


def test_init_connection_error():
    """
    test init for connection error
    """
    with pytest.raises(RequestsConnectionError):
        TenableSC(
            url='https://nothing-here.local',
            access_key='nope',
            secret_key='also-nope',
            vendor='pytest',
            product='pytenable-automated-testing',
            backoff=0,
            retries=0,
            timeout=1,
        )


def test_enter(tsc):
    """
    test enter
    """
    assert tsc == tsc.__enter__()


@responses.activate
def test_exit():
    """
    test exit
    """
    responses.post(
        'https://nourl/rest/token',
        json={'error_code': 0, 'response': {'token': 1234}},
        headers={'Set-Cookie': 'TNS_SESSIONID=0123456789abcdef0123456789abcdef'},
    )
    responses.get(
        'https://nourl/rest/system',
        json={'error_code': 0, 'response': {'version': '6.4.0'}},
    )
    logout = responses.delete(
        'https://nourl/rest/token', json={'error_code': 0, 'response': ''}
    )
    with pytest.warns(DeprecationWarning):
        tsc = TenableSC(url='https://nourl', username='user', password='pass')
    tsc.__exit__(
        exc_type='exc_type', exc_value='exc_value', exc_traceback='exc_traceback'
    )
    assert logout.call_count == 1


def test_resp_error_check(tsc):
    """
    test response error check
    """
    with pytest.raises(AttributeError):
        response = Response()
        response._content = b'{ "error_code": 401}'
        tsc._resp_error_check(response)
    # pass
    response = Response()
    response._content = b'{ "error_code": 401, }'
    tsc._resp_error_check(response)


@pytest.mark.skip(reason='Deprecating this method')
def test_log_in():
    """
    test log in
    """
    tsc = TenableSC(url='https://localhost')
    tsc._version = '5.12.0'
    with pytest.raises(ConnectionError):
        tsc.login(access_key='access_key', secret_key='secret_key')

    tsc._version = '5.14.0'
    tsc.login(access_key='access_key', secret_key='secret_key')
    assert tsc._auth_mech == 'keys'

    tsc._version = None
    tsc._auth_mech = None
    with responses.RequestsMock() as rsps:
        rsps.get(
            'https://localhost/rest/system', json={'error_code': 0, 'response': ''}
        )
        tsc.login(access_key='access_key', secret_key='secret_key')
        assert tsc._auth_mech == 'keys'


def test_pkcs12_import_error():
    import tenable.sc

    tenable.sc.serialization = None
    with pytest.raises(ModuleNotFoundError):
        sc = TenableSC(
            url='http://something', p12_cert='something', password='something'
        )


@responses.activate
def test_session_logout_deletes_token():
    """
    Session-based auth must send DELETE /rest/token when the session is closed.
    """
    responses.post(
        'https://nourl/rest/token',
        json={'error_code': 0, 'response': {'token': 1234}},
        headers={'Set-Cookie': 'TNS_SESSIONID=0123456789abcdef0123456789abcdef'},
    )
    responses.get(
        'https://nourl/rest/system',
        json={'error_code': 0, 'response': {'version': '6.4.0'}},
    )
    logout = responses.delete(
        'https://nourl/rest/token', json={'error_code': 0, 'response': {}}
    )
    with pytest.warns(DeprecationWarning):
        tsc = TenableSC(url='https://nourl', username='user', password='pass')
    assert tsc._auth_mech == 'session'
    tsc.logout()
    assert logout.call_count == 1
    assert tsc._auth_mech is None
