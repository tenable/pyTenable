import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_preference_details(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/preferences',
                  json={
                      'language': 'en',
                      'preferredProfileId': 1
                  }
                  )
    resp = api.preference.details()
    assert isinstance(resp, dict)
    assert resp['language'] == 'en'
    assert resp['preferred_profile_id'] == 1


@responses.activate
def test_preference_update(api):
    responses.add(responses.PATCH,
                  f'{RE_BASE}/preferences',
                  json={
                      'language': 'en',
                      'preferredProfileId': 2
                  })
    resp = api.preference.update(language='en',
                                  preferred_profile_id='2')
    assert isinstance(resp, dict)
    assert resp['language'] == 'en'
    assert resp['preferred_profile_id'] == 2
