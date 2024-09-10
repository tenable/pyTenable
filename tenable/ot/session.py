"""
Tenable OT Security
==========

This package covers the Tenable OT Security interface.

.. autoclass:: TenableOT
    :members:


.. toctree::
    :hidden:
    :glob:

    assets
    events
    plugins
"""
import os
import warnings

from tenable.base.platform import APIPlatform
from tenable.ot.assets import AssetsAPI
from tenable.ot.events import EventsAPI
from tenable.ot.plugins import PluginsAPI
from tenable.ot.exports.api import ExportsAPI


class TenableOT(APIPlatform):
    """
    The Tenable OT Security object is the primary interaction point for users
    to interface with Tenable.OT via the pyTenable library.  All the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        api_key (str, optional):
            The user's API key for Tenable OT Security.  If an api key isn't
            specified, then the library will attempt to read the environment
            variable ``TOT_API_KEY`` to acquire the key.
        url (str, optional):
            The base URL used to connect to the Tenable OT Security service.
            If a URL isn't specified, then the library will attempt to read the
            environment variable ``TOT_URL`` to acquire the URL.

        **kwargs:
            arguments passed to :class:`tenable.base.platform.APIPlatform` for
            ConnectionAbortedErrorn management.


    Examples:
        Basic Example:

        >>> from tenable.ot import TenableOT
        >>> ot = TenableOT(api_key='SECRET_KEY',
        ..                 url='https://ot.example.com')

        Example with proper identification:

        >>> ot = TenableOT(api_key='SECRET_KEY',
        ...                url='https://ot.example.com',
        ...                vendor='Company Name',
        ...                product='My Awesome Widget',
        ...                build='1.0.0')

        Example with proper identification leveraging environment variables for
        the connection parameters:

        >>> ot = TenableOT(vendor='Company', product='Widget', build='1.0.0')
    """

    _env_base = "TOT"
    _ssl_verify = False
    _conv_json = True
    _allowed_auth_mech_priority = ['key']
    _allowed_auth_mech_params = {
        'key': ['api_key']
    }

    def _key_auth(self, api_key, **kwargs):  # noqa: PLW0221,PLW0613
        self._session.headers.update({"X-APIKeys": f"key={api_key}"})
        self._auth_mech = "keys"

    def _authenticate(self, **kwargs):
        kwargs["_key_auth_dict"] = kwargs.get(
            "_key_auth_dict",
            {"api_key": kwargs.get("api_key", os.getenv(f"{self._env_base}_API_KEY"))},
        )
        super()._authenticate(**kwargs)

    def graphql(self, **kwargs):
        """
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
        """
        return self.post("graphql", json=kwargs)

    @property
    def assets(self):
        """
        The interface object for the
        :doc:`Tenable OT Security Assets APIs <assets>`.
        """
        return AssetsAPI(self)

    @property
    def events(self):
        """
        The interface object for the
        :doc:`Tenable OT Security Events APIs <events>`.
        """
        return EventsAPI(self)

    @property
    def plugins(self):
        """
        The interface object for the
        :doc:`Tenable OT Security Plugins APIs <plugins>`.
        """
        return PluginsAPI(self)

    @property
    def exports(self):
        """
        The interface object for the
        :doc:`Tenable OT Security Exports <exports>`.
        """
        return ExportsAPI(self)
