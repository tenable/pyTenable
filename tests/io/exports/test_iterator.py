'''
Testing the exports iterator
'''
import re
import pytest
import responses
from box import Box
from tenable.errors import TioExportsError, TioExportsTimeout
from tenable.io.exports.iterator import ExportsIterator


URL_BASE = 'https://cloud.tenable.com/assets/export'
URL_ACTIONS = f'{URL_BASE}/([0-9a-fA-F\\-]+)'
URL_EXPORT = re.compile(URL_BASE)
URL_CANCEL = re.compile(f'{URL_ACTIONS}/cancel')
URL_STATUS = re.compile(f'{URL_ACTIONS}/status')
URL_CHUNK = re.compile(f'{URL_ACTIONS}/chunks/[0-9]+')


@pytest.fixture
def export_request():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, URL_EXPORT, json={
            'export_uuid': '01234567-89ab-cdef-0123-4567890abcde'
        })
        rsps.add(responses.GET, URL_STATUS, json={
            'status': 'PROCESSING',
            'chunks_available': []
        })
        rsps.add(responses.GET, URL_STATUS, json={
            'status': 'PROCESSING',
            'chunks_available': [1, 2, 5]
        })
        rsps.add(responses.GET, URL_STATUS, json={
            'status': 'FINISHED',
            'chunks_available': [1, 2, 3, 5]
        })
        rsps.add(responses.GET, URL_CHUNK, json=[
            {'name': 'item 1'},
            {'name': 'item 2'},
            {'name': 'item 3'},
            {'name': 'item 4'},
            {'name': 'item 5'}
        ])
        yield rsps


@responses.activate
def test_iterator_term_on_error(api):
    responses.add(responses.GET, URL_STATUS, json={'status': 'ERROR',
                                                   'chunks_available': []
                                                   })
    iterator = ExportsIterator(api,
                               type='assets',
                               uuid='01234567-89ab-cdef-0123-4567890abcde',
                               _term_on_error=True
                               )

    with pytest.raises(TioExportsError):
        iterator.next()


@responses.activate
def test_iterator_timeout(api):
    for _ in range(10):
        responses.add(responses.GET, URL_STATUS, json={'status': 'QUEUED',
                                                       'chunks_available': []
                                                       })
    responses.add(responses.POST, URL_CANCEL, json={'status': 'CANCELLED'})
    iterator = ExportsIterator(api,
                               type='assets',
                               uuid='01234567-89ab-cdef-0123-4567890abcde',
                               timeout=0
                               )

    with pytest.raises(TioExportsTimeout):
        iterator.next()


@responses.activate
def test_empty_chunk(api):
    responses.add(responses.GET, URL_STATUS, json={'status': 'FINISHED',
                                                   'chunks_available': [1, 2]
                                                   })
    responses.add(responses.GET, URL_CHUNK, json=[])
    export = ExportsIterator(api,
                             type='assets',
                             uuid='01234567-89ab-cdef-0123-4567890abcde',
                             )
    for _ in export:
        pass
    export.count == 0


def test_iterator_wait(export_request, api):
    export = api.exports.assets(when_done=True)
    assert export.uuid == '01234567-89ab-cdef-0123-4567890abcde'
    for item in export:
        if export.boxify:
            assert isinstance(item, Box)
            export.boxify = False
        else:
            assert isinstance(item, dict)
            export.boxify = True
    assert export.count == 20


def test_iterator_iterable(export_request, api):
    export = api.exports.assets()
    assert export.uuid == '01234567-89ab-cdef-0123-4567890abcde'
    for _ in export:
        pass
    assert export.count == 20


def test_iterator_context_errors(api):
    export = ExportsIterator(api,
         type='assets',
         uuid='01234567-89ab-cdef-0123-4567890abcde',
         )
    export._is_iterator = False
    with pytest.raises(TioExportsError):
        export.next()

    export._is_iterator = True
    def test_func(**kwargs):
        for item in kwargs['data']:
            pass

    with pytest.raises(TioExportsError):
        export.run_threaded(test_func)


def test_iterator_threaded(export_request, api):
    def test_func(data, **kwargs):
        counter = 0
        for item in data:
            counter += 1
        assert counter == 5

    export = api.exports.assets()
    export.run_threaded(test_func)
    assert len(export.processed) == 4
