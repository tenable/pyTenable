'''
About
=====

Methods described in this section relate to the About API.
These methods can be accessed at ``TenableIE.about``.

.. rst-class:: hide-signature
.. autoclass:: AboutAPI
    :members:
'''
from tenable.base.endpoint import APIEndpoint


class AboutAPI(APIEndpoint):
    _path = 'about'

    def version(self) -> str:
        '''
        Returns the version of the connected Tenable Identity Exposure instance.

        Examples:

            >>> tie.about.version()
        '''
        return self._get(box=True).version
