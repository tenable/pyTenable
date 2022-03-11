'''
Tests for connectors endpoint
'''

import responses
from requests import Response
from responses import matchers

from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)

CONNECTORS_BASE_URL = r'https://cloud.tenable.com/api/v3/connectors'


@responses.activate
def test_create(api):
    '''
    Test the create function
    '''
    resp_data = {
        'connector': {
            'type': 'aws_keyless',
            'human_type': 'AWS',
            'data_type': 'assets',
            'name': 'AWS Keyless FA Connector',
            'status': 'Scheduled',
            'status_message': 'FA Enabled',
            'schedule': {
                'units': 'minutes',
                'value': 30,
                'empty': False
            },
            'date_created': '2021-07-22T14:31:15.616Z',
            'id': '5b08b44c-5682-4d8c-b574-a660052c9895',
            'container_id': '330dbe3b-263e-411f-b73f-bc1abbd187f3',
            'expired': False,
            'incremental_mode': False,
            'params': {
                'sub_accounts': [
                    {
                        'account_id': '012345678912',
                        'trails': [],
                        'role_arn':
                            'arn:aws:iam::04567:role/tenableio-connector_ex',
                        'external_id': '4fec419f-a9af-4183-8b4b-2e6bcf7d1975',
                        'incremental_mode': False
                    }
                ],
                'import_config': False,
                'auto_discovery': True,
                'tags': [
                    {
                        'key': 'Tenable',
                        'value': 'FA'
                    }
                ],
                'service': 'aws_keyless'
            },
            'network_id': '00000000-0000-0000-0000-000000000000'
        }
    }

    responses.add(
        responses.POST,
        url=f'{CONNECTORS_BASE_URL}',
        json=resp_data
    )

    resp = api.v3.connectors.create(
        name='test', con_type='aws_keyless',
        network_id='00000000-0000-0000-0000-000000000000',
        schedule=('days', 2), sub_accounts=[{}]
    )

    assert resp['type'] == 'aws_keyless'


@responses.activate
def test_aws_cloudtrails(api):
    '''
    Test the aws cloudtrails function
    '''
    resp_data = {
        'trails': [
            {
                'arn':
                    'arn:aws:cloudtrail:us-east-1:00:trail/ExampleAWSTrail',
                'name': 'ExampleAWSTrail',
                'region': {
                    'name': 'All',
                    'friendly_name': 'All'
                },
                'availability': 'success'
            },
            {
                'arn': 'arn:aws:cloudtrail:us-east-1:20:trail/ExampleAWSTrail',
                'name': 'ExampleAWSTrail',
                'region': {
                    'name': 'All',
                    'friendly_name': 'All'
                },
                'availability': 'success'
            }
        ]
    }

    responses.add(
        responses.POST,
        url=f'{CONNECTORS_BASE_URL}/aws/cloudtrails',
        json=resp_data
    )

    resp = api.v3.connectors.list_aws_cloudtrails(
        region=[('All', 'All')], credentials={
            'access_key': 'fasd7fs897df98asdf79a8sd9f',
            'secret_key': 'hfghty7fs897df98asdf79a8sd9f'
        }
    )

    assert resp[0]['name'] == 'ExampleAWSTrail'


@responses.activate
def test_delete(api):
    '''
    Test the delete function
    '''
    connector_id = '80e82b30-596f-4229-95b2-404429ae1767'
    responses.add(
        responses.DELETE,
        f'{CONNECTORS_BASE_URL}/{connector_id}'
    )
    assert None is api.v3.connectors.delete(connector_id)


@responses.activate
def test_details(api):
    '''
    Test the details function
    '''

    resp_data = {
        'connector': {
            'type': 'aws_keyless',
            'human_type': 'AWS',
            'data_type': 'assets',
            'name': 'AWS Keyless with Frictionless Assessment Connector',
            'is_fa': True,
            'status': 'Scheduled',
            'status_message': 'Import completed successfully',
            'schedule': {
                'units': 'minutes',
                'value': 30,
                'empty': False
            },
            'date_created': '2021-07-22T14:31:15.616Z',
            'date_modified': '2021-07-22T14:31:27.098Z',
            'id': 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba',
            'container_id': '7930d8cc-27c0-43cc-abdb-b846e2b13414',
            'expired': False,
            'incremental_mode': True,
            'last_sync_time': '2021-07-22T14:31:27.098Z',
            'last_run': '2021-07-22T14:31:39.809Z',
            'params': {
                'sub_accounts': [
                    {
                        'account_id': '012345678910',
                        'trails': [],
                        'role_arn':
                            'arn:aws:iam::00:role/tenableio-connector_example',
                        'external_id': '7930d8cc-27c0-43cc-abdb-b846e2b13414',
                        'incremental_mode': False
                    }
                ],
                'import_config': False,
                'auto_discovery': True,
                'tags': [
                    {
                        'key': 'Tenable',
                        'value': 'FA'
                    }
                ],
                'service': 'aws_keyless'
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_seen_updated': '2021-07-22T14:31:39.801Z'
        }
    }

    connector_id = 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba'
    responses.add(
        responses.GET,
        f'{CONNECTORS_BASE_URL}/{connector_id}',
        json=resp_data
    )

    resp = api.v3.connectors.details(connector_id)
    assert resp['id'] == connector_id


@responses.activate
def test_download_template(api):
    '''
    Test the download template function
    '''

    resp_data = {
        '$schema':
            'https://schema.management.azure.com/schemas/2018-05-01/subscriptionDeploymentTemplate.json#', # noqa E501
        'contentVersion': '1.0.0.0',
        'variables': {
            'connectorId': 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba',
            'storageAccount': 'faconnector',
            'storageContainer': 'ba10492c-365b-1a45-ba07-5670efae1b12',
            'storageKey': 'redacted',
            'scriptsAccount': 'faautomationscript',
            'scriptsKey': 'redacted',
            'tableKey': 'redacted',
            'keyRotationMethod': 'default',
            'resourceGroupLocation': 'eastus',
            'resourceGroupName':
                '[concat("Tenable-FA-Connector-",variables("connectorid"))]',
            'tenableFACollectionRoleDefinitionResourceName':
                '[guid("Tenable-FA-Custom-Role-Def",'
                ' subscription().id, variables("connectorId"))]',
            'tenableFACollectionRoleDefinitionId':
                '[subscriptionResourceId('
                '"Microsoft.Authorization/roleDefinitions",'
                ' variables("tenableFACollectionRoleDefinitionResourceName")'
                ')]',
            'logicAppName': 'TenableFAEventBasedCollection',
            'resourceTags': {
                'Tenable': 'AzureFa'
            },
            'roleDefinition': {
                'name':
                    '[format("Tenable FA Role (Subscription: {0} |'
                    ' Connector: {1})", subscription().subscriptionId, '
                    'variables("connectorId"))]',
                'description':
                    'Auth required to run Assessment on Azure Resources',
                'actions': [
                    'Microsoft.ClassicCompute/operatingSystems/read',
                    'Microsoft.ClassicCompute/operatingSystemFamilies/read',
                    'Microsoft.ClassicCompute/virtualMachines/read',
                    'Microsoft.Compute/virtualMachines/read',
                    'Microsoft.Compute/virtualMachineScaleSets/read',
                    'Microsoft.Compute/virtualMachines/runCommand/action'
                ],
                'notActions': []
            }
        },
        'resources': [
            {
                'type': 'Microsoft.Resources/resourceGroups',
                'apiVersion': '2020-06-01',
                'name': '[variables("resourceGroupName")]',
                'location': '[variables("resourceGroupLocation")]',
                'tags': '[variables("resourceTags")]',
                'properties': {}
            },
            {
                'type': 'Microsoft.Authorization/roleDefinitions',
                'apiVersion': '2018-01-01-preview',
                'name':
                    '[variables("tenableFACollectionRoleDefResourceName")]',
                'properties': {
                    'roleName': '[variables("roleDefinition").name]',
                    'description': '[variables("roleDefinition").description]',
                    'type': 'customRole',
                    'permissions': [
                        {
                            'actions': '[variables("roleDefinition").actions]',
                            'notActions':
                                '[variables("roleDefinition").notActions]'
                        }
                    ],
                    'assignableScopes': [
                        '[subscription().id]'
                    ]
                }
            }
        ]
    }

    connector_id = 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba'
    responses.add(
        responses.GET,
        f'{CONNECTORS_BASE_URL}/azure_fa/{connector_id}/arm-template',
        json=resp_data
    )

    resp = api.v3.connectors.download_template(connector_id)
    assert resp['variables']['connectorId'] == connector_id


@responses.activate
def test_import_data(api):
    '''
    Test the import data function
    '''

    resp_data = {
        'connector': {
            'type': 'aws',
            'human_type': 'AWS',
            'data_type': 'assets',
            'name': 'AWS Connector - Keyed',
            'status': 'Scheduled',
            'status_message': 'Import completed successfully',
            'date_created': '2019-11-31T17:21:19.495Z',
            'date_modified': '2019-12-31T17:21:28.457Z',
            'id': 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba',
            'container_id': '154a05bd-3f27-495a-a001-a659c24eb1a4',
            'expired': False,
            'incremental_mode': False,
            'last_sync_time': '2019-12-31T17:21:28.457Z',
            'params': {
                'access_key': 'AJIAJLRNVRLZRDZLVBXR',
                'trails': [
                    {
                        'arn':
                            'arn:aws:cloudtrail:us-east-1:06:trail/ExampleAWSTrail', # noqa E501
                        'name': 'ExampleAWSTrail',
                        'region': {
                            'name': 'All',
                            'friendly_name': 'All'
                        },
                        'availability': ''
                    }
                ],
                'sub_accounts': [
                    {
                        'role_arn': 'arn:aws:iam::51:role/tenableio-connector',
                        'external_id': '154a05bd-3f27-495a-a001-a659c24eb1a4',
                        'trails': [
                            {
                                'arn':
                                    'arn:aws:cloudtrail:us-east-1:795163652895:trail/ExampleAWSTrail', # noqa E501
                                'name': 'ExampleAWSTrail',
                                'region': {
                                    'name': 'us-west-1',
                                    'friendly_name': 'us-west-1'
                                },
                                'availability': ''
                            }
                        ],
                        'incremental_mode': False,
                        'account_id': '795163652895'
                    }
                ],
                'service': 'aws'
            },
            'network_id': '89578c5d-931a-4bae-bcd6-421cacfad3b8'
        }
    }

    connector_id = 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba'
    responses.add(
        responses.POST,
        f'{CONNECTORS_BASE_URL}/{connector_id}/import',
        json=resp_data
    )

    resp = api.v3.connectors.import_data(connector_id)
    assert resp['id'] == connector_id


@responses.activate
def test_edit(api):
    '''
    Test the edit function
    '''

    resp_data_details = {
        'connector': {
            'type': 'aws_keyless',
            'human_type': 'AWS',
            'data_type': 'assets',
            'name': 'AWS Keyless with Frictionless Assessment Connector',
            'is_fa': True,
            'status': 'Scheduled',
            'status_message': 'Import completed successfully',
            'schedule': {
                'units': 'minutes',
                'value': 30,
                'empty': False
            },
            'date_created': '2021-07-22T14:31:15.616Z',
            'date_modified': '2021-07-22T14:31:27.098Z',
            'id': 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba',
            'container_id': '7930d8cc-27c0-43cc-abdb-b846e2b13414',
            'expired': False,
            'incremental_mode': True,
            'last_sync_time': '2021-07-22T14:31:27.098Z',
            'last_run': '2021-07-22T14:31:39.809Z',
            'params': {
                'sub_accounts': [
                    {
                        'account_id': '012345678910',
                        'trails': [],
                        'role_arn':
                            'arn:aws:iam::00:role/tenableio-connector_example',
                        'external_id': '7930d8cc-27c0-43cc-abdb-b846e2b13414',
                        'incremental_mode': False
                    }
                ],
                'import_config': False,
                'auto_discovery': True,
                'tags': [
                    {
                        'key': 'Tenable',
                        'value': 'FA'
                    }
                ],
                'service': 'aws_keyless'
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_seen_updated': '2021-07-22T14:31:39.801Z'
        }
    }

    resp_data = {
        'connector': {
            'type': 'aws_keyless',
            'human_type': 'AWS',
            'data_type': 'assets',
            'name': 'AWS keyless renamed',
            'is_fa': True,
            'status': 'Scheduled',
            'status_message': 'Import completed successfully',
            'schedule': {
                'units': 'minutes',
                'value': 30,
                'empty': False
            },
            'date_created': '2021-07-22T14:31:15.616Z',
            'date_modified': '2021-07-22T14:31:27.098Z',
            'id': 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba',
            'container_id': '7930d8cc-27c0-43cc-abdb-b846e2b13414',
            'expired': False,
            'incremental_mode': True,
            'last_sync_time': '2021-07-22T14:31:27.098Z',
            'last_run': '2021-07-22T14:31:39.809Z',
            'params': {
                'sub_accounts': [
                    {
                        'account_id': '012345678910',
                        'trails': [],
                        'role_arn':
                            'arn:aws:iam::00:role/tenableio-connector_example',
                        'external_id': '7930d8cc-27c0-43cc-abdb-b846e2b13414',
                        'incremental_mode': False
                    }
                ],
                'import_config': True,
                'auto_discovery': False,
                'tags': [
                    {
                        'key': 'Tenable',
                        'value': 'FA'
                    }
                ],
                'service': 'aws_keyless'
            },
            'network_id': '00000000-0000-0000-0000-000000000000',
            'last_seen_updated': '2021-07-22T14:31:39.801Z'
        }
    }

    connector_id = 'b3397cb2-6650-432b-ae1c-fc64ec7ef6ba'
    responses.add(
        responses.GET,
        f'{CONNECTORS_BASE_URL}/{connector_id}',
        json=resp_data_details
    )

    responses.add(
        responses.PUT,
        f'{CONNECTORS_BASE_URL}/{connector_id}',
        json=resp_data
    )

    resp = api.v3.connectors.edit(connector_id, name='AWS keyless renamed',
                                  import_config=True,
                                  auto_discovery=False)
    assert resp['name'] == 'AWS keyless renamed'


@responses.activate
def test_search(api):
    '''
    Test the search method
    '''
    fields = [
        'name',
        'type',
        'id'
    ]
    sort = [('date_created', 'desc')]
    filters = ('status', 'eq', 'Scheduled')

    payload = {
        'fields': fields,
        'limit': 200,
        'sort': [{'date_created': 'desc'}],
        'filter': {
            'property': 'status',
            'operator': 'eq',
            'value': 'Scheduled'
        }
    }

    api_response = {
        'connectors': [
            {
                'type': 'aws_keyless',
                'human_type': 'AWS',
                'data_type': 'assets',
                'name': 'AWS FA Connector',
                'is_fa': True,
                'status': 'Scheduled',
                'status_message': 'Import completed successfully',
                'date_created': '2021-07-22T14:31:15.616Z',
                'date_modified': '2021-07-22T14:31:27.098Z',
                'id': '56d31cbe-efab-47d6-8158-749192629954',
                'container_id': '9164fd5e-5013-4fa2-bfce-557c54f7a7e4',
                'expired': False,
                'incremental_mode': True,
                'last_sync_time': '2021-07-22T14:31:27.098Z',
                'last_run': '2021-07-22T14:31:39.809Z',
                'params': {
                    'sub_accounts': [
                        {
                            'account_id': '012345678901',
                            'trails': [],
                            'role_arn':
                                'arn:aws:iam::01:role/tenableio-connector_example',  # noqa E501
                            'external_id':
                                '5147401f-d006-4a2b-9ded-a40c156be579',
                            'incremental_mode': False,
                        },
                    ],
                    'import_config': False,
                    'auto_discovery': True,
                    'tags': [],
                    'service': 'aws_keyless',
                },
                'network_id': '00000000-0000-0000-0000-000000000000',
                'last_seen_updated': '2021-07-22T14:31:39.801Z',
            }
        ],
        'pagination': {
            'total': 1,
            'next': 'nextToken'
        }

    }
    responses.add(
        responses.POST,
        f'{CONNECTORS_BASE_URL}/search',
        match=[matchers.json_params_matcher(payload)],
        json=api_response
    )

    iterator = api.v3.connectors.search(
        fields=fields, limit=200, sort=sort, filter=filters
    )
    assert isinstance(iterator, SearchIterator)

    assert len(list(iterator)) == api_response['pagination']['total']

    iterator = api.v3.connectors.search(
        fields=fields, return_csv=True, sort=sort, limit=200, filter=filters
    )
    assert isinstance(iterator, CSVChunkIterator)

    resp = api.v3.connectors.search(
        fields=fields, return_resp=True, limit=200, sort=sort, filter=filters
    )
    assert isinstance(resp, Response)
