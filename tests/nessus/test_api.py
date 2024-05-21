import pytest
import responses
from tenable.nessus import Nessus
from tenable.errors import AuthenticationWarning


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