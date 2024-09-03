"""
Tenable Cloud Security
======================

.. autoclass:: CloudSecurity
    :members:

    .. automethod:: query
    .. automethod:: validate

.. toctree::
    :hidden:
    :glob:

    assets
    vulns
"""
from typing import Dict
from pathlib import Path
from tenable.base.graphql import GraphQLSession

from .assets import AssetsAPI
from .vulns import VulnsAPI


class CloudSecurity(GraphQLSession):
    """Tenable Cloud Security
    The CloudSecurity class is the primary interaction point for the Cloud Security
    GraphQL API within pyTenable.  The most commonly used and supported GraphQL APIs
    have also been wrapped into the endpoints below.

    Args:
        url (str):
            The url that points to the cloud security site to interact with.  If not
            specified, the SDK will attempt to pull the parameter from the environment
            variable `TCS_URL`
        api_key (str):
            The API Key to use for authentication to the API.  If not specied, the SDK
            will attempt to pull the parameter from the environment variable
            `TCS_API_KEY`.
        verify (bool, optional):
            Should SSL verification be performed?  The default is `True`.
        retries (int, optional):
            How many retries should be attempted before giving up on the current call?
            The default is `3`.
        timeout (int, optional):
            How long to wait in seconds for the API to respond before timing out the
            call and throwing an error?  The default is `300`.
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
    _query_folder: Path = Path(__file__).parent.joinpath('queries')
    _base_path: str = 'api/graph'
    _env_base: str = 'TCS'

    def _authorization(self, api_key: str) -> Dict:
        return {
            'Authorization': f'Bearer {api_key}'
        }

    @property
    def assets(self):
        """
        Interface object for the
        :doc:`Tenable Cloud Security Assets Queries <assets>`.
        """
        return AssetsAPI(self)

    @property
    def vulns(self):
        """
        Interface object for the
        :doc:`Tenable Cloud Security Vulnerability Queries <vulns>`.
        """
        return VulnsAPI(self)
