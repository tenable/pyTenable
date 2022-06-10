'''
Findings V3 endpoints
=====================

The following methods allow for interaction into the Tenable.io
:devportal:`findings <io-v3-uw-vulnerabilities-search>` API.

Methods available on ``tio.v3.explore.findings``:

.. rst-class:: hide-signature
.. autoclass:: FindingsAPI
    :members:
'''
from typing import Dict, Union

from requests import Response

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)


class FindingsAPI(ExploreBaseEndpoint):
    '''
    API class containing all the methods related to Findings.
    '''
    _path = 'api/v3/findings/vulnerabilities'
    _conv_json = True
