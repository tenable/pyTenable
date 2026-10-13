"""
test file to test various scenarios in sc report_definition
"""

import pytest
import responses
from ..checker import check


def test_report_definition_id_typeerror(tsc):
    """
    validate id is int not string
    """
    with pytest.raises(TypeError):
        tsc.report_definition.launch(id='one')


def test_report_definition_id_item_typeerror(tsc):
    """
    validate id is int not list
    """

    with pytest.raises(TypeError):
        tsc.report_definition.launch(id=['one'])


@responses.activate
def test_report_definition_launch_success(tsc):
    """
    validate launch is successful and returns running report ID
    """
    responses.post(
        'https://nourl/rest/reportDefinition/1/launch',
        json={
            'type': 'regular',
            'response': {
                'reportDefinitionID': '1',
                'reportResult': {
                    'creatorID': '2',
                    'ownerID': '2',
                    'ownerGID': '1',
                    'reportDefinitionID': '7',
                    'jobID': '113868',
                    'name': 'CS-4700 Iterator',
                    'description': '',
                    'type': 'pdf',
                    'status': 'Queued',
                    'errorDetails': '',
                    'totalSteps': -1,
                    'completedSteps': 0,
                    'startTime': -1,
                    'finishTime': 0,
                    'pubSites': [],
                    'id': '1',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1434567869,
        },
    )
    report = tsc.report_definition.launch(id=1)
    assert isinstance(report, dict)
    check(report['reportResult'], 'id', str)
    check(report['reportResult'], 'name', str)
    check(report['reportResult'], 'status', str)
