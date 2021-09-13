'''
test pages
'''
import pytest
import six

from ..checker import check
from tests.downloads.conftest import dl as download


@pytest.mark.vcr()
def test_pages_list_success(download):
    '''test to list the pages'''
    pages = download.pages.list()
    assert isinstance(pages, list)
    for page in pages:
        check(page, 'description', str)
        check(page, 'files_index_url', str)
        check(page, 'page_slug', str)
        check(page, 'title', str)


@pytest.mark.vcr()
def test_pages_detail_success(download):
    '''test to get the page details'''
    detail = download.pages.details('nessus')
    assert isinstance(detail, dict)
    check(detail, 'releases', dict)
    for key, value in list(detail['releases'].items()) if six.PY3 else detail['releases'].items():
        assert isinstance(value, (list, dict))
        # For regular releases
        if isinstance(value, list):
            for data in value:
                assert isinstance(data, dict)
                check(data, 'file', str)
                check(data, 'file_url', str)
                check(data, 'product_release_date', str)
                check(data, 'sha256', str)
                check(data, 'md5', str)
                check(data, 'release_date', str)
                check(data, 'size', int)

        # for the latest release
        if isinstance(value, dict):
            for key, val in list(value.items()) if six.PY3 else value.items():
                for data in val:
                    assert isinstance(data, dict)
                    check(data, 'file', str)
                    check(data, 'file_url', str)
                    check(data, 'product_release_date', str)
                    check(data, 'sha256', str)
                    check(data, 'md5', str)
                    check(data, 'release_date', str)
                    check(data, 'size', int)

    check(detail, 'signing_keys', list)
    for data in detail['signing_keys']:
        check(data, 'file', str)
        check(data, 'file_url', str)
        check(data, 'md5', str)
        check(data, 'sha256', str)
        check(data, 'size', int)


@pytest.mark.vcr()
@pytest.mark.skip(reason='Large File download')
def test_pages_download_success(download):
    '''test to download the pages'''
    with open('Nessus.deb', 'wb') as fobj:
        download.pages.download('nessus', 'Nessus-latest-debian6_amd64.deb', fobj)
