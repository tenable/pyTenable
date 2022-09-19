'''
test file for testing various scenarios in feeds
'''
import os

import pytest

from tenable.errors import UnexpectedValueError
from ..checker import check


def test_feeds_feed_type_typeerror(security_center):
    '''
    test feeds feed type for type error
    '''
    with pytest.raises(TypeError):
        security_center.feeds.status(1)


def test_feeds_feed_type_unexpectedvalueerror(security_center):
    '''
    test feeds feed type for unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.feeds.status('something else')


@pytest.mark.vcr()
def test_feeds_success(security_center):
    '''
    test feeds for success
    '''
    feed = security_center.feeds.status()
    assert isinstance(feed, dict)
    for key in feed.keys():
        check(feed[key], 'updateTime', str)
        check(feed[key], 'stale', str)
        check(feed[key], 'updateRunning', str)


@pytest.mark.vcr()
def test_feeds_individual_success(security_center):
    '''
    test feeds individual for success
    '''
    feed = security_center.feeds.status('active')
    assert isinstance(feed, dict)
    check(feed, 'updateTime', str)
    check(feed, 'stale', str)
    check(feed, 'updateRunning', str)


def test_feeds_update_feed_type_typeerror(security_center):
    '''
    test feeds 'update feed type' for type error
    '''
    with pytest.raises(TypeError):
        security_center.feeds.update(1)


def test_feeds_update_feed_type_unexpectedvalueerror(security_center):
    '''
    test feeds 'update feed type' for unexpected value
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.feeds.update('somethign else')


@pytest.mark.vcr()
def test_feeds_update_success(security_center):
    '''
    test feeds 'update' for success
    '''
    security_center.feeds.update('active')


@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'SecurityCenterFeed48.tar.gz'))
def test_feeds_process_success(admin, datafiles, security_center):
    '''
    test feeds 'process' for success
    '''
    with open(os.path.join(str(datafiles), 'SecurityCenterFeed48.tar.gz'), 'rb') as plugfeed:
        security_center.feeds.process('active', plugfeed)
