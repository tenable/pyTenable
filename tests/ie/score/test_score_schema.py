'''tests for score schema'''
import pytest
from marshmallow import ValidationError
from tenable.ie.score.schema import ScoreSchema

schema = ScoreSchema()


@pytest.fixture
def score_schema_directory_id_list():
    return {
        'profileId': '1',
        'directoryIds': [3, 4]
    }


def test_score_schema_directory_id_list(score_schema_directory_id_list):
    test_response = [{
        'directoryId': 3,
        'score': 100
    }, {
        'directoryId': 4,
        'score': None
    }]

    req = schema.load(score_schema_directory_id_list)
    assert test_response[0]['directoryId'] in req['directory_ids']
    assert test_response[0]['score'] == 100
    assert test_response[1]['score'] is None
    with pytest.raises(ValidationError):
        score_schema_directory_id_list['new_val'] = 'something'
        schema.load(score_schema_directory_id_list)


@pytest.fixture
def score_schema_directory_id_single():
    return {
        'directoryIds': '3',
        'checkerIds': '1',
        'reasonIds': '1'
    }


def test_score_schema_directory_id_single(score_schema_directory_id_single):
    test_response = [{
        'directoryId': 3,
        'score': None
    }]
    assert isinstance(test_response, list)
    req = schema.dump(schema.load(score_schema_directory_id_single))
    assert str(test_response[0]['directoryId']) == req['directoryIds']
    assert test_response[0]['score'] is None
    with pytest.raises(ValidationError):
        score_schema_directory_id_single['new_val'] = 'something'
        schema.load(score_schema_directory_id_single)


def test_score_schema_validation_error(score_schema_directory_id_single):
    '''
    test to raise the exception when directory_ids doesn't match with
    expected type
       '''
    with pytest.raises(ValidationError):
        score_schema_directory_id_single['directoryIds'] = True
        schema.load(score_schema_directory_id_single)
