from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from tenable.io.exports import models as m


@pytest.fixture
def asset_export():
    """
    Example asset export request
    """
    return {
        'chunk_size': 1000,
        'filters': {
            'last_scan_id': 'd27b3f28-9a36-4127-b63a-3da3801121ec',
            'created_at': 1635798607,
            'deleted_at': 1635798607,
            'first_scan_time': 1635798607,
            'last_assessed': 1635798607,
            'last_authenticated_scan_time': 1635798607,
            'terminated_at': 1635798607,
            'updated_at': 1635798607,
            'has_plugin_results': 'no',
            'is_licensed': 'yes',
            'is_terminated': True,
            'servicenow_sysid': 'true',
            'network_id': 'f634d639-cc33-4149-a683-5ad6b8f29d9c',
            'tags': [
                ('test1', 'val1'),
                ('test2', 'val2'),
                ('test3', 'val3'),
                ('test3', 'val4'),
            ],
        },
    }


@pytest.fixture
def asset_export_with_open_ports_true():
    """
    Asset export request with open ports set as true.
    """
    return {'chunk_size': 1000, 'include_open_ports': True, 'filters': {}}


@pytest.fixture
def asset_export_with_open_ports_false():
    """
    Asset export request with open ports set as false.
    """
    return {'chunk_size': 1000, 'include_open_ports': False, 'filters': {}}


@pytest.fixture
def asset_export_with_out_open_ports():
    """
    Asset export request without open ports.
    """
    return {'chunk_size': 1000, 'filters': {}}


@pytest.fixture
def compliance_export():
    """
    Example compliance export request
    """
    return {
        'num_findings': 1000,
        'asset': [
            'f634d639-cc33-4149-a683-5ad6b8f29d9c',
            UUID('c62f8737-8623-45a3-bdcb-560daacb21f1'),
        ],
        'filters': {
            'first_seen': 1635798607,
            'last_seen': 1635798607,
        },
    }


@pytest.fixture
def compliance_export_phase_1_and_2_schema():
    """
    Example compliance export request with phase 1 filters
    """
    return {
        'num_findings': 1000,
        'asset': [
            'f634d639-cc33-4149-a683-5ad6b8f29d9c',
            UUID('c62f8737-8623-45a3-bdcb-560daacb21f1'),
        ],
        'filters': {
            'first_seen': 1635798607,
            'last_seen': 1635798607,
            'ipv4_addresses': ['192.168.0.1'],
            'ipv6_addresses': ['2001:0db8:85a3:0000:0000:8a2e:0370:7334'],
            'plugin_name': [
                'Debian dla-3719 : php-seclib - security update',
                'Debian dsa-5607 : chromium - security update',
            ],
            'plugin_id': [189491, 189490],
            'audit_name': 'my-audit-name',
            'audit_file_name': 'my-audit-file-name',
            'compliance_results': ['PASSED'],
            'last_observed': 1635798607,
            'indexed_at': 1635798607,
            'since': 1635798607,
            'state': ['open'],
            'tags': [('Category', ['value1', 'value2'])],
            'network_id': 'd6797cf4-42b9-4cad-8591-9dd91c3f0fc3',
        },
    }


@pytest.fixture
def vuln_export():
    """
    Example vulnerability export request
    """
    return {
        'include_unlicensed': True,
        'num_assets': 500,
        'filters': {
            'first_found': 1635798607,
            'last_found': 1635798607,
            'indexed_at': 1635798607,
            'last_fixed': 1635798607,
            'since': 1635798607,
            'plugin_family': ['Family Name'],
            'plugin_id': [19506, 21745, 66334],
            'scan_uuid': '992b7204-bde2-d17c-cabf-1191f2f6f56b7f1dbd59e117463c',
            'severity': ['CRITICAL', 'High', 'medium', 'LoW', 'InfO'],
            'state': ['OPEN', 'reopened', 'Fixed'],
            'vpr_score': {
                'eq': [2.0, 3.1],
                'neq': [9.9],
                'gt': 1,
                'gte': 1.1,
                'lt': 0.5,
                'lte': 0.4,
            },
            'tags': [
                ('test1', 'val1'),
                ('test2', 'val2'),
                ('test3', 'val3'),
                ('test3', 'val4'),
            ],
            'network_id': 'f634d639-cc33-4149-a683-5ad6b8f29d9c',
            'cidr_range': '192.0.2.0/24',
        },
    }


def test_assetschema(asset_export):
    """
    Test the asset export schema
    """
    test_resp = {
        'chunk_size': 1000,
        'filters': {
            'last_scan_id': 'd27b3f28-9a36-4127-b63a-3da3801121ec',
            'created_at': 1635798607,
            'deleted_at': 1635798607,
            'first_scan_time': 1635798607,
            'last_assessed': 1635798607,
            'last_authenticated_scan_time': 1635798607,
            'terminated_at': 1635798607,
            'updated_at': 1635798607,
            'has_plugin_results': False,
            'is_licensed': True,
            'is_terminated': True,
            'servicenow_sysid': True,
            'network_id': 'f634d639-cc33-4149-a683-5ad6b8f29d9c',
            'tag.test1': ['val1'],
            'tag.test2': ['val2'],
            'tag.test3': ['val3', 'val4'],
        },
    }

    assert test_resp == m.AssetExportV1(**asset_export).model_dump(
        mode='json', exclude_none=True
    )

    with pytest.raises(ValidationError):
        asset_export['new_val'] = 'something'
        m.AssetExportV1(**asset_export)


def test_complianceschema(compliance_export):
    """
    Test the compliance export schema
    """
    test_resp = {
        'num_findings': 1000,
        'asset': [
            'f634d639-cc33-4149-a683-5ad6b8f29d9c',
            'c62f8737-8623-45a3-bdcb-560daacb21f1',
        ],
        'filters': {'first_seen': 1635798607, 'last_seen': 1635798607},
    }
    assert test_resp == m.ComplianceExportV1(**compliance_export).model_dump(
        mode='json', exclude_none=True
    )

    with pytest.raises(ValidationError):
        compliance_export['new_val'] = 'something'
        m.ComplianceExportV1(**compliance_export)


def test_vulnerabilityschema(vuln_export):
    """
    Test the vulnerability finding schema
    """
    test_resp = {
        'num_assets': 500,
        'include_unlicensed': True,
        'filters': {
            'first_found': 1635798607,
            'last_found': 1635798607,
            'indexed_at': 1635798607,
            'last_fixed': 1635798607,
            'since': 1635798607,
            'plugin_family': ['Family Name'],
            'plugin_id': [19506, 21745, 66334],
            'scan_uuid': '992b7204-bde2-d17c-cabf-1191f2f6f56b7f1dbd59e117463c',
            'severity': ['critical', 'high', 'medium', 'low', 'info'],
            'state': ['OPEN', 'REOPENED', 'FIXED'],
            'vpr_score': {
                'eq': [2.0, 3.1],
                'neq': [9.9],
                'gt': 1.0,
                'gte': 1.1,
                'lt': 0.5,
                'lte': 0.4,
            },
            'network_id': 'f634d639-cc33-4149-a683-5ad6b8f29d9c',
            'cidr_range': '192.0.2.0/24',
            'tag.test1': ['val1'],
            'tag.test2': ['val2'],
            'tag.test3': ['val3', 'val4'],
        },
    }
    assert test_resp == m.VulnerabilityExportV1(**vuln_export).model_dump(
        mode='json', exclude_none=True
    )

    with pytest.raises(ValidationError):
        vuln_export['new_val'] = 'something'
        m.VulnerabilityExportV1(**vuln_export)

    with pytest.raises(ValidationError):
        vuln_export['scan_uuid'] = 0
        m.VulnerabilityExportV1(**vuln_export)


def test_asset_export_schema_for_open_ports_true(asset_export_with_open_ports_true):
    """
    Ensure Asset Export request is correctly formed with include_open_ports set to true.
    """
    schema_dump = m.AssetExportV1(**asset_export_with_open_ports_true).model_dump(
        mode='json', exclude_none=True
    )
    assert schema_dump['include_open_ports'] is True


def test_asset_export_schema_for_open_ports_false(asset_export_with_open_ports_false):
    """
    Ensure Asset Export request is correctly formed with include_open_ports set to false.
    """
    schema_dump = m.AssetExportV1(**asset_export_with_open_ports_false).model_dump(
        mode='json', exclude_none=True
    )
    assert schema_dump['include_open_ports'] is False


def test_asset_export_schema_without_open_ports(asset_export_with_out_open_ports):
    """
    Ensure Asset Export request is correctly formed without include_open_ports.
    """
    schema_dump = m.AssetExportV1(**asset_export_with_out_open_ports).model_dump(
        mode='json', exclude_none=True
    )
    assert 'include_open_ports' not in schema_dump


def test_compliance_export_phase_1_and_2_filters(
    compliance_export_phase_1_and_2_schema,
):
    """
    Test Compliance Export Phase 1 Filter Schema
    """
    schema_dump = m.ComplianceExportV1(
        **compliance_export_phase_1_and_2_schema
    ).model_dump(mode='json', exclude_none=True)

    # checking random element
    assert schema_dump['filters']['state'][0] == 'OPEN'
    assert len(schema_dump['filters']['tags']) == 1
    assert (
        schema_dump['filters']['network_id'] == 'd6797cf4-42b9-4cad-8591-9dd91c3f0fc3'
    )


@pytest.fixture
def was_vulns_export():
    """
    Example was vulns export request
    """
    return {
        'num_assets': 50,
        'include_unlicensed': False,
        'filters': {
            'asset_uuid': ['d27b3f28-9a36-4127-b63a-3da3801121ec'],
            'asset_name': 'abc.com',
            'first_found': 1635798607,
            'last_found': 1635798606,
            'last_fixed': 1635798605,
            'indexed_at': 1635798604,
            'since': 1635798603,
            'plugin_ids': [1340, 2554],
            'owasp_2010': ['A1'],
            'owasp_2013': ['A1'],
            'owasp_2017': ['a1'],
            'owasp_2021': ['a1'],
            'owasp_api_2019': ['api1'],
            'severity': ['Low'],
            'state': ['Fixed'],
            'severity_modification_type': ['ACCEPTED'],
            'vpr_score': {'eq': [1.2, 3.5]},
            'ipv4s': ['134.43.4.34'],
        },
    }


def test_was_vulns_schema_all_values(was_vulns_export):
    test_resp = {
        'num_assets': 50,
        'include_unlicensed': False,
        'filters': {
            'asset_uuid': ['d27b3f28-9a36-4127-b63a-3da3801121ec'],
            'asset_name': 'abc.com',
            'first_found': 1635798607,
            'last_found': 1635798606,
            'last_fixed': 1635798605,
            'indexed_at': 1635798604,
            'since': 1635798603,
            'plugin_ids': [1340, 2554],
            'owasp_2010': ['A1'],
            'owasp_2013': ['A1'],
            'owasp_2017': ['A1'],
            'owasp_2021': ['A1'],
            'owasp_api_2019': ['API1'],
            'severity': ['low'],
            'state': ['FIXED'],
            'severity_modification_type': ['ACCEPTED'],
            'vpr_score': {'eq': [1.2, 3.5]},
            'ipv4s': ['134.43.4.34'],
        },
    }

    assert test_resp == m.WASExportV1(**was_vulns_export).model_dump(
        mode='json', exclude_none=True
    )

    with pytest.raises(ValidationError):
        was_vulns_export['new_val'] = 'something'
        m.WASExportV1(**was_vulns_export)
