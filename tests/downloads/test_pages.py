from tenable.errors import *
from ..checker import check
import datetime, sys, pytest, os

@pytest.mark.vcr()
def test_pages_list_success(dl):
    pages = dl.pages.list()
    assert isinstance(pages, list)
    for p in pages:
        check(p, 'description', str)
        check(p, 'files_index_url', str)
        check(p, 'page_slug', str)
        check(p, 'title', str)

@pytest.mark.vcr()
def test_pages_detail_success(dl):
    p = dl.pages.details('nessus')
    assert isinstance(p, dict)
    check(p, 'releases', dict)
    for k, v in p['releases'].items():
        assert isinstance(v, (list, dict))
        # For regular releases
        if isinstance(v, list):
            for i in v:
                assert isinstance(i, dict)
                check(i, 'file', str)
                check(i, 'file_url', str)
                check(i, 'product_release_date', str)
                check(i, 'sha256', str)
                check(i, 'md5', str)
                check(i, 'release_date', str)
                check(i, 'size', int)
        
        # for the latest release
        if isinstance(v, dict):
            for k, j in v.items():
                for i in j:
                    assert isinstance(i, dict)
                    check(i, 'file', str)
                    check(i, 'file_url', str)
                    check(i, 'product_release_date', str)
                    check(i, 'sha256', str)
                    check(i, 'md5', str)
                    check(i, 'release_date', str)
                    check(i, 'size', int)
    
    check(p, 'signing_keys', list)
    for i in p['signing_keys']:
        check(i, 'file', str)
        check(i, 'file_url', str)
        check(i, 'md5', str)
        check(i, 'sha256', str)
        check(i, 'size', int)

@pytest.mark.vcr()
@pytest.mark.skip(reason='Large File download')
def test_pages_download_success(dl):
    with open('Nessus.deb', 'wb') as fobj:
        dl.pages.download('nessus', 'Nessus-latest-debian6_amd64.deb', fobj)
    