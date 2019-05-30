'''
reports
=======

The reports methods allow interaction into ContainerSecurity 
reports API.

Methods available on ``cs.reports``:

.. rst-class:: hide-signature
.. autoclass:: ReportAPI

    .. automethod:: report
'''
from .base import CSEndpoint

class ReportAPI(CSEndpoint):
    def report(self, digest):
        '''
        Retrieves the image report by the image digest.

        Args:
            digest (str): The image digest.

        Returns:
            dict: The report resource record.
        '''
        return self._api.get('reports/{}'.format(
            self._check('digest', digest, str))).json()