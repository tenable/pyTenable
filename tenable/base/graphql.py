"""
GraphQL Base Module
===================

The GraphQL module offers a simple yet flexible interface to wrap any Tenable GraphQL
applications into the pyTenable SDK.

.. autoclass:: GraphQLSession
    :members:

.. autoclass:: GraphQLEndpoint
    :members:
    :private-members:

.. autoclass:: GraphQLIterator
    :members:
"""
from typing import Dict, Optional, Union, Any, List
from io import StringIO
import os
import sys
import logging
import platform
from pathlib import Path
from restfly.iterator import APIIterator
from tenable.version import version
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from graphql import DocumentNode, validate


class GraphQLIterator(APIIterator):
    """
    An iterator class to be used with GraphQL paginated/iterable datasets.
    """
    _api: 'GraphQLSession'
    model: str
    query: DocumentNode
    variables: Dict[str, Any]
    next_token: Optional[str] = None

    def _transform(self, data: Dict) -> List[Dict[str, Any]]:
        """
        Data transformation method.  Performs any necessary conversion,
        flattening, or data restructuring before returning a list of items
        to be consumed by the iterator.
        """
        return data[self.model].get('nodes', [])

    def _get_page_tokens(self, data: Dict) -> None:
        """
        Handles storage of any page-based attributes needed to assist the
        iterator.  Things like the endCursor, count totals, etc.
        """
        if data[self.model]['pageInfo'].get('hasNextPage'):
            self.next_token = data[self.model]['pageInfo'].get('endCursor')
        else:
            self.next_token = None

    def _get_next_item(self) -> Dict:
        """
        Returns the next item in the page
        """
        return self[self.page_count]

    def _increment_counters(self) -> None:
        """
        Handles incrementing all of the counters that are controlling the next
        item to be retreived.
        """
        self.count += 1
        self.page_count += 1

    def _get_page(self) -> None:
        """
        Fetches the next page of data.  Will raise a StopIteration if there
        are no more pages to consume.
        """
        if self.next_token:
            self.variables['startAt'] = self.next_token
        elif not self.next_token and self.page_count > 0:
            raise StopIteration()
        resp = self._api.query(self.query, **self.variables)
        self.raw = resp
        self._get_page_tokens(resp)
        self.page = self._transform(resp)

    def next(self) -> Any:
        """
        Ask for the next record
        """
        # If there are no more records to return, then we should raise a
        # StopIteration exception to break the iterator out.
        if (
            (self.total and self.count + 1 > self.total)  # noqa: PLR0916
            or (self.max_items and self.count >= self.max_items)
        ):
            raise StopIteration()

        # If we have worked through the current page of records and we still
        # haven't hit to the total number of available records, then we should
        # query the next page of records.
        if (
            self.page_count >= len(self.page)
            and (not self.total or self.count + 1 <= self.total)
        ):
            if (self.max_pages and self.num_pages >= self.max_pages):
                raise StopIteration()

            # Perform the _get_page call.
            self._get_page()
            self.page_count = 0
            self.num_pages += 1

            # If the length of the page is 0, then we don't have anything
            # further to do and should stop iteration.
            if len(self.page) == 0:
                raise StopIteration()

        # Get the relevant record, increment the counters, and return the
        # record.
        item = self._get_next_item()
        self._increment_counters()
        return item



class GraphQLEndpoint:
    """
    A GraphQL Endpoint class to be used in-place of the Restfly-base endpoint
    adaptor.
    """
    def __init__(self, api: 'GraphQLSession'):
        self._api = api
        self._log = api._log

    def _query(self, *args, **kwargs) -> Union[Dict[str, Any], GraphQLIterator]:
        """Simple helper to call the api query"""
        return self._api.query(*args, **kwargs)


class GraphQLSession:
    """
    GraphQL API Session handler using the official GQL python library instead
    of Restfly.

    Attributes:
        _query_folder (Path):
            The location to where stored query files exist.  Because of how
            Parent-Child relationships work within python and how that effects
            file locations, this MUST be set within the child class.  This
            should almost _always_ be set to:
            `Path(__file__).parent.joinpath('queries')`
        _base_path (str):
            The URI path (excluding the root `/`) to where the GraphQL API
            resides.
        _env_base (str):
            The environment variable prefix for the library.
        _client (gql.Client):
            Set as part of initialization, however is the GQL library client
            that will be used to interface to the GQL API.
    """

    _query_folder: Path
    _base_path: str = ''
    _env_base: str = ''
    _client: Client

    def __init__(self,
                 url: Optional[str] = None,
                 api_key: Optional[str] = None,
                 verify: bool = True,
                 schema_validation: bool = True,
                 retries: int = 3,
                 timeout: int = 300,
                 vendor: str = 'unknown',
                 product: str = 'unknown',
                 build: str = 'unknown',
                 ):
        """
        Creates a new GraphQLSession object

        Args:
            url (str):
                The base URL to use for interfacing to the GraphQL API.
            api_key (str):
                The API key to use to authroize all interactions with the
                remote API.
            verify (bool, True):
                Should SSL certificate verification be performed?
            retires (int, 3):
                How many times should we retry a failed API call before
                giving up?
            timeout (int, 300):
                How long should we wait in seconds before raising a
                ConnectionError?
            vendor (str, optional):
                Identifies the vendor of the integration making the call to
                the API.  This is used as part of the User-Agent construction.
            product (str, optional):
                Identifies the product of the integration making the call to
                the API.  This is used as part of the User-Agent construction.
            build (str, optional):
                Identifies the build of the integration making the call to
                the API.  This is used as part of the User-Agent construction.
        """
        self._log = logging.getLogger(
            f'{self.__module__}.{self.__class__.__name__}'
        )
        if not url:
            url = os.environ.get(f'{self._env_base}_URL')
        if not api_key:
            api_key = os.environ.get(f'{self._env_base}_API_KEY')

        if not api_key or not url:
            raise ConnectionError(
                f'Invalid connection settings: url="{url}", api_key="{api_key}"'
            )

        headers = {
            **self._authorization(api_key),
            **self._build_session(vendor, product, build)
        }
        transport = RequestsHTTPTransport(url=f'{url}/{self._base_path}',
                                          verify=verify,
                                          retries=retries,
                                          headers=headers
                                          )
        self._client = Client(transport=transport,
                              fetch_schema_from_transport=schema_validation,
                              execute_timeout=timeout,
                              )

    def _build_session(self,
                       vendor: str = 'unknown',
                       product: str = 'unknown',
                       build: str = 'unknown'
                       ) -> Dict:
        """
        Handles initial header setup for things such as user-agent
        """
        uname = platform.uname()
        py_version = '.'.join([str(i) for i in sys.version_info][0:3])
        opsys = uname[0]
        arch = uname[-2]
        return {
            'User-Agent': (
                f'Integration/1.0 ({vendor.strip(";")}; '
                f'{product.strip(";")}; '
                f'Build/{build.strip(";")}) '
                f'pyTenable/{version} (GQL-Requests; '
                f'Python/{py_version}; {opsys}/{arch})'
            )
        }

    def _authorization(self, api_key: str) -> Dict:
        """
        API Authorization stub
        """
        return {}

    def construct_query(self,
                        query: Optional[Union[str,
                                              StringIO,
                                              DocumentNode
                                              ]] = None,
                        stored_file: Optional[str] = None
                        ) -> DocumentNode:
        """
        The query constructor takes any of the input types given and will
        return a DocumentNode containing the GraphQL query to be used with the
        query method.

        As this method is called by both the query and validate methods
        directly, there generally isn't a need to call this outside of those
        two methods.

        Args:
            query (str | StringIO | DocumentNode, optional):
                The query obj that we want to normalize into a DocumentNode.
            stored_file (str, optional):
                The filename of a vendored (stored) graphql query to construct.

        Returns:
            DocumentNode
        """
        if query and isinstance(query, StringIO):
            return gql(query.read())
        elif query and isinstance(query, str):
            return gql(query)
        elif query and isinstance(query, DocumentNode):
            return query
        elif not query and stored_file:
            queryfile = self._query_folder.joinpath(stored_file)
            with queryfile.open('r', encoding='utf-8') as fobj:
                query_obj = gql(fobj.read())
            return query_obj
        else:
            raise TypeError(
                f'No query was presented query="{query}", stored_file="{stored_file}"'
            )

    def query(self,
              query: Optional[str] = None,
              stored_file: Optional[str] = None,
              keyword_arguments: Optional[Dict[str, Any]] = None,
              iterator: Optional[GraphQLIterator] = None,
              graphql_model: Optional[str] = None,
              **variables: Any
              ) -> Dict[str, Any]:
        """
        Query the GraphQL API

        Args:
            query (str | StringIO | DocumentNode, optional):
                The GraphQL query to pass to the remote API.
            stored_file (str, optional):
                The filename of a vendored (stored) graphql query to construct.

                .. note::
                    This parameter should not need to be used for outside of the
                    library itself.  All of the queries available with this parameter
                    are also wrapped within the endpoint classes.

            iterator (GraphQLIterator, optional):
                If specified, the response will be an instance of this iterable
                instead of the dictionary response.  Useful for when the
                response data is expected to be larger datasets that would
                require multiple pages to collect all of the data.
            graphql_model (str, optional):
                When using the iterator, we need to specify the base entity
                that is returned from the GraphQL response.
            keyword_argument (dict, optional):
                Anything specified within this dictionary will be passed on
                to the gql libraries query method.  While not expected to be
                commonly used, we're exposing this here just incase we need it.
            **variables (dict, optional):
                Any variable declarations that need to be passed along with
                the query.

        Returns:
            Dict:
                If no iterator is passed, then the response dictionary is
                returned to the caller.
            GraphQLIterator:
                If an iterator class was passed, then the query is generated
                and the passed to the iterator nefore returning an instance
                of the iterator class.

        Example:

            A very basic example:

            >>> session.query('{ hero { name } }')

            An example using a variable within the query:

            >>> query = '''
            ... query HeroNameAndFriends($episode: Episode) {
            ...   hero(episode: $episode) {
            ...     name
            ...     friends {
            ...       name
            ...     }
            ...   }
            ... }
            >>> session.query(query, episode='JEDI')
        """
        query_doc = self.construct_query(query=query, stored_file=stored_file)
        if not keyword_arguments:
            keyword_arguments = {}
        if iterator:
            if not graphql_model:
                raise TypeError(
                    'No "graphql_model" name was assigned for the iterator.'
                )
            return iterator(self,
                            query=query_doc,
                            variables=variables,
                            model=graphql_model,
                            )
        return self._client.execute(query_doc, **keyword_arguments)

    def validate(self, query: Union[str, StringIO]) -> Dict[str, Any]:
        """
        Validates the query against the schema and returns any validation
        errors that may have occured.

        Args:
            query (str | StringIO):
                The query to validate against

        Returns:

        """
        graphql_query = self.construct_query(query=query)
        return validate(self._client.schema, graphql_query)

