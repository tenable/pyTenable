import responses
from tenable.nessus import Nessus


@responses.activate
def test_session_authentication():
    '''
    test to raise the exception unauthorized session is created
    '''
    responses.add(responses.POST,
                  'https://localhost:8834/session',
                  json={'token': 'EXAMPLE TOKEN'}
                  )
    mock = Nessus(url='https://localhost:8834',
                  username='username',
                  password='password'
                  )

@responses.activate
def test_session_logout_deletes_session():
    '''
    Session-based auth must send DELETE /session when the session is closed.
    '''
    responses.post('https://localhost:8834/session', json={'token': 'TOKEN'})
    logout = responses.delete('https://localhost:8834/session')
    with Nessus(url='https://localhost:8834',
                username='username',
                password='password'
                ) as nessus:
        assert nessus._auth_mech == 'session'
    assert logout.call_count == 1
    assert nessus._auth_mech is None
