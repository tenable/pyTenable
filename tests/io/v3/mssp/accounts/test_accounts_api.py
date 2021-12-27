import pytest
import responses


@responses.activate
def test_search(api):
    '''
    Test mssp accounts search method
    '''
    with pytest.raises(NotImplementedError):
        api.v3.vm.folders.search()
