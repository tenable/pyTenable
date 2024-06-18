'''tests for checker schema'''
import pytest
from marshmallow.exceptions import ValidationError
from tenable.ie.checker.schema import (CheckerSchema,
                                       RecommendationSchema,
                                       AttackerKnownToolSchema,
                                       ResourcesSchema,
                                       VulnerabilityDetailSchema)


@pytest.fixture
def checker_schema():
    return {
        "id": 0,
        "codename": "C-toto-s",
        "categoryId": 0,
        "remediationCost": 0,
        "name": "string",
        "description": "string",
        "execSummary": "string",
        "vulnerabilityDetail": {
            "detail": "string"
        },
        "attackerKnownTools": [{
            "name": "tool_name",
            "url": "string",
            "author": "string"
        }],
        "resources": [{
            "name": "computers",
            "url": "string",
            "type": "string"
        }],
        "recommendation": {
            "name": "string",
            "description": "string",
            "execSummary": "string",
            "detail": "recommendation_details",
            "resources": [{
                "name": "string",
                "url": "string",
                "type": "string"
            }]
        }
    }


def test_checker_schema(checker_schema):
    test_response = {
        "id": 2,
        "codename": "C-toto-s",
        "category_id": 0,
        "remediationCost": 0,
        "name": "string",
        "description": "desc",
        "execSummary": "summary",
        "vulnerabilityDetail": {
            "detail": "vuln_detail"
        },
        "attackerKnownTools": [{
            "name": "test",
            "url": "test@tenable.com",
            "author": "Mac"
        }],
        "resources": [{
            "name": "cyberc",
            "url": "cyberc@tenable.com",
            "type": "book"
        }],
        "recommendation": {
            "name": "recommended_name",
            "description": "about",
            "execSummary": "summary",
            "detail": "details",
            "resources": [{
                "name": "cyberc1",
                "url": "cyberc1@tenable.com",
                "type": "book1"
            }]
        }
    }
    schema = CheckerSchema()
    assert test_response['category_id'] == \
           schema.dump(schema.load(checker_schema))['categoryId']
    with pytest.raises(ValidationError):
        checker_schema['new_val'] = 'something'
        schema.load(checker_schema)


@pytest.fixture
def recommendation_schema():
    return {
        "name": "recommended_name",
        "description": "string",
        "execSummary": "string",
        "detail": "string",
        "resources": [{
            "name": "string",
            "url": "string",
            "type": "string"
        }]
    }


def test_recommendation_schema(recommendation_schema):
    test_response = {
        "name": "recommended_name",
        "description": "about",
        "execSummary": "summary",
        "detail": "details",
        "resources": [{
            "name": "cyberc1",
            "url": "cyberc1@tenable.com",
            "type": "book1"
        }]
    }
    schema = RecommendationSchema()
    assert test_response['name'] == \
           schema.dump(schema.load(recommendation_schema))['name']
    with pytest.raises(ValidationError):
        recommendation_schema['new_val'] = 'something'
        schema.load(recommendation_schema)


@pytest.fixture
def attacker_known_tool_schema():
    return [{
        'author': None,
        'name': 'Kerberoast',
        'type': 'hyperlink',
        'url': 'https://github.com/nidem/kerberoast'
    }]


def test_attacker_known_tool_schema(attacker_known_tool_schema):
    test_response = [{
        'author': None,
        'name': 'Kerberoast',
        'type': 'hyperlink',
        'url': 'https://github.com/nidem/kerberoast'
    }, {
        'author': None,
        'name': 'Empire',
        'type': 'hyperlink',
        'url': 'https://github.com/EmpireProject/Empire'
    }, {
        'author': 'Gentil Kiwi',
        'link': 'https://github.com/gentilkiwi/mimikatz/releases\
                    /latest',
        'name': 'mimikatz',
        'url': None
    }, {
        'author': None,
        'name': 'PowerSploit',
        'type': 'hyperlink',
        'url': 'https://github.com/PowerShellMafia/PowerSploit'
    }]
    schema = AttackerKnownToolSchema()
    assert test_response[0] == schema.dump(
        schema.load(attacker_known_tool_schema[0]))
    with pytest.raises(ValidationError):
        attacker_known_tool_schema[0]['new_val'] = 'something'
        schema.load(attacker_known_tool_schema[0])


@pytest.fixture
def resource_schema():
    return [{
        'name': 'MITRE ATT&CK – Steal or Forge Kerberos Tickets: '
                'Kerberoasting',
        'type': 'hyperlink',
        'url': 'https://attack.mitre.org/techniques/T1558/003/'
    }, {
        'name': 'Kerberos: An Authentication Service for Computer '
                'Networks',
        'type': 'hyperlink',
        'url': 'http://gost.isi.edu/publications/kerberos-neuman-tso'
               '.html '
    }]


def test_resource_schema(resource_schema):
    test_response = [{
        'name': 'MITRE ATT&CK – Steal or Forge Kerberos Tickets: '
                'Kerberoasting',
        'type': 'hyperlink',
        'url': 'https://attack.mitre.org/techniques/T1558/003/'
    }, {
        'name': 'Kerberos: An Authentication Service for Computer '
                'Networks',
        'type': 'hyperlink',
        'url': 'http://gost.isi.edu/publications/kerberos-neuman-tso'
               '.html '
    }]
    schema = ResourcesSchema()
    assert test_response[0] == schema.dump(
        schema.load(resource_schema[0]))
    with pytest.raises(ValidationError):
        resource_schema[0]['new_val'] = 'something'
        schema.load(resource_schema[0])


@pytest.fixture
def vulnerability_detail_schema():
    return {
        'detail': 'string'
    }


def test_vulnerability_detail_schema(vulnerability_detail_schema):
    test_response = {
        'detail': 'string'
    }
    schema = VulnerabilityDetailSchema()
    assert test_response == schema.dump(
        schema.load(vulnerability_detail_schema))
    with pytest.raises(ValidationError):
        vulnerability_detail_schema['new_val'] = 'something'
        schema.load(vulnerability_detail_schema)
