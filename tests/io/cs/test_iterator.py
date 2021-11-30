'''
Testing the CS iterator
'''
import re
import pytest
import responses
from tenable.io.cs.iterator import CSIterator


@responses.activate
def test_cs_iterator(api):
    responses.add(responses.GET,
                  'https://cloud.tenable.com/iter',
                  json={
                      'pagination': {
                          'total': 100,
                      },
                      'items': [
                          {'id': 1, 'name': 'One'},
                          {'id': 2, 'name': 'Two'},
                          {'id': 3, 'name': 'Three'},
                          {'id': 4, 'name': 'Four'},
                          {'id': 5, 'name': 'Five'}
                      ]
                  })
    iterator = CSIterator(api,
                          _path='iter',
                          _params={},
                          _limit=5
                          )
    counter = 0
    for item in iterator:
        counter += 1
        assert isinstance(item['name'], str)
    assert iterator.total == counter
