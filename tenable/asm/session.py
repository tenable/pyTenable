"""
Tenable Attack Surface Management
=================================

This package covers the Tenable ASM application.

.. autoclass:: TenableASM
    :members:


.. toctree::
    :hidden:
    :glob:

    inventory
    smart_folders

"""
from tenable.base.platform import APIPlatform
from .inventory import InventoryAPI
from .smart_folders import SmartFoldersAPI


class TenableASM(APIPlatform):
    """
    The TenableASM class is the primary interaction point for users to interface with
    Tenable Attack Surface Management via the pyTenable library.  All the API endpoint
    classes that wrap the various aspects of ASM will be attached to this base class.

    Args:
        api_key (str, optional):
            The user's API key to interface into Tenable ASM.  If the key isn't
            specified, then the library will attempt to read the environment
            variable ``TASM_API_KEY`` to get the key.
        url (str, optional):
            The base URL that the paths will be appended onto.  If the url isn't
            specified, then the library will attempt to read the environment variable
            ``TASM_URL``.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``5``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        vendor (str, optional):
            The vendor name for the User-Agent string.
        product (str, optional):
            The product name for the User-Agent string.
        build (str, optional):
            The version or build identifier for the User-Agent string.
        timeout (int, optional):
            The connection timeout parameter informing the library how long to
            wait in seconds for a stalled response before terminating the
            connection.  If unspecified, the default is 120 seconds.

    Examples:

        Basic example:

        >>> from tenable.asm import TenableASM
        >>> tasm = TenableASM(url='https://asm.cloud.tenable.com',
        ...                   api_key='abcdef1234567890'
        ...                   )

        Another example with proper identification:

        >>> tasm = TenableASM(url='https://asm.cloud.tenable.com',
        ...                   api_key='abcdef1234567890',
        ...                   vendor='Company Name',
        ...                   product='My Awesome Widget',
        ...                   build='1.0.0'
        ...                   )

        Yet another example thats leveraging the ``TASM_API_KEY`` and
        ``TASM_URL`` environment variables:

        >>> os.environ['TASM_URL'] = 'https://asm.cloud.tenable.com'
        >>> os.environ['TASM_API_KEY'] = 'abcdef1234567890'
        >>> tasm = TenableASM(vendor='Company Name',
        ...                   product='My Awesome Widget',
        ...                   build='1.0.0'
        ...                   )
    """
    _base_path = 'api/1.0'
    _env_base = 'TASM'
    _box = True
    _allowed_auth_mech_priority = ['key']
    _allowed_auth_mech_params = {'key': ['api_key']}

    def _key_auth(self, api_key, **kwargs):
        """
        API Key authorization mechanism for Tenable ASM.
        """
        self._session.headers.update({'Authorization': api_key})
        self._auth_meth = 'key'

    @property
    def inventory(self):
        """
        The interface object for the
        :doc:`Tenable ASM Inventory API <inventory>`
        """
        return InventoryAPI(self)

    @property
    def smart_folders(self):
        """
        The interface object for the
        :doc:`Tenable ASM Smart Folders API <smart_folders>`
        """
        return SmartFoldersAPI(self)
