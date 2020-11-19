'''
Tenable.ot
==========

This package covers the Tenable.ot interface.

.. autoclass:: TenableOT
    :members:


.. toctree::
    :hidden:
    :glob:

    assets
    network_interfaces
    vulns

'''
from tenable.base.platform import APIPlatform
import os, semver

from .assets import AssetsAPI
from .network_interfaces import NetworkInterfacesAPI
from .vulns import VulnsAPI

class TenableOT(APIPlatform):
    '''
    The Tenable.ot object is the primary interaction point for users to
    interface with Tenable.io via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        secret_key (str, optional):
            The user's API secret key for Tenable.ot.
        port (int, optional):
            The port to connect to on the Tenable.ot host.  If left unspecified,
            then the library will attempt to
        **kwargs:
            arguments passed to :class:`tenable.base.platform.APIPlatform` for
            connection management.


    Examples:
        Basic Example:

        >>> from tenable.ot import TenableOT
        >>> ot = TenableOT(api_token='API_TOKEN', address='ot.example.com')

        Example with proper identification:

        >>> ot = TenableOT(api_token='API_TOKEN', address='ot.example.com',
        >>>     vendor='Company Name',
        >>>     product='My Awesome Widget',
        >>>     build='1.0.0')

        Example with proper identification leveraging environment variables for
        the connection parameters:

        >>> ot = TenableOT(vendor='Company', product='Widget', build='1.0.0')
    '''
    _base_path = 'v1'
    _env_base = 'TOT'
    _ssl_verify = False

    def _authenticate(self, **kwargs):
        '''
        Authentication method for Tenable.ot platform
        '''
        api_token = kwargs.get('secret_key',
            os.getenv(f'{self._env_base}_SECRET_KEY')
        )

        self._session.headers.update({
            'X-APIKeys': f'key={api_token}',
        })

    def graphql(self, **kwargs):
        '''
        GraphQL Endpoint

        This singular method exposes the GraphQL API to the library.  As all
        keyword arguments are passed directly to the JSON body, it allows for a
        freeform interface into the GraphQL API.

        Args:
            **kwargs (dict, optional):
                The key/values that should be passed to the body of the GraphQL
                request.

        Example:
            >>> ot.graphql(
            ...     variables={'asset': 'b64 id string'},
            ...     query=\'\'\'
            ...         query getAssetDetails($asset: ID!) {
            ...             asset(id: $asset) {
            ...                 id
            ...                 type
            ...                 name
            ...                 criticality
            ...                 location
            ...             }
            ...         }
            ... \'\'\')
        '''
        return self.post('graphql', json=kwargs, use_base=False)

    @property
    def assets(self):
        '''
        The interface object for the
        :doc:`Tenable.ot Assets APIs <assets>`.
        '''
        return AssetsAPI(self)

    @property
    def network_interfaces(self):
        '''
        The interface object for the
        :doc:`Tenable.ot Network Interfaces APIs <network_interfaces>`.
        '''
        return NetworkInterfacesAPI(self)

    @property
    def vulns(self):
        '''
        The interface object for the
        :doc:`Tenable.ot Vulnerabilities APIs <vulns>`.
        '''
        return VulnsAPI(self)