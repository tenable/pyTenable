
import pytest
from tenable.nessus import Nessus


@pytest.fixture
def nessus():
    return Nessus(url='https://localhost:8834',
                  access_key='access_key',
                  secret_key='secret_key'
                  )