from tenable.base.platform import APIPlatform
import os

from .assets import AssetsAPI
from .network_interfaces import NetworkInterfacesAPI
from .vulns import VulnsAPI

class TenableOT(APIPlatform):
    '''
    The Tenable.ot object is the primary interaction point for users to
    interface with Tenable.io via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        api_token (str, optional):
            The user's API access key for Tenable.ot.
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
    _base_path = '/v1'
    _env_base = 'TOT'
    _ssl_verify = False
    _box_attrs = {'camel_killer_box': True}

    def _authenticate(self, **kwargs):
        '''
        Authentication method for Tenable.ot platform
        '''
        api_token = kwargs.get('api_token', os.getenv(
            '{}_API_TOKEN'.format(self._env_base)))

        self._session.headers.update({
            'Authorization': 'Key {token}'.format(token=api_token)
        })

    @property
    def assets(self):
        return AssetsAPI(self)

    @property
    def network_interfaces(self):
        return NetworkInterfacesAPI(self)

    @property
    def vulns(self):
        return VulnsAPI(self)