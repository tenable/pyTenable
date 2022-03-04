'''
Scans
=====

The following methods allow for interaction into the Tenable.io
:devportal:`scans <scans>` API endpoints.

Methods available on ``tio.v3.vm.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScansAPI
    :members:
'''
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class ScansAPI(ExploreBaseEndpoint):
    '''
    This will contain all methods related to scans
    '''
    _path = 'api/v3/scans'
    _conv_json = True

    def timezones(self) -> list:
        '''
        Retrieves the list of timezones.
        :devportal:`scans: timezones <scans-timezones>`

        Returns:
            :obj:`list`:
                List of allowed timezone strings accepted by Tenable.IO

        Examples:
            >>> for item in  tio.v3.vm.scans.timezones():
            ...     pprint(item)
        '''
        resp = self._get('timezones')['timezones']
        return [i['value'] for i in resp]
