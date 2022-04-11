'''
Connectors
==========

The following methods allow for interaction into the Tenable.io
:devportal:`connectors <connectors>` API endpoints.

Methods available on `` tio.v3.connectors``:

.. rst-class:: hide-signature
.. autoclass:: ConnectorsAPI
    :members:
'''
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.connectors.schema import (ConnectorCreateOrEditSchema,
                                             ConnectorListTrails)
from tenable.utils import dict_clean, dict_merge


class ConnectorsAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Connectors API
    '''

    _path = 'api/v3/connectors'
    _conv_json = True

    def create(self,
               name: str,
               con_type: str,
               network_id: Optional[str] = None,
               schedule: Optional[Dict] = None,
               **params: Dict
               ) -> Dict:
        '''
        Create a connector.

        :devportal:`connectors: create <connectors-create>`

        Args:
            name (str):
                The name of the connector to create.
            con_type (str):
                The type of connector to create.
                Example:
                    'aws_keyless'
            schedule (str, optional):
                The data import schedule
                Example:
                    >>> ('days', 2)
            network_id (str, optional):
                The UUID for network
            **params (dict):
                The various parameters that can be passed to the connector
                creation API.  Examples would be sub_accounts, access_key,
                etc. For more detailed information, please refer to API
                documentation linked above.  Further, any keyword arguments
                passed that are not explicitly documented will be
                automatically appended to the params document.  There is
                no need to pass params directly.

        Returns:
            :obj:`dict`:
                The connector resource record.

        Example:
        >>> resp = tio.v3.connectors.create(
        ...     name='test', con_type='aws_keyless',
        ...     network_id='00000000-0000-0000-0000-000000000000',
        ...     schedule=('days', 2), sub_accounts=[{}]
        ...     )
        '''

        payload = {
            'name': name,
            'type': con_type,
            'network_id': network_id,
            'schedule': schedule,
            'params': params
        }
        payload = dict_clean(payload)
        schema = ConnectorCreateOrEditSchema()
        payload = schema.dump(schema.load(payload))
        payload = {'connector': payload}
        return self._post(json=payload)['connector']

    def list_aws_cloudtrails(self,
                             region: List[Tuple],
                             account_id: Optional[str] = None,
                             credentials: Optional[Dict] = None
                             ) -> Dict:
        '''
        List the AWS cloudtrails.

        :devportal:`connectors: list_aws_cloudtrails <connectors-list_aws_cloudtrails>` # noqa E501

        Args:
            region (list(tuple)):
                Complete list of aws available
                name (str):
                    The AWS region code, for example, us-east-1.
                     The value of All indicates that the cloudtrail is
                     associated with all AWS available regions.

                friendly_name (str):
                    The AWS region name, for example, US East (N. Virginia).
                    The value of All indicates that the cloudtrail is
                    associated with all AWS available regions.
                Examples:
                    >>> [('us-east-1', 'US East (N. Virginia)')]
            credentials (dict, optional):
                The credentials that the Tenable.io connector uses to
                communicate with the AWS API, including access_key
                and secret_key.

                Examples:
                    >>> {
                    ... 'access_key':
                    ... 'd08c2a75517ad18da1d1d2e8f9ea70792f658674b352a9a00e7fcc4a74dcff6a',  # noqa E501
                    ... 'secret_key':
                    ... 'be13082452f57880261e8170290490026417745b8cde8a7d1e554d16eff690bf'  # noqa E501
                    ... }
            account_id (str, optional):
                For keyless AWS connectors, the AWS account ID.

        Returns:
            :obj:`dict`:
                The connector resource record.

        Example:
            >>> resp = api.v3.connectors.list_aws_cloudtrails(
            ...     region=[('All', 'All')], credentials={
            ...     'access_key': 'fasd7fs897df98asdf79a8sd9f',
            ...     'secret_key': 'hfghty7fs897df98asdf79a8sd9f'
            ...     }
            ... )
        '''

        payload = {
            'region': region,
            'credentials': credentials,
            'account_id': account_id
        }
        payload = dict_clean(payload)
        schema = ConnectorListTrails()
        payload = schema.dump(schema.load(payload))
        return self._post('aws/cloudtrails', json=payload)['trails']

    def delete(self, connector_id: UUID) -> None:
        '''
        Deletes a connector.

        :devportal:`connectors: delete <connectors-delete>`

        Args:
            connector_id (uuid.UUID):
                The unique identifier for the connector to delete.

        Returns:
            :obj:`None`:
                The connector has been successfully deleted.

        Examples:
            >>>  tio.v3.connectors.delete(
            ... 'b5db63f1-551d-4789-aefa-9629c93ddc45')
        '''
        self._delete(f'{connector_id}')

    def details(self, connector_id: UUID) -> Dict:
        '''
        Retrieves the details about a connectors.

        :devportal:`connectors: details <connectors-details>`

        Args:
            connector_id (uuid.UUID):
                The unique identifier for the connectors.

        Returns:
            :obj:`dict`:
                The connectors resource record.

        Examples:
            >>> connector =  tio.v3.connectors.details(
            ... 'b5db63f1-551d-4789-aefa-9629c93ddc45')
            >>> pprint(connector)
        '''
        return super()._details(connector_id)['connector']

    def download_template(self, connector_id: UUID) -> Dict:
        '''
        Retrieves the ARM templates about a connector.

        :devportal:`connectors: template <connectors-template>`

        Args:
            connector_id (uuid.UUID):
                The unique identifier for the connectors.

        Returns:
            :obj:`dict`:
                The connectors resource record.

        Examples:
            >>> connector =  tio.v3.connectors.download_template(
            ... 'b5db63f1-551d-4789-aefa-9629c93ddc45')
            >>> pprint(connector)
        '''
        return self._get(f'azure_fa/{connector_id}/arm-template')

    def import_data(self, connector_id: UUID) -> Dict:
        '''
        Retrieves the data about a connector.

        :devportal:`connectors: import_data <connectors-import_data>`

        Args:
            connector_id (uuid.UUID):
                The unique identifier for the connectors.

        Returns:
            :obj:`dict`:
                The connectors resource record.

        Examples:
            >>> connector =  tio.v3.connectors.import_data(
            ... 'b5db63f1-551d-4789-aefa-9629c93ddc45')
            >>> pprint(connector)
        '''
        return self._post(f'{connector_id}/import')['connector']

    def edit(self,
             connector_id: UUID,
             name: str,
             schedule: Optional[tuple] = None,
             network_id: Optional[str] = None,
             **params: Dict
             ) -> None:
        '''
        Modifies a connectors.

        :devportal:`connectors: edit <connectors-edit>`


        Args:
            connector_id (uuid.UUID):
                The UUID for connector
            name (str):
                The name of the connector to create.
            schedule (tuple, optional):
                The data import schedule
                Example:
                    >>> ('days', 2)
            network_id (str, optional):
                The unique identifier for networks
            **params:
                The various parameters that can be passed to the connector
                edit API.  Examples would be sub_accounts, access_key,
                etc. For more detailed information, please refer to API
                documentation linked above.  Further, any keyword arguments
                passed that are not explicitly documented will be
                automatically appended to the params document.  There is
                no need to pass params directly.

        Returns:
            :obj:`dict`:
                The connector resource record.

        Examples:
            >>>  tio.v3.connectors.edit(
            ... 'b5db63f1-551d-4789-aefa-9629c93ddc45', 'New Group Name',
            ... import_config=True, auto_discovery=False)
        '''
        payload = {
            'name': name,
            'network_id': network_id,
            'params': params,
            'schedule': schedule

        }
        payload = dict_clean(payload)
        schema = ConnectorCreateOrEditSchema()
        payload = schema.dump(schema.load(payload))

        connector_info = self.details(connector_id)
        payload = dict_merge(
            {
                'name': connector_info.get('name'),
                'network_id': connector_info.get('network_id'),
                'params': connector_info.get('params'),
                'schedule': connector_info.get('schedule')
            },
            payload
        )

        payload = {'connector': payload}
        return self._put(f'{connector_id}', json=payload)['connector']

    def search(self,
               **kw
               ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Retrieves the connectors.

        Args:
            fields (list, optional):
                The list of field names to return from the Tenable API.
                Example:
                    >>> ['field1', 'field2']
            filter (tuple, dict, optional):
                A nestable filter object detailing how to filter the results
                down to the desired subset.
                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...                 ('test', 'oper', '2')
                    ...             ),
                    ...     'and', ('test', 'oper', 3)
                    ... )
                    >>> {
                    ...  'or': [{
                    ...      'and': [{
                    ...              'value': '1',
                    ...              'operator': 'oper',
                    ...              'property': '1'
                    ...          },
                    ...          {
                    ...              'value': '2',
                    ...              'operator': 'oper',
                    ...              'property': '2'
                    ...          }
                    ...      ]
                    ...  }],
                    ...  'and': [{
                    ...      'value': '3',
                    ...      'operator': 'oper',
                    ...      'property': 3
                    ...  }]
                    ... }
                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth: `tio.v3.definitions.vm.connectors()` endpoint
                to get more details.

            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            limit (int, optional):
                Number of objects to be returned in each request.
                Default limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
        Returns:
            Iterable:
                The iterable that handles the pagination for the job.
            requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.
        Examples:
            >>> tio.v3.connectors.search(
            ...     filter=('name','eq','test'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('field', 'asc')]
            ... )
        '''
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='connectors',
                               iterator_cls=iclass,
                               api_path=f'{self._path}/search',
                               **kw
                               )
