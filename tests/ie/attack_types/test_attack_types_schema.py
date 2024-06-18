'''
Testing the attack type schemas
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.attack_types.schema import (
    AttackTypesSchema,
    AttackTypesResourceSchema,
    AttackTypesVectorTemplateReplacementsSchema
)


def test_attack_type_schema():
    '''
    test attack type schema
    '''
    test_resp = [{
        "id": 1,
        "name": "test",
        "yaraRules": "attack type rules",
        "description": "attack type description",
        "workloadQuota": 3,
        "mitreAttackDescription": "mitre_attack_description",
        "criticity": "critical",
        "resources": [{
            "name": "resource name",
            "url": "https://test.domain.com",
            "type": "resource type"
        }],
        "vectorTemplate": "vector_template",
        "vectorTemplateReplacements": [{
            "name": "user",
            "valueType": "string"
        }]
    }]

    schema = AttackTypesSchema()
    req = schema.load(test_resp, many=True)
    assert test_resp[0]['id'] == req[0]['id']
    assert test_resp[0]['name'] == req[0]['name']
    assert test_resp[0]['yaraRules'] == req[0]['yara_rules']
    assert test_resp[0]['description'] == req[0]['description']
    assert test_resp[0]['workloadQuota'] == req[0]['workload_quota']
    assert test_resp[0]['mitreAttackDescription'] == req[0][
        'mitre_attack_description']
    assert test_resp[0]['criticity'] == req[0]['criticity']
    assert test_resp[0]['vectorTemplate'] == req[0]['vector_template']

    with pytest.raises(ValidationError):
        test_resp[0]['some_val'] = 'something'
        schema.load(test_resp, many=True)


def test_attack_type_resource_schema():
    '''
    test attack type resource schema
    '''
    test_resp = {
        "name": "resource name",
        "url": "https://test.domain.com",
        "type": "resource type"
    }

    schema = AttackTypesResourceSchema()
    req = schema.load(test_resp)
    assert test_resp['name'] == req['name']
    assert test_resp['url'] == req['url']
    assert test_resp['type'] == req['type']

    with pytest.raises(ValidationError):
        test_resp['some_val'] = 'something'
        schema.load(test_resp)


def test_attack_type_vector_template_replacements_schema():
    '''
    test attack type vector template replacements schema
    '''
    test_resp = {
        "name": "user",
        "valueType": "string"
    }

    schema = AttackTypesVectorTemplateReplacementsSchema()
    req = schema.load(test_resp)
    assert test_resp['name'] == req['name']
    assert test_resp['valueType'] == req['value_type']

    with pytest.raises(ValidationError):
        test_resp['some_val'] = 'something'
        schema.load(test_resp)
