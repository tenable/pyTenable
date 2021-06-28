'''
test compile
'''
import pytest
from tenable.errors import UnexpectedValueError
from tenable.cs import ContainerSecurity


def test_cs_init_catch_name_error():
    '''
    test to raise the exception when no api keys are provided
    '''
    try:
        ContainerSecurity()
    except NameError as error:
        print('\n', 'The following error exists-\n', error)
        pytest.raises(NameError)
        assert True
    except UnexpectedValueError:
        pytest.raises(UnexpectedValueError)
