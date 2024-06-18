import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_about(api):
    '''
    tests the version of the Tenable ad instance
    '''
    responses.add(responses.GET,
                  f'{RE_BASE}/about',
                  json={'version': 'some_version',
                        'hostname': 'hostname'}

                  )
    resp = api.about.version()
    assert isinstance(resp, str)
