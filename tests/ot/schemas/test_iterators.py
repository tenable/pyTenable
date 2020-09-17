from tenable.ot.schemas.iterators import OTIterator
import responses, pytest, re


@responses.activate
def test_iterator(ot):
    responses.add(
        method='POST',
        url='https://localhost:443/v1/iterator_test',
        json=['item1', 'item2', 'item3', 'item4', 'item5', 'item6']
    )

    # iterate through multiple pages
    items = OTIterator(ot, path='iterator_test', payload=dict(), limit=6, max_pages=3)
    for item in items:
        assert isinstance(item, str)
    assert items.count == 18
    assert items.num_pages == 3

    # insure that the iterator will bail when the limit is larger than the page.
    items = OTIterator(ot, path='iterator_test', payload=dict(), max_pages=3)
    for item in items:
        assert isinstance(item, str)
    assert items.count == 6
    assert items.num_pages == 1