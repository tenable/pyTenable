import pytest
import responses
from responses.matchers import query_param_matcher

from tenable.io.pci import iterators as i


@pytest.fixture
def att_list():
    return {
        'pagination': {
            'total': 2,
            'offset': 0,
            'limit': 200,
            'sort': [{'name': 'name', 'order': 'asc'}],
        },
        'attestations': [
            {
                'owner': 'example@example.com',
                'latest_comment': 'None',
                'submitted_at': '2021-02-12T10:27:21.988Z',
                'dispute_count': 0,
                'customer_uuid': '0010d632-4c24-4b71-9a4f-71416c375d47',
                'scan_completion_date': '2021-01-28T12:42:21Z',
                'created_at': '2021-02-12T10:25:48.267Z',
                'failure_count': 15,
                'created_by': 'example@example.com',
                'uuid': 'a13b1497-5fec-41be-a9d6-ffef794c304c',
                'asset_count': 1,
                'passed_dispute_count': 0,
                'undisputed_failure_count': 15,
                'scan_expiration_date': '2021-04-28T12:42:21Z',
                'updated_at': '2021-09-08T05:07:18.827Z',
                'contact': {
                    'contact_name': 'person',
                    'email': 'person@example.com',
                    'title': 'SW',
                    'phone_number': '123456789',
                    'company_name': 'Example, Inc.',
                    'company_url': 'example.com',
                    'city': 'San Jose',
                    'state': 'CA',
                    'zip_code': '95116',
                    'country': '',
                    'submitted_at': '2021-02-12T10:27:21.988Z',
                    'submitted_by_username': 'pci.test.0@tenable.com',
                    'submitted_by_id': '9b0aae86-71f8-40f0-bfd7-c5b7f16602a8',
                    'address_1': '1234 Main St.',
                    'address_2': '',
                },
                'updated_by': 'example@example.com',
                'name': 'PCI Attestation',
                'failed_dispute_count': 0,
                'cde.uuid': '4e533e20-bb69-d12d-9336-3ce52b679552',
                'company': 'company',
                'undetermined_dispute_count': 0,
                'excluded_asset_count': 0,
                'status': 'needs-work',
            },
            {
                'owner': 'example@example.com',
                'latest_comment': 'None',
                'submitted_at': '2021-02-12T10:27:21.988Z',
                'dispute_count': 0,
                'customer_uuid': '0010d632-4c24-4b71-9a4f-71416c375d47',
                'scan_completion_date': '2021-01-28T12:42:21Z',
                'created_at': '2021-02-12T10:25:48.267Z',
                'failure_count': 15,
                'created_by': 'example@example.com',
                'uuid': 'a13b1497-5fec-41be-a9d6-ffef794c304c',
                'asset_count': 1,
                'passed_dispute_count': 0,
                'undisputed_failure_count': 15,
                'scan_expiration_date': '2021-04-28T12:42:21Z',
                'updated_at': '2021-09-08T05:07:18.827Z',
                'contact': {
                    'contact_name': 'person',
                    'email': 'person@example.com',
                    'title': 'SW',
                    'phone_number': '123456789',
                    'company_name': 'Example, Inc.',
                    'company_url': 'example.com',
                    'city': 'San Jose',
                    'state': 'CA',
                    'zip_code': '95116',
                    'country': '',
                    'submitted_at': '2021-02-12T10:27:21.988Z',
                    'submitted_by_username': 'pci.test.0@tenable.com',
                    'submitted_by_id': '9b0aae86-71f8-40f0-bfd7-c5b7f16602a8',
                    'address_1': '1234 Main St.',
                    'address_2': '',
                },
                'updated_by': 'example@example.com',
                'name': 'PCI Attestation',
                'failed_dispute_count': 0,
                'cde.uuid': '4e533e20-bb69-d12d-9336-3ce52b679552',
                'company': 'company',
                'undetermined_dispute_count': 0,
                'excluded_asset_count': 0,
                'status': 'needs-work',
            },
        ],
    }


@pytest.fixture
def att_dets():
    return {
        'owner': 'example@example.com',
        'latest_comment': 'None',
        'submitted_at': '2021-02-12T10:27:21.988Z',
        'dispute_count': 0,
        'customer_uuid': '0010d632-4c24-4b71-9a4f-71416c375d47',
        'scan_completion_date': '2021-01-28T12:42:21Z',
        'created_at': '2021-02-12T10:25:48.267Z',
        'failure_count': 15,
        'created_by': 'example@example.com',
        'uuid': 'a13b1497-5fec-41be-a9d6-ffef794c304c',
        'asset_count': 1,
        'passed_dispute_count': 0,
        'undisputed_failure_count': 15,
        'scan_expiration_date': '2021-04-28T12:42:21Z',
        'updated_at': '2021-09-08T05:07:18.827Z',
        'contact': {
            'contact_name': 'person',
            'email': 'person@example.com',
            'title': 'SW',
            'phone_number': '123456789',
            'company_name': 'Example, Inc.',
            'company_url': 'example.com',
            'city': 'San Jose',
            'state': 'CA',
            'zip_code': '95116',
            'country': '',
            'submitted_at': '2021-02-12T10:27:21.988Z',
            'submitted_by_username': 'pci.test.0@tenable.com',
            'submitted_by_id': '9b0aae86-71f8-40f0-bfd7-c5b7f16602a8',
            'address_1': '1234 Main St.',
            'address_2': '',
        },
        'updated_by': 'example@example.com',
        'name': 'PCI Attestation',
        'failed_dispute_count': 0,
        'cde.uuid': '4e533e20-bb69-d12d-9336-3ce52b679552',
        'company': 'company',
        'undetermined_dispute_count': 0,
        'excluded_asset_count': 0,
        'status': 'needs-work',
    }


@pytest.fixture
def disp_list():
    return {
        'pagination': {
            'total': 17,
            'offset': 0,
            'limit': 2,
            'sort': [{'name': 'created_at', 'order': 'desc'}],
        },
        'disputes': [
            {
                'severity': 2,
                'owner': 'pci-testing@example.com',
                'reason': 'false-positive',
                'plugin_id': 106230,
                'latest_comment': 'None',
                'customer_uuid': '196d99ba-7f93-4945-be6c-1a6089b36a7c',
                'created_at': '2021-09-15T12:20:45.19Z',
                'failure_count': 1,
                'explanation': 'FP3',
                'plugin_name': 'Apache Default Index Page',
                'created_by': 'pci-testing@example.com',
                'determination_comment': 'Pass',
                'uuid': 'a0aaf660-9308-422c-8545-daa764886cf9',
                'cloned': True,
                'updated_at': '2021-09-16T04:52:30.837Z',
                'attestation_uuid': '47d04762-387d-44c0-aadc-b845d7227089',
                'updated_by': 'pci@example.com',
                'name': 'target3.pubtarg.tenablesecurity.com 106230',
                'scan_date': '2021-09-15T05:04:21Z',
                'status': 'passed',
            },
            {
                'severity': 2,
                'owner': 'pci-testing@example.com',
                'reason': 'false-positive',
                'plugin_id': 17705,
                'latest_comment': 'None',
                'customer_uuid': '196d99ba-7f93-4945-be6c-1a6089b36a7c',
                'created_at': '2021-09-15T12:20:45.177Z',
                'failure_count': 1,
                'explanation': 'FP4',
                'plugin_name': 'OPIE w/ OpenSSH Account Enumeration',
                'created_by': 'pci-testing@example.com',
                'uuid': 'dce82e5a-58ef-481e-a6ab-94ca0c0d1973',
                'cloned': True,
                'updated_at': '2021-09-15T12:20:45.177Z',
                'attestation_uuid': '47d04762-387d-44c0-aadc-b845d7227089',
                'updated_by': 'pci-testing@example.com',
                'name': 'target3.pubtarg.tenablesecurity.com 17705',
                'scan_date': '2021-09-15T05:04:21Z',
                'status': 'in-review',
            },
        ],
    }


@pytest.fixture
def fail_list():
    return {
        'pagination': {
            'total': 1,
            'offset': 0,
            'limit': 200,
            'sort': [{'name': 'plugin_id', 'order': 'desc'}],
        },
        'failures': [
            {
                'severity': 3,
                'plugin_id': 173384,
                'cvss_score': 9.8,
                'address': '127.0.0.1',
                'scan_uuid': '2693c579-0ab0-40c9-8eef-d8f1e18167ef',
                'duplicate': False,
                'rerank_type': 'not-reranked',
                'plugin_name': 'OpenSSH < 9.3 Multiple Vulnerabilities',
                'uuid': 'a3382dad-b0a8-4919-846d-1ec504d1e05f',
                'protocol': 'tcp',
                'asset_name': 'Asset Name',
                'port': 22,
                'attestation_uuid': 'dd39c320-ee0f-4a8d-9a7b-4cd334425fd7',
                'scan_name': 'Scan Name',
                'scan_date': '2023-06-08T17:05:04Z',
            }
        ],
    }


@pytest.fixture
def att_ass_list():
    return {
        'pagination': {
            'total': 1,
            'offset': 0,
            'limit': 200,
            'sort': [{'name': 'name', 'order': 'asc'}],
        },
        'assets': [
            {
                'excluded': False,
                'undisputed_failure_count': 14,
                'address': '127.0.0.1',
                'fqdn': 'target.example.com',
                'attestation_uuid': '12ec4034-1fcb-11ee-be56-0242ac120002',
                'scan_uuid': '6e384626-5937-476d-9f15-224df98e3fd6',
                'name': 'Asset Name',
                'operating_system': 'Linux Kernel 3.13 on Ubuntu 14.04 (trusty)',
                'failure_count': 14,
                'scan_name': 'Scan Name',
                'scan_date': '2023-07-06T15:57:26Z',
                'uuid': '2faa4bfe-1fcb-11ee-be56-0242ac120002',
            }
        ],
    }


def test_scans_format_sorts(tvm):
    assert (
        tvm.pci.attestations._format_sorts([('a', 'desc'), ('b', 'asc')])
        == 'a:desc,b:asc'
    )


@responses.activate
def test_attestation_list_iterator(tvm, att_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=att_list,
    )
    resp = tvm.pci.attestations.list()
    assert isinstance(resp, i.PCIAttestationsIterator)
    assert next(resp) == att_list['attestations'][0]
    assert next(resp) == att_list['attestations'][1]


@responses.activate
def test_attestation_list_no_iterator(tvm, att_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=att_list,
    )
    resp = tvm.pci.attestations.list(iterator=None)
    assert isinstance(resp, dict)
    assert resp == att_list


@responses.activate
def test_disputes_list_iterator(tvm, disp_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/details/12345678-1234-1234-1234-1234567890ab/disputes',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=disp_list,
    )
    resp = tvm.pci.attestations.disputes('12345678-1234-1234-1234-1234567890ab')
    assert isinstance(resp, i.PCIDisputesIterator)
    assert next(resp) == disp_list['disputes'][0]
    assert next(resp) == disp_list['disputes'][1]


@responses.activate
def test_disputes_list_no_iterator(tvm, disp_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/details/12345678-1234-1234-1234-1234567890ab/disputes',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=disp_list,
    )
    resp = tvm.pci.attestations.disputes(
        '12345678-1234-1234-1234-1234567890ab', iterator=None
    )
    assert isinstance(resp, dict)
    assert resp == disp_list


@responses.activate
def test_failures_list_iterator(tvm, fail_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/12345678-1234-1234-1234-1234567890ab/failures/undisputed/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=fail_list,
    )
    resp = tvm.pci.attestations.failures('12345678-1234-1234-1234-1234567890ab')
    assert isinstance(resp, i.PCIUndisputedFailuresIterator)
    assert next(resp) == fail_list['failures'][0]


@responses.activate
def test_failures_list_no_iterator(tvm, fail_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/12345678-1234-1234-1234-1234567890ab/failures/undisputed/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=fail_list,
    )
    resp = tvm.pci.attestations.failures(
        '12345678-1234-1234-1234-1234567890ab', iterator=None
    )
    assert isinstance(resp, dict)
    assert resp == fail_list


@responses.activate
def test_assets_list_iterator(tvm, att_ass_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/12345678-1234-1234-1234-1234567890ab/assets/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=att_ass_list,
    )
    resp = tvm.pci.attestations.assets('12345678-1234-1234-1234-1234567890ab')
    assert isinstance(resp, i.PCIAttestationAssetsIterator)
    assert next(resp) == att_ass_list['assets'][0]


@responses.activate
def test_assets_list_no_iterator(tvm, att_ass_list):
    responses.add(
        responses.GET,
        'https://nourl/pci-asv/attestations/12345678-1234-1234-1234-1234567890ab/assets/list',
        match=[query_param_matcher({'limit': 1000, 'offset': 0})],
        json=att_ass_list,
    )
    resp = tvm.pci.attestations.assets(
        '12345678-1234-1234-1234-1234567890ab', iterator=None
    )
    assert isinstance(resp, dict)
    assert resp == att_ass_list
