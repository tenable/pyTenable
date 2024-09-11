'''
Base platform Testing module.
'''
import os
import pytest
import responses
from tenable.base.platform import APIPlatform


def test_url_constructor():
    '''
    Test the URL constructor.
    '''
    # test invalid URL
    with pytest.raises(ConnectionError):
        APIPlatform(url='something')


@responses.activate
def test_authentication():
    '''
    Test APIPlatform authentication methods.
    '''
    # Check that api key auth worked as expected
    api = APIPlatform(access_key='1',
                      secret_key='2',
                      url='https://localhost'
                      )
    assert api._session.headers.get('x-apikeys') == 'accessKey=1; secretKey=2'  # noqa: PLW0212,E501
    assert api._auth_mech == 'keys'  # noqa: PLW0212

    responses.add(responses.POST, 'https://localhost/session')
    responses.add(responses.DELETE, 'https://localhost/session')

    # Check that session auth worked as expected.
    os.unsetenv('_USERNAME')
    os.unsetenv('_PASSWORD')
    api = APIPlatform(username='user',
                      password='pass',
                      url='https://localhost'
                      )
    assert api._auth_mech == 'session'  # noqa: PLW0212

    # Check to ensure that API Keys are preferred over session auth.
    api = APIPlatform(access_key='1',
                      secret_key='2',
                      username='user',
                      password='password',
                      url='https://localhost'
                      )
    assert api._session.headers.get('x-apikeys') == 'accessKey=1; secretKey=2'  # noqa: PLW0212,E501
    assert api._auth_mech == 'keys'  # noqa: PLW0212

    # Test deauthentication.
    api._deauthenticate()  # noqa: PLW0212
    assert api._auth_mech is None  # noqa: PLW0212


@responses.activate
def test_camel_squashing():
    '''
    Test camelcase squashing capabilities within Box.
    '''
    responses.add(
        method='GET',
        url='https://localhost/example',
        json={'id': 1, 'camelCase': 'passed'}
    )
    api1 = APIPlatform(url='https://localhost',
                       access_key='1',
                       secret_key='2',
                       box=True
                       )
    api2 = APIPlatform(url='https://localhost',
                       access_key='1',
                       secret_key='2',
                       squash_camel=True,
                       box=True
                       )
    assert api1.get('example').camelCase == api2.get('example').camel_case
