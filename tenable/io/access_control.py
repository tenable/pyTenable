"""
Access Control
==============

the following methods allow for interaction into the tenable Platform's
:devportal:`Access Control <access_control>` API endpoints.

Methods available on ``tio.access_control``:

.. rst-class:: hide-signature
.. autoclass:: AccessControlAPI
    :members:
"""
from tenable.io.base import TIOEndpoint


class AccessControlAPI(TIOEndpoint):
    """
    This will contain all the methods related to Access Control.
    """

    def list(self) -> list:
        """
        Returns a list of permissions in your container.

        Returns:
            :obj:`list`:
                List of permissions.

        Examples:
            >>> for permission in tio.access_control.list():
            ...     pprint(permission)
        """
        return self._api.get("api/v3/access-control/permissions").json()["permissions"]
