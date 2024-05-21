'''
Reports
=======

The following methods allow for interaction into the Tenable Vulnerability Management
Container Security :devportal:`report <cs-v2-reports>` API endpoints.

Methods available on ``tio.cs.reports``:

.. rst-class:: hide-signature
.. autoclass:: ReportsAPI
    :members:
'''
from typing import Dict
from tenable.base.endpoint import APIEndpoint


class ReportsAPI(APIEndpoint):  # noqa: PLR0903
    _path = 'container-security/api/v2/reports'
    _box = True
    _box_attrs = {'camel_killer_box': True}

    def report(self, repository: str, image: str, tag: str) -> Dict:
        '''
        Returns the report for the specified image.

        :devportal:`API Documentation <container-security-v2-get-image-report>`

        Args:
            repository (str):
                The repository name.
            image (str):
                The image name.
            tag (str):
                The tag name.

        Examples:

            >>> tio.cs.reports.report('centos', '7', 'latest')
        '''
        return self._get(f'{repository}/{image}/{tag}')
