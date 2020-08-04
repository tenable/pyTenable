from tenable.base.platform import APIPlatform
import pytest, responses

def test_url_constructor():
    # Test all params
    api = APIPlatform(scheme='https', address='localhost', port=8080)
    assert api._url == 'https://localhost:8080'

    # tests only 1 param
    api = APIPlatform(address='localhost')
    assert api._url == 'https://localhost:443'

    # test invalid URL
    with pytest.raises(TypeError):
        api = APIPlatform(scheme='')


@responses.activate
def test_authentication():
    api = APIPlatform(access_key='1', secret_key='2', address='localhost')
    assert api._session.headers.get('x-apikeys') == 'accessKey=1; secretKey=2'
    assert api._auth_mech == 'keys'

    responses.add(responses.POST, 'https://localhost:443/session')
    responses.add(responses.DELETE, 'https://localhost:443/session')

    api = APIPlatform(username='user', password='pass', address='localhost')
    assert api._auth_mech == 'user'
    assert api._auth == ('user', 'pass')

    api._deauthenticate()
    assert api._auth_mech == None
    assert api._auth == (None, None)

@responses.activate
def test_camel_squashing():
    responses.add(
        method='GET',
        url='https://localhost:443/example',
        json={'id': 1, 'annoyingResponse': 'passed'}
    )
    api1 = APIPlatform(address='localhost')
    api2 = APIPlatform(address='localhost', squash_camel=True)
    assert api1.get('example').annoyingResponse == api2.get('example').annoying_response
