import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_api_keys_get(api):
    '''
    tests the api-key of the Tenable ad instance.
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/api-key',
                  json={'key': 'something'}

                  )
    resp = api.api_keys.get()
    print(resp)
    assert isinstance(resp, str)
    assert resp == 'something'


@responses.activate
def test_api_keys_renew(api):
    '''
    tests the code to refresh or renew or create the api key.

    Returns:
        str
    '''
    responses.add(responses.POST,
                  f'{RE_BASE}/api-key',
                  json={'key': 'new_api_key'})
    resp = api.api_keys.refresh()
    assert isinstance(resp, str)
    assert resp == 'new_api_key'
