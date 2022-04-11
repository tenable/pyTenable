'''
Vulnerability
=============

The following methods allow for interaction of VM vulnerabilities into
Tenable.io
:devportal:`vulnerabilities <vulnerabilities>` API.

Methods available on ``tio.v3.vm.vulnerabilities``:

.. rst-class:: hide-signature
.. autoclass:: VulnerabilityAPI
    :members:
'''

from typing import Dict, List, Optional, Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.vulnerabilities.schema import VulnerabilitySchema
from tenable.utils import dict_clean


class VulnerabilityAPI(ExploreBaseEndpoint):
    '''
    API class containing all the methods related to VM Vulnerability.
    '''
    _path = 'api/v3/findings'
    _conv_json = True
    _schema = VulnerabilitySchema()

    def import_vulnerability(self,
                             vendor: str,
                             data_type: str,
                             source: str,
                             assets: List,
                             product: Optional[str] = None,
                             coverage:  Optional[str] = None
                             ) -> Dict:
        '''
        The import vulnerability methods

        Args:
            vendor (str):
                The company that owns the product that is the source of the
                vulnerability data.

                >>> tenable — A Nessus scan identified the vulnerabilities you
                ... want to import. Use this value for all Nessus scans,
                ... regardless of the scan manager (Tenable.io, Tenable.sc, or
                ... Nessus Manager).

            data_type (str):
                Type field must contain one of these values:

                >>> 'vm' or 'was'

            source (str):
                The source field needs to have two parts, scan id and
                chunk id, split by ':'

                >>> ('75c6c4c3-1626-4b57-9095-71b58ff8999e:'
                ...     'e9b89d18-87cc-4fd5-8e6f-27a1d24fa2ac0')

            assets (list):
                An array of asset objects with vulnerabilities information.
                A valid asset record requires at least one valid
                network_interface object.

                Note: Tenable.io supports a maximum of 50 individual asset
                objects per request message. In addition, because Tenable.io
                supports a total size limit of 15 MB for the request message
                , you may want to limit the number of asset objects you
                include in an individual request, depending on the number of
                vulnerabilities identified on the assets and the size of the
                related vulnerability output.

                Note: This endpoint does not support the network_id attribute
                in asset objects for import. Tenable.io automatically assigns
                imported assets to the default network object. For more
                information about network objects, see Manage Networks.

                For each asset Host requires at least one of
                [ipv4, netbios_name, fqdn, tenable_agent_id, qualys_host_id,
                or qualys_asset_id].

                Example:
                    >>>  [{
                    ...  'network_interfaces': {
                    ...      'ipv4': ['192.0.2.57', '192.0.2.177']
                    ...  },
                    ...  'hostname': 'windsmb.server.example.com',
                    ...  'bios_uuid': '9c60da51-762a-4b9b-8504-411056c2f696',
                    ...  'netbios_name': 'JUPITER',
                    ...  'vulnerabilities': [{
                    ...      'tenable_plugin_id': '97737',
                    ...      'last_found': 1568086236,
                    ...      'output': ('Description: The remote Windows host
                    ...          is missing a security update.')
                    ...  }]
                    ... }]

            product (str, optional):
                The name of the product from the vendor that is the source of
                the vulnerability data being imported.

                >>> tenable.io — The vulnerability data source is Tenable.io.

            coverage (str, optional):
                A string or range of IDs that each represents a check that
                the scan used to detect vulnerabilities you are importing.
                This parameter supports Tenable plugin checks only.
                For more information, see https://www.tenable.com/plugins.

                >>> '24531,76010-76023,88107'

        Returns:
            :obj:`dict`: {'job_uuid':''}
            This attribute is always empty.
            An empty value does not indicate an error condition.

        Examples:
            >>> tio.v3.vm.vulnerabilities.import_vulnerability(
            ...    vendor=vendor
            ...    product=product
            ...    data_type=data_type
            ...    source=source
            ...    assets=assets
            ...    coverage=coverage
            ... )
        '''
        data = {
            'vendor': vendor,
            'data_type': data_type,
            'source': source,
            'assets': assets,
            'product': product,
            'coverage': coverage
        }
        payload = self._schema.dump(self._schema.load(dict_clean(data)))
        payload['coverage'] = {'ids': coverage}
        return self._post('types/host', json=payload)

    def search(self,
               **kw
               ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Search and retrieve the VM Vulnerabilities based on supported
        conditions.

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
                the :py:meth:`tio.v3.definitions.vm.vulnerabilities()`
                endpoint to get more details.

            sort (list[tuple], optional):
                A list of dictionaries describing how to sort the data
                that is to be returned.

                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]

            limit (int, optional):
                Number of objects to be returned in each request.
                Default and max_limit is 200.

            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.

            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object as is to the user.

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
            >>> tio.v3.vm.vulnerabilities.search(
            ... filter=('id', 'eq', '00089a45-44a5-4620-bf9f-75ebedc6cc6c'),
            ... fields=['id'], limit=2)
        '''
        api_path = 'vulnerabilities/host/search'
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(iterator_cls=iclass,
                               sort_type=self._sort_type.property_based,
                               api_path=f'{self._path}/{api_path}',
                               resource='findings',
                               **kw
                               )
