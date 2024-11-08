'''
Deviance
=============

Methods described in this section relate to the deviance API.
These methods can be accessed at ``TenableIE.deviance``.

.. rst-class:: hide-signature
.. autoclass:: DevianceAPI
    :members:
'''
from typing import List, Dict, Union, Mapping
from restfly.utils import dict_clean
from tenable.ie.base.iterator import ADIterator
from tenable.ie.deviance.schema import DevianceSchema
from tenable.base.endpoint import APIEndpoint


class DevianceIterator(ADIterator):
    '''
    The deviance iterator provides a scalable way to work through list
    result sets of any size. The iterator will walk through each page of data,
    returning one record at a time. If it reaches the end of a page of
    records, then it will request the next page of information and then
    continue to return records from the next page (and the next, and the next)
    until the counter reaches the total number of records that the API has
    reported.
    '''


class DevianceAPI(APIEndpoint):
    _schema = DevianceSchema()

    def list(self,
             infrastructure_id: str,
             directory_id: str,
             **kwargs
             ) -> Union[List[Dict], DevianceIterator]:
        '''
        Retrieve all deviances for a directory

        Args:
            infrastructure_id (str):
                The infrastructure instance identifier.
            directory_id (str):
                The directory instance identifier.
            page (optional, int):
                The page number user wants to retrieve.
            per_page (optional, int):
                The number of records per page user wants to retrieve.
            batch_size (optional, int):
                The total number of records user wants to retrieve.
            last_identifier_seen (optional, int):
                The deviance identifier after which the deviance should be
                considered.
            resolved (optional, bool):
                is the deviance resolved?
            max_items (optional, int):
                The maximum number of items to return before
                stopping iteration.
            max_pages (optional, int):
                The maximum number of pages to request before throwing
                stopping iteration.

        Returns:
            list[dict] or DevianceIterator:
                An iterator that handles the page management of the requested
                records.

        Examples:
            return an iterator to loop through all records

            >>> for deviance in tie.deviance.list(
            ...     infrastructure_id='1',
            ...     directory_id='1',
            ...     resolved=True,
            ...     last_identifier_seen=1,
            ...     page=1,
            ...     per_page=10,
            ...     max_pages=11,
            ...     max_items=100
            ...     ):
            ...     pprint(deviance)

            return a list of requested records using batch_size

            >>> tie.deviance.list(
            ...     infrastructure_id='1',
            ...     directory_id='1',
            ...     resolved=True,
            ...     last_identifier_seen=1,
            ...     batch_size=100
            ...     )
        '''
        # create a dictionary of query parameters from kwargs
        # it contains all parameters required for iterator and additional
        # parameters allowed by api
        params = self._schema.dump(self._schema.load(kwargs))

        # setting api call url
        path = f'infrastructures/{infrastructure_id}/' \
               f'directories/{directory_id}/deviances'

        # if batch size is present then a direct call is done to API to get
        # total records requested by user else an iterator is returned to
        # loop through all records
        if params.get('batchSize'):
            # first we have to clean query param dictionary by removing
            # additional items if any
            params.pop('maxItems', None)
            params.pop('maxPages', None)
            return self._schema.load(
                self._api.get(path, params=params),
                many=True)
        else:
            # The iterator will start returning data from first page or
            # from page requested till last or until max pages or max items
            # are defined.
            return DevianceIterator(
                api=self._api,
                _path=path,
                num_pages=params.get('page') or 1,
                _per_page=params.get('perPage'),
                _query=params,
                _schema=self._schema,
                max_pages=params.pop('maxPages', None),
                max_items=params.pop('maxItems', None)
            )

    def get_history_details(self,
                            infrastructure_id: str,
                            directory_id: str,
                            deviance_id: str
                            ) -> Dict:
        '''
        Retrieve ad-object-deviance-history instance by id.


        Args:
            infrastructure_id (str):
                The infrastructure instance identifier.
            directory_id (str):
                The directory instance identifier.
            deviance_id (str):
                The deviance identifier.

        Return:
            dict:
                The deviance object.

        Example:
            >>> tie.deviance.history_details(
            ...     infrastructure_id='1',
            ...     directory_id='1',
            ...     deviance_id='1'
            ...     )
        '''
        return self._schema.load(
            self._api.get(f'infrastructures/{infrastructure_id}/'
                          f'directories/{directory_id}/'
                          f'deviances/{deviance_id}'))

    def update_history_details(self,
                               infrastructure_id: str,
                               directory_id: str,
                               deviance_id: str,
                               **kwargs
                               ) -> Dict:
        '''
        Retrieve ad-object-deviance-history instance by id.


        Args:
            infrastructure_id (str):
                The infrastructure instance identifier.
            directory_id (str):
                The directory instance identifier.
            deviance_id (str):
                The deviance identifier.
            ignore_until (optional, str(datetime)):
                Ignore deviance until defined date.

        Return:
            dict:
                The deviance object.

        Example:
            >>> tie.deviance.history_details(
            ...     infrastructure_id='1',
            ...     directory_id='1',
            ...     deviance_id='1',
            ...     ignore_until='2022-01-27T23:59:59.999Z'
            ...     )
        '''
        # created a payload dictionary for API call.
        payload = self._schema.dump(self._schema.load(kwargs))

        # let's make actual API call
        return self._schema.load(self._api.patch(
            f'infrastructures/{infrastructure_id}/'
            f'directories/{directory_id}/'
            f'deviances/{deviance_id}',
            json=payload))

    def list_by_directory_and_checker(self,
                                      profile_id: str,
                                      infrastructure_id: str,
                                      directory_id: str,
                                      checker_id: str,
                                      **kwargs
                                      ) -> DevianceIterator:
        '''
        Retrieve all deviances related to a single directory and checker

        Args:
            profile_id (str):
                The profile instance identifier.
            infrastructure_id (str):
                The infrastructure instance identifier.
            directory_id (str):
                The directory instance identifier.
            checker_id (str):
                The checker instance identifier.
            page (optional, str):
                The page number user wants to retrieve.
            per_page (optional, str):
                The number of records per page user wants to retrieve.
            max_items (optional, int):
                The maximum number of items to return before
                stopping iteration.
            max_pages (optional, int):
                The maximum number of pages to request before throwing
                stopping iteration.

        Returns:
            DevianceIterator:
                An iterator that handles the page management of the requested
                records.

        Examples:
            >>> for deviance in tie.deviance.list_by_directory_and_checker(
            ...     profile_id='1',
            ...     infrastructure_id='1',
            ...     dashboard_id='1',
            ...     checker_id='1',
            ...     page=1,
            ...     per_page=10,
            ...     max_pages=11,
            ...     max_items=100
            ...     ):
            ...     pprint(deviance)
        '''
        # create a dictionary of query parameters from kwargs
        # it contains all parameters required for iterator and additional
        # parameters allowed by api
        params = self._schema.dump(self._schema.load(kwargs))

        # setting api call url
        path = f'profiles/{profile_id}/infrastructures/{infrastructure_id}/' \
               f'directories/{directory_id}/checkers/{checker_id}/deviances'

        # The iterator will start returning data from first page or
        # from page requested till last or until max pages or max items
        # are defined.
        return DevianceIterator(
            api=self._api,
            _path=path,
            num_pages=params.get('page') or 1,
            _per_page=params.get('perPage'),
            _query=params,
            _schema=self._schema,
            max_pages=params.pop('maxPages', None),
            max_items=params.pop('maxItems', None)
        )

    def list_by_checker(self,
                        profile_id: str,
                        checker_id: str,
                        expression: Mapping,
                        **kwargs
                        ) -> Union[List[Dict], DevianceIterator]:
        '''
        Retrieve all deviances by checker

        Args:
            profile_id (str):
                The profile instance identifier.
            checker_id (str):
                The checker instance identifier.
            expression (mapping):
                An object describing a filter for searched items.
            batch_size (optional, int):
                The total number of records user wants to retrieve.
            last_identifier_seen (optional, int):
                The deviance identifier after which the deviance should be
                considered.
            page (optional, int):
                The page number user wants to retrieve.
            per_page (optional, int):
                The number of records per page user wants to retrieve.
            max_items (optional, int):
                The maximum number of items to return before
                stopping iteration.
            max_pages (optional, int):
                The maximum number of pages to request before throwing
                stopping iteration.

        Returns:
            list[dict] or DevianceIterator:
                An iterator that handles the page management of the requested
                records.

        Examples:
            return an iterator to loop through all records

            >>> for deviance in tie.deviance.list_by_checker(
            ...     profile_id='1',
            ...     checker_id='1',
            ...     expression={'OR': [{
            ...         'whencreated': '2021-07-29T12:27:50.0000000Z'
            ...     }]},
            ...     last_identifier_seen=1,
            ...     page=1,
            ...     per_page=10,
            ...     max_pages=11,
            ...     max_items=100
            ...     ):
            ...     pprint(deviance)

            return a list of requested records using batch_size

            >>> tie.deviance.list_by_checker(
            ...     profile_id='1',
            ...     checker_id='1',
            ...     expression={'OR': [{
            ...         'whencreated': '2021-07-29T12:27:50.0000000Z'
            ...     }]},
            ...     last_identifier_seen=1,
            ...     batch_size=100
            ...     )
        '''
        # create a dictionary of query parameters from kwargs
        # it contains all parameters required for iterator and additional
        # parameters allowed by api
        params = self._schema.dump(self._schema.load(dict_clean(kwargs)))

        # create a payload dictionary
        payload = self._schema.dump(
            self._schema.load({'expression': expression}))

        # setting api call url
        path = f'profiles/{profile_id}/checkers/{checker_id}/deviances'

        # if batch size is present then a direct call is done to API to get
        # total records requested by user else an iterator is returned to
        # loop through all records
        if params.get('batchSize'):
            # first we have to clean query param dictionary by removing
            # additional items if any
            params.pop('maxItems', None)
            params.pop('maxPages', None)
            return self._schema.load(
                self._api.post(path, params=params, json=payload),
                many=True)
        else:
            # The iterator will start returning data from first page or
            # from page requested till last or until max pages or max items
            # are defined.
            return DevianceIterator(
                api=self._api,
                _path=path,
                _method='post',
                num_pages=params.get('page') or 1,
                _per_page=params.get('perPage'),
                _query=params,
                _payload=payload,
                _schema=self._schema,
                max_pages=params.pop('maxPages', None),
                max_items=params.pop('maxItems', None)
            )

    def update_by_checker(self,
                          profile_id: str,
                          checker_id: str,
                          ignore_until: str
                          ) -> None:
        '''
        Update instances matching a checker id.

        Args:
            profile_id (str):
                The profile instance identifier.
            checker_id (str):
                The checker instance identifier.
            ignore_until (str(datetime)):
                Ignore deviance until defined date.

        Return:
            None:

        Example:
            >>> tie.deviance.update_by_checker(
            ...     profile_id='1',
            ...     checker_id='1',
            ...     ignore_until='2022-01-27T23:59:59.999Z'
            ...     )
        '''
        # created a payload dictionary required for api call
        payload = self._schema.dump(self._schema.load({
            'ignoreUntil': ignore_until
        }))

        # let's make actual API call
        self._api.patch(
            f'profiles/{profile_id}/checkers/{checker_id}/deviances',
            json=payload)

    def search(self,
               profile_id: str,
               checker_id: str,
               ad_object_id: str,
               show_ignored: bool,
               **kwargs
               ) -> DevianceIterator:
        '''
        Search all deviances by profile by checker by AD object.

        Args:
            profile_id (str):
                The profile instance identifier.
            checker_id (str):
                The checker identifier.
            ad_object_id (str):
                The AD object identifier.
            show_ignored (bool):
                Whether ignored deviances should be included?
            date_start (optional, str(datetime)):
                The date after which the deviances should have been emitted.
            date_end (optional, str(datetime)):
                The date before which the deviances should have been emitted.
            page (optional, int):
                The page number user wants to retrieve.
            per_page (optional, int):
                The number of records per page user wants to retrieve.
            max_items (optional, int):
                The maximum number of items to return before
                stopping iteration.
            max_pages (optional, int):
                The maximum number of pages to request before throwing
                stopping iteration.

        Return:
            DevianceIterator:
                An iterator that handles the page management of the requested
                records.

        Example:
            >>> for deviance in tie.deviance.search(
            ...     profile_id='1',
            ...     checker_id='1',
            ...     ad_object_id='1',
            ...     show_ignored=True,
            ...     page=1,
            ...     per_page=10,
            ...     max_pages=11,
            ...     max_items=100
            ...     ):
            ...     pprint(deviance)
        '''
        # create a dictionary of query parameters from kwargs
        # it contains all parameters required for iterator and additional
        # parameters allowed by api
        params = self._schema.dump(self._schema.load({
            'perPage': kwargs.get('per_page'),
            'page': kwargs.get('page'),
            'maxItems': kwargs.get('max_items'),
            'maxPages': kwargs.get('max_pages')
        }))

        # create a payload dictionary and clean additional None values
        payload = self._schema.dump(self._schema.load(
            dict_clean({
                'dateStart': kwargs.get('date_start'),
                'dateEnd': kwargs.get('date_end'),
                'showIgnored': show_ignored
            })
        ))

        # setting api call url
        path = f'profiles/{profile_id}/checkers/{checker_id}/' \
               f'ad-objects/{ad_object_id}/deviances'

        # The iterator will start returning data from first page or
        # from page requested till last or until max pages or max items
        # are defined.
        return DevianceIterator(
            api=self._api,
            _path=path,
            _method='post',
            num_pages=params.get('page') or 1,
            _per_page=params.get('perPage'),
            _query=params,
            _payload=payload,
            _schema=self._schema,
            max_pages=params.pop('maxPages', None),
            max_items=params.pop('maxItems', None)
        )

    def update_on_ado_and_checker(self,
                                  profile_id: str,
                                  checker_id: str,
                                  ad_object_id: str,
                                  ignore_until: str
                                  ) -> None:
        '''
        Update the deviances emitted on a specific AD object and
        for specific checker.

        Args:
            profile_id (str):
                the profile instance identifier.
            checker_id (str):
                The checker instance identifier.
            ad_object_id (str):
                The AD object instance identifier.
            ignore_until (str(datetime)):
                Ignore deviance until defined date.

        Return:
            None:

        Example:
            >>> tie.deviance.update_on_ado_and_checker(
            ...     profile_id='1',
            ...     checker_id='1',
            ...     ad_object_id='1',
            ...     ignore_until='2022-01-27T23:59:59.999Z'
            ...     )
        '''
        # created a payload dictionary for API call
        payload = self._schema.dump(self._schema.load({
            'ignoreUntil': ignore_until
        }))

        # let's make actual API call
        self._api.patch(f'profiles/{profile_id}/'
                        f'checkers/{checker_id}/'
                        f'ad-objects/{ad_object_id}/deviances',
                        json=payload)
