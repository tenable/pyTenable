"""
test file for testing various scenarios in feeds
"""

import os

import pytest
import responses

from tenable.errors import UnexpectedValueError
from ..checker import check


def test_feeds_feed_type_typeerror(tsc):
    """
    test feeds feed type for type error
    """
    with pytest.raises(TypeError):
        tsc.feeds.status(1)


def test_feeds_feed_type_unexpectedvalueerror(tsc):
    """
    test feeds feed type for unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.feeds.status('something else')


@responses.activate
def test_feeds_success(tsc):
    """
    test feeds for success
    """
    responses.get(
        'https://nourl/rest/feed',
        json={
            'type': 'regular',
            'response': {
                'sc': {
                    'updateTime': '1553231422',
                    'stale': 'false',
                    'updateRunning': 'false',
                    'subscriptionStatus': 'Valid',
                },
                'active': {
                    'updateTime': '1553156153',
                    'stale': 'false',
                    'updateRunning': 'false',
                    'subscriptionStatus': 'Valid',
                },
                'passive': {
                    'updateTime': '1553234416',
                    'stale': 'false',
                    'updateRunning': 'false',
                    'subscriptionStatus': 'Valid',
                },
                'lce': {
                    'updateTime': '1550205301',
                    'stale': 'true',
                    'updateRunning': 'false',
                    'subscriptionStatus': 'Expired',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553279040,
        },
    )
    feed = tsc.feeds.status()
    assert isinstance(feed, dict)
    for key in feed.keys():
        check(feed[key], 'updateTime', str)
        check(feed[key], 'stale', str)
        check(feed[key], 'updateRunning', str)


@responses.activate
def test_feeds_individual_success(tsc):
    """
    test feeds individual for success
    """
    responses.get(
        'https://nourl/rest/feed/active',
        json={
            'type': 'regular',
            'response': {
                'updateTime': '1553156153',
                'stale': 'false',
                'subscriptionStatus': 'Valid',
                'updateRunning': 'true',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553279111,
        },
    )
    feed = tsc.feeds.status('active')
    assert isinstance(feed, dict)
    check(feed, 'updateTime', str)
    check(feed, 'stale', str)
    check(feed, 'updateRunning', str)


def test_feeds_update_feed_type_typeerror(tsc):
    """
    test feeds 'update feed type' for type error
    """
    with pytest.raises(TypeError):
        tsc.feeds.update(1)


def test_feeds_update_feed_type_unexpectedvalueerror(tsc):
    """
    test feeds 'update feed type' for unexpected value
    """
    with pytest.raises(UnexpectedValueError):
        tsc.feeds.update('somethign else')


@responses.activate
def test_feeds_update_success(tsc):
    """
    test feeds 'update' for success
    """
    responses.post(
        'https://nourl/rest/feed/active/update',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1553279040,
        },
    )
    tsc.feeds.update('active')


@pytest.mark.datafiles(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'test_files',
        'SecurityCenterFeed48.tar.gz',
    )
)
@responses.activate
def test_feeds_process_success(tsc, datafiles):
    """
    test feeds 'process' for success
    """
    responses.post(
        'https://nourl/rest/file/upload',
        json={
            'type': 'regular',
            'response': {
                'filename': 'UjhU7F',
                'originalFilename': 'SecurityCenterFeed48.tar.gz',
                'content': '',
                'context': '',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1654072950,
        },
    )
    responses.post(
        'https://nourl/rest/feed/active/process',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1654072951,
        },
    )
    with open(
        os.path.join(str(datafiles), 'SecurityCenterFeed48.tar.gz'), 'rb'
    ) as plugfeed:
        tsc.feeds.process('active', plugfeed)
