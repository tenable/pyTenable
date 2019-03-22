from tenable.errors import *
from ..checker import check, single
import pytest, os

def test_feeds_feed_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.feeds.status(1)

def test_feeds_feed_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.feeds.status('something else')

@pytest.mark.vcr()
def test_feeds_success(sc):
    f = sc.feeds.status()
    assert isinstance(f, dict)
    for i in f.keys():
        check(f[i], 'updateTime', str)
        check(f[i], 'stale', str)
        check(f[i], 'updateRunning', str)

@pytest.mark.vcr()
def test_feeds_individual_success(sc):
    f = sc.feeds.status('active')
    assert isinstance(f, dict)
    check(f, 'updateTime', str)
    check(f, 'stale', str)
    check(f, 'updateRunning', str)

def test_feeds_update_feed_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.feeds.update(1)

def test_feeds_update_feed_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.feeds.update('somethign else')

@pytest.mark.vcr()
def test_feeds_update_success(sc):
    sc.feeds.update('active')

@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 
    '..', 'test_files', 'sc-plugins-diff.tar.gz'))
@pytest.mark.skip(reason='no plugin tarball to download')
def test_feeds_process_success(admin, datafiles):
    with open(os.path.join(str(datafiles), 'sc-plugins-diff.tar.gz'), 'rb') as plugfeed:
        admin.feeds.process('active', plugfeed)