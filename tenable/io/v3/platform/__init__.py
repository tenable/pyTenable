'''
Platform
========

The following API's are available for interaction under Platform

Methods available on ``tio.v3.platform``:


.. rst-class:: hide-signature
.. autoclass:: Platform
    :members:

.. toctree::
    :hidden:
    :glob:

    groups
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.platform.groups.api import GroupsAPI


class Platform(ExploreBaseEndpoint):  # noqa: PLR0904
    '''
    This class will contain property for all resources under Platform
    i.e plugins, scans, folders etc.
    '''

    @property
    def groups(self):
        '''
        The interface object for the
        :doc:`Tenable.IO v3 Groups API <groups>`
        '''
        return GroupsAPI(self._api)
