'''
Reports Definition
============

The following methods allow for interaction into the Tenable.sc
:sc-api:`ReportsDefinition <ReportsDefinition.html>` API.

Methods available on ``sc.report_definition``:

.. rst-class:: hide-signature
.. autoclass:: ReportDefinitionAPI
    :members:
'''
from .base import SCEndpoint

class ReportDefinitionAPI(SCEndpoint):
    def launch(self, id):
        '''
        Launches a Report definition.
        :sc-api:`report-definition: launch <ReportDefinition.html#ReportDefinitionRESTReference-/reportDefinition/{id}/launch>`
        Args:
            id (int): The report definition identifier to launch.
        Returns:
            :obj:`dict`:
                A report ID resource for the newly launched report definition.
        Examples:
            >>> running = sc.report_definition.launch(1)
            >>> print('The Scan Result ID is {}'.format(
            ...     running['scanResult']['id']))
        '''

        return self._api.post('reportDefinition/{}/launch'.format(
            self._check('id', id, int))).json()['response']
