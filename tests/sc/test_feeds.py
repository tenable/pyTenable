import os
import pytest
from ..checker import check
from tenable.errors import UnexpectedValueError


def test_feeds_feed_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.feeds.status(1)


def test_feeds_feed_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.feeds.status('something else')


@pytest.mark.vcr()
def test_feeds_success(sc):
    feed = sc.feeds.status()
    assert isinstance(feed, dict)
    for key in feed.keys():
        check(feed[key], 'updateTime', str)
        check(feed[key], 'stale', str)
        check(feed[key], 'updateRunning', str)


@pytest.mark.vcr()
def test_feeds_individual_success(sc):
    feed = sc.feeds.status('active')
    assert isinstance(feed, dict)
    check(feed, 'updateTime', str)
    check(feed, 'stale', str)
    check(feed, 'updateRunning', str)


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
