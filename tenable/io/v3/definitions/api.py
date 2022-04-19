'''
Definitions
===========

The following methods allow for interaction into the Tenable.io
:devportal:`definitions <definitions>` API endpoints.

Methods available on ``tio.v3.definitions``:

.. rst-class:: hide-signature
.. autoclass:: DefinitionsAPI
    :members:
'''

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.mssp.definitions.api import MSSPDefinitionsAPI
from tenable.io.v3.vm.definitions.api import VMDefinitionsAPI
from tenable.io.v3.was.definitions.api import WASDefinitionsAPI


class DefinitionsAPI(ExploreBaseEndpoint):

    _conv_json = True

    def connectors(self):
        return self._get('api/v3/definitions/connectors')

    def groups(self):
        return self._get('api/v3/definitions/groups')

    @property
    def mssp(self):
        return MSSPDefinitionsAPI(self._api)

    def users(self):
        raise NotImplementedError('Definitions not available.'
                                  'It will be available in future')

    @property
    def vm(self):
        return VMDefinitionsAPI(self._api)

    @property
    def was(self):
        return WASDefinitionsAPI(self._api)
