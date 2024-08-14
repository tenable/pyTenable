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
    _api: 'GraphQLSession'
    query: DocumentNode
    variables: Dict[str, Any]
    next_token: Optional[str] = None

    def _transform(self, resp: Dict) -> List[Dict[str, Any]]:
        return resp.get('nodes', [])

    def _get_page(self):
        if self.next_token:
            self.variables['startAt'] = self.next_token
        resp = self._api.query(self.query, **self.variables)
        self.next_token = resp.get('pageInfo', {}).get('endCursor')
        self.total = resp.get('count')
        self.page = self._transform(resp)


class GraphQLSession:
    _query_folder: Path
    _base_path: str = ''
    _env_base: str = ''
    client: Client

    def __init__(self,
                 url: Optional[str] = None,
                 api_key: Optional[str] = None,
                 verify: bool = True,
                 retries: int = 3,
                 timeout: int = 300,
                 vendor: str = 'unknown',
                 product: str = 'unknown',
                 build: str = 'unknown',
                 ):
        self._log = logging.getLogger(
            f'{self.__module__}.{self.__class__.__name__}'
        )
        if not url:
            url = os.environ.get(f'{self._env_base}_URL')
        if not api_key:
            api_key = os.environ.get(f'{self._env_base}_API_KEY')

        if not api_key or not url:
            raise ConnectionError(
                f'Invalid connection settings: {url=}, {api_key=}'
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
        self.client = Client(transport=transport,
                             fetch_schema_from_transport=True,
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
                        query: Optional[Union[str, StringIO]] = None,
                        stored_file: Optional[str] = None
                        ) -> DocumentNode:
        if query and isinstance(query, StringIO):
            return gql(query.read())
        elif query and isinstance(query, str):
            return gql(query)
        elif not query and stored_file:
            queryfile = self._query_folder.joinpath(stored_file)
            with queryfile.open('r', encoding='utf-8') as fobj:
                query_obj = gql(fobj.read())
            return query_obj
        else:
            raise TypeError(f'No query was presented {query=}, {stored_file=}')

    def query(self,
              query: Optional[str] = None,
              stored_file: Optional[str] = None,
              operation_name: Optional[str] = None,
              serialize_variables: Optional[bool] = None,
              parse_result: Optional[bool] = None,
              get_execution_result: bool = False,
              keyword_arguments: Optional[Dict[str, Any]] = None,
              iterator: Optional[GraphQLIterator] = None,
              **variables: Any
              ) -> Dict[str, Any]:
        """
        Query the GraphQL API

        Args:
            query (str | StringIO):
                The GraphQL query to run
            variables (dict, optional):
                Any variable declarations that need to be passed alonmg with
                the query.

        Returns:
            Dict:
                If no iterator is passed, then the response dictionary is
                returned to the caller.
            GraphQLIterator:
                If an iterator class was passed, then the query is generated
                and the passed to the iterator nefore returning an instance
                of the iterator class.
        """
        query_doc = self.construct_query(query=query, stored_file=stored_file)
        if not keyword_arguments:
            keyword_arguments = {}
        if iterator:
            return iterator(self,
                            query=query_doc,
                            variables=variables,
                            )
        return self.client.execute(query_doc,
                                   variable_values=variables,
                                   operation_name=operation_name,
                                   serialize_variables=serialize_variables,
                                   parse_result=parse_result,
                                   get_execution_result=get_execution_result,
                                   **keyword_arguments
                                   )

    def validate(self, query: Union[str, StringIO]):
        """
        Validates the query against the schema and returns any validation
        errors that may have occured.

        Args:
            query (str | StringIO):
                The query to validate against
        """
        graphql_query = self.construct_query(query=query)
        return validate(self.client.schema, graphql_query)

