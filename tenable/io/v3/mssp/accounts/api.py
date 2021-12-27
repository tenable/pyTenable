'''
Accounts
========

The following methods allow for interaction into the Tenable.io
:devportal:`Managed Security Service Provider v3 accounts
<io-mssp-accounts>` API.

Methods available on ``tio.v3.mssp.accounts``:

.. rst-class:: hide-signature
.. autoclass:: AccountsAPI
    :members:
'''
from typing import List

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class AccountsAPI(ExploreBaseEndpoint):
    _path = 'api/v3/mssp/accounts'
    _conv_json = True

    def search(self, **kwargs) -> List:
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )
