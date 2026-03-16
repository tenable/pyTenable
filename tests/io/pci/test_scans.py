import pytest
import responses
from responses.matchers import query_param_matcher

from tenable.io.pci.iterators import PCIScansIterator


@pytest.fixture
def scan_list():
    return {
        'pagination': {
            'total': 2,
            'offset': 0,
            'limit': 200,
            'sort': [{'name': 'name', 'order': 'asc'}],
        },
        'scans': [
            {
                'asset_count': 4,
                'updated_at': '2023-01-13T08:30:03.219Z',
                'name': 'PCI Scan Example 1',
                'cde.uuid': '2a26c398-d61f-4f0f-8aea-bce410a64818',
                'started_at': '2023-01-13T05:30:12Z',
                'scan_type': 'nessus',
                'failure_count': 68,
                'import_status': 'complete',
                'vulnerability_count': 229,
                'uuid': '1ud20a81-5dbf-4749-9173-62ba398c0646',
                'ended_at': '2023-01-13T05:50:03Z',
                'status': 100,
            },
            {
                'asset_count': 4,
                'updated_at': '2023-01-13T08:30:03.219Z',
                'name': 'PCI Scan Example 2',
                'cde.uuid': '1a26c398-d61f-4f0f-8aea-bce410a64818',
                'started_at': '2023-01-13T05:30:12Z',
                'scan_type': 'nessus',
                'failure_count': 68,
                'import_status': 'complete',
                'vulnerability_count': 229,
                'uuid': 'bu7e71d6-25db-44a1-8869-f7b234480c11',
                'ended_at': '2023-01-13T05:50:03Z',
                'status': 100,
            },
        ],
    }


def test_scans_format_sorts(tvm):
    assert tvm.pci.scans._format_sorts([('a', 'desc'), ('b', 'asc')]) == 'a:desc,b:asc'


@responses.activate
def test_scans_iterator_response(tvm, scan_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/scans/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=scan_list,
    )
    resp = tvm.pci.scans.list()
    assert isinstance(resp, PCIScansIterator)

    item = next(resp)
    assert item == scan_list['scans'][0]

    item = next(resp)
    assert item == scan_list['scans'][1]

    with pytest.raises(StopIteration):
        next(resp)

    assert resp.total == 2
    assert resp.count == 2


@responses.activate
def test_scans_no_iterator(tvm, scan_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/scans/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=scan_list,
    )
    resp = tvm.pci.scans.list(iterator=None)
    assert isinstance(resp, dict)
    assert len(resp['scans']) == 2
