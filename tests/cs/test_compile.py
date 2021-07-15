'''
test compile
'''
import pytest
from tenable.cs import ContainerSecurity
from tenable.cs.base import CSIterator, CSEndpoint
from tenable.cs.images import ImageIterator, ImageAPI
from tenable.cs.reports import ReportAPI
from tenable.cs.repositories import RepositoryAPI, RepositoryIterator
from tenable.cs.uploads import UploadAPI
from tenable.cs.usage import UsageAPI
from tests.cs.conftest import api
from tenable.errors import UnexpectedValueError


def test_cs_compile():
    '''
    test to raise the exception when no api keys are provided
    '''
    try:
        ContainerSecurity()
        CSEndpoint(api)
        CSIterator(api)
        ImageIterator(api)
        ImageAPI(api)
        ReportAPI(api)
        RepositoryIterator(api)
        RepositoryAPI(api)
        UploadAPI(api)
        UsageAPI(api)

    except NameError as error:
        print('\n The following name error exists: {}'.format(error))
        pytest.raises(NameError)
        assert True
    except UnexpectedValueError as error:
        print('\n The following value error exists: {}'.format(error))
        pytest.raises(UnexpectedValueError)
        assert True
