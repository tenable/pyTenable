'''
MSSP Definitions
================

The following methods allow for interaction into the Tenable.io
:devportal:`definitions <definitions>` API endpoints.

Methods available on ``tio.v3.vm.definitions``:

.. rst-class:: hide-signature
.. autoclass:: MSSPDefinitionsAPI
    :members:
'''

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class MSSPDefinitionsAPI(ExploreBaseEndpoint):

    _conv_json = True

    def accounts(self):
        return self._get('api/v3/definitions/mssp/accounts')

    def logos(self):
        return self._get('api/v3/definitions/mssp/logos')
