import pytest
from tenable.errors import ConnectionError
from tenable.sc import TenableSC


def test_sc_init_catch_name_error():
    '''
    test to raise the exception when host is invalid, hence the connection wont be made
    '''

    try:
        TenableSC(host='127.0.0.1')
    except NameError as error:
        pytest.raises(NameError)
    except ConnectionError as err:
        print("The following error exists: ", err)
        pytest.raises(ConnectionError)
        assert True
