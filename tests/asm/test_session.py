import os
import pytest
from tenable.asm import TenableASM
from tenable.errors import AuthenticationWarning


def test_asm_session_authentication():
    asm = TenableASM(url='http://nourl', api_key='abcdef')
    assert asm._session.headers['Authorization'] == 'abcdef'

    os.environ['TASM_API_KEY'] = 'efghi'
    asm = TenableASM(url='http://nourl')
    assert asm._session.headers['Authorization'] == 'efghi'

    os.environ.pop('TASM_API_KEY')
    with pytest.warns(AuthenticationWarning):
        asm = TenableASM(url='http://nourl')
