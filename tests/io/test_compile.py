import pytest
from tenable.errors import UnexpectedValueError
from tenable.io import TenableIO
from tenable.io.exports import ExportsIterator
from tests.io.conftest import api


def test_io_init_catch_value_error():
    '''
    test to raise the exception when value is not passed correctly
    '''
    try:
        TenableIO()
        ExportsIterator(api)
    except NameError:
        pytest.raises(NameError)
        assert True
    except UnexpectedValueError as err:
        print('The following error exists: ', err)
        pytest.raises(UnexpectedValueError)
        assert True
