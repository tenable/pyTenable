"""
Data Export Helper
==================

The methods exposed within the export module are designed to mimick the same
structure that Tenable Vulnerability Management uses for exporting data.
These methods ultimately translate to GraphQL queries and then are fed to the
Tenable OT API.

.. rst-class:: hide-signature
.. autoclass:: ExportsAPI
    :members:
"""
from typing import List, Dict, Optional, Union, Any
from tenable.base.endpoint import APIEndpoint
from tenable.ot.exports.iterator import OTExportsIterator, OTFindingsIterator
from tenable.ot.exports import queries


class ExportsAPI(APIEndpoint):
    def _list(self,
              query: str,
              model: str,
              limit: int = 200,
              return_json: bool = False,
              filter_type: str = 'And',
              filters: Optional[List[Dict]] = None,
              default_filters: Optional[List[Dict]] = None,
              sort: Optional[List[Dict]] = None,
              search: Optional[str] = None,
              start_at: Optional[str] = None,
              iterable: Optional[Any] = OTExportsIterator,
              **kwargs
              ) -> Any:
        """
        Base listing method to be used for the exports.

        Args:
            query (str): The GraphQL Query to run
            model (str):
                The GraphQL Model that is to be returned from the API.  This
                name is what is used by the iterator to traverse the data
                page.
            limit (int, optional):
                The number of objects to be returned per page.
            sort (list[dict], optional):
                A list of sort parameters to be passed to sort the responses.
            search (str, optional):
                Search string
            start_at (str, optional):
                Start returning data after this object id.
            filters (list[dict], optional):
                List of filters to apply to restict the response to only the
                desired items.
            filter_type (str, optional):
                When passing multiple filters, how should the filters be
                applied to the dataset?  Acceptable values are `And` and `Or`.
            return_json (bool, optional):
                If `True`, then the instead of an iterator, the json response
                will be returned instead.
            default_filters (list[dict], optional):
                The default filters to appllied to the query first.  This is
                mainly used by the caller as part of passing through the
                filters parameter as well.
            iterable: (object, optional):
                The iterable object to return to the caller.

        Returns:
            Union[OTExportsIterator, dict]:
                By default the method will return an iterator that will handle
                pagination and return a single item at a time.  If return_json
                is set to `True` however, then the JSON response will be
                returned instead for that page.
        """
        default_filters = [] if default_filters is None else default_filters
        filters = [] if filters is None else filters
        sort = [] if sort is None else sort

        # Iterate over the default filters and add them to the filter list
        # if they don't exist.
        for default_filter in default_filters:
            field = default_filter['field']
            if field not in [f.get('field') for f in filters]:
                filters.append(default_filter)

        filter = filters[0] if filters else None
        if len(filters) > 1:
            filter = {
                'op': 'And',
                'expressions': filters
            }

        variables = {
            'search': search,
            'sort': sort,
            'startAt': start_at,
            'limit': limit,
            'filter': filter,
        }

        if return_json:
            return self._api.query(query=query,
                                   variables=variables,
                                   **kwargs
                                   )
        return iterable(self._api,
                        _model=model,
                        _query=query,
                        _variables=variables,
                        **kwargs
                        )

    def assets(self,
               filters: Optional[List[Dict]] = None,
               sort: Optional[List[Dict]] = None,
               search: Optional[str] = None,
               start_at: Optional[str] = None,
               limit: int = 200,
               filter_type: str = 'And',
               return_json: bool = False,
               ) -> Union[OTExportsIterator, Dict]:
        """
        Assets Export

        Args:
            limit (int, optional):
                The number of objects to be returned per page.
            sort (list[dict], optional):
                A list of sort parameters to be passed to sort the responses.
            search (str, optional):
                Search string
            start_at (str, optional):
                Start returning data after this object id.
            filters (list[dict], optional):
                List of filters to apply to restict the response to only the
                desired items.
            filter_type (str, optional):
                When passing multiple filters, how should the filters be
                applied to the dataset?  Acceptable values are `And` and `Or`.
            return_json (bool, optional):
                If `True`, then the instead of an iterator, the json response
                will be returned instead.

        Returns:
            Union[OTExportsIterator, dict]:
                By default the method will return an iterator that will handle
                pagination and return a single item at a time.  If return_json
                is set to `True` however, then the JSON response will be
                returned instead for that page.

        Example:

            >>> for asset in tot.exports.assets():
            ...    print(asset)
        """
        default_filters = [
            {'op': 'Equal', 'field': 'hidden', 'values': 'false'}
        ]
        default_sort = [
            {'field': 'risk', 'direction': 'DescNullLast'},
            {'field': 'id', 'direction': 'AscNullLast'},
        ]
        sort = default_sort if sort is None else sort
        return self._list(query=queries.ASSETS,
                          model='assets',
                          filters=filters,
                          default_filters=default_filters,
                          sort=sort,
                          search=search,
                          start_at=start_at,
                          limit=limit,
                          filter_type=filter_type,
                          return_json=return_json,
                          )

    def plugins(self,
                filters: Optional[List[Dict]] = None,
                sort: Optional[List[Dict]] = None,
                search: Optional[str] = None,
                start_at: Optional[str] = None,
                limit: int = 200,
                filter_type: str = 'And',
                return_json: bool = False,
                ) -> Union[OTExportsIterator, Dict]:
        """
        Plugin Export

        Args:
            limit (int, optional):
                The number of objects to be returned per page.
            sort (list[dict], optional):
                A list of sort parameters to be passed to sort the responses.
            search (str, optional):
                Search string
            start_at (str, optional):
                Start returning data after this object id.
            filters (list[dict], optional):
                List of filters to apply to restict the response to only the
                desired items.
            filter_type (str, optional):
                When passing multiple filters, how should the filters be
                applied to the dataset?  Acceptable values are `And` and `Or`.
            return_json (bool, optional):
                If `True`, then the instead of an iterator, the json response
                will be returned instead.

        Returns:
            Union[OTExportsIterator, dict]:
                By default the method will return an iterator that will handle
                pagination and return a single item at a time.  If return_json
                is set to `True` however, then the JSON response will be
                returned instead for that page.

        Example:

            >>> for plugin in tot.exports.plugins():
            ...    print(plugin)
        """
        return self._list(query=queries.PLUGINS,
                          model='plugins',
                          filters=filters,
                          sort=sort,
                          search=search,
                          start_at=start_at,
                          limit=limit,
                          filter_type=filter_type,
                          return_json=return_json,
                          )

    def findings(self,
                 filters: Optional[List[Dict]] = None,
                 sort: Optional[List[Dict]] = None,
                 search: Optional[str] = None,
                 start_at: Optional[str] = None,
                 limit: int = 200,
                 filter_type: str = 'And',
                 return_json: bool = False,
                 ) -> Union[OTExportsIterator, Dict]:
        """
        Findings Export

        Args:
            sorted (list[dict], optional):
                A list of asset sort parameters to be passed to sort the
                responses.
            search (str, optional):
                Asset Search string
            filters (list[dict], optional):
                List of asset filters to apply to restict the response to only
                the desired assets.
            filter_type (str, optional):
                When passing multiple filters, how should the filters be
                applied to the dataset?  Acceptable values are `And` and `Or`.

        Returns:
            OTFindingsIterator:
                The Iterable that hadles the more complex logic of gathering
                the findings for each asset and presenting them to the caller.

        Example:

            >>> for finding in tot.exports.findings():
            ...    print(finding)
        """

        assets = self._list(query=queries.FINDING_ASSETS,
                            filters=filters,
                            model='assets',
                            sort=sort,
                            search=search,
                            limit=1000,
                            filter_type=filter_type,
                            return_json=return_json,
                            )
        return OTFindingsIterator(self._api, _assets=assets)
