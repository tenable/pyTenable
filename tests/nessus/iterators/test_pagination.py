import pytest
import responses
from tenable.nessus.iterators.pagination import PaginationIterator


@responses.activate
def test_pagination_iterator(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/page',
                  json={'envelope': [{'id': i} for i in range(100)]}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/page',
                  json={'envelope': [{'id': i + 100} for i in range(100)]}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/page',
                  json={'envelope': [{'id': i + 200} for i in range(92)]}
                  )
    iter = PaginationIterator(nessus,
                              path='page',
                              envelope='envelope',
                              limit=100
                              )
    total = 0
    for item in iter:
        assert item['id'] == total
        total += 1
    assert total == 292