'''
Templates
=========

The following methods allow for interaction into the Tenable.io
:devportal:`Web Application Scanning v3 templates <was-v2-templates>` API.

Methods available on ``tio.v3.was.templates``:

.. rst-class:: hide-signature
.. autoclass:: TemplatesAPI
    :members:
'''
from typing import Dict
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class TemplatesAPI(ExploreBaseEndpoint):
    _path = 'api/v3/was/templates'
    _conv_json = True

    def details(self, template_id: UUID) -> Dict:
        '''
        Returns the details for a Tenable-provided template. Tenable-provided
        templates can be used to define scan configurations.

        :devportal:`was templates: Get Tenable-provided template details
        <was-v2-templates-details>`

        Args:
            template_id (UUID):
                The UUID of the Tenable-provided template resource.

        Returns:
            :obj:`dict`: The resource record of the template.

        Examples:
            >>> template = (tio.v3.was.templates.
            ...     details('d5b3cb1c-9c72-4974-a936-3dfbd2e2835e'))
            >>> pprint(template)
        '''
        return super().details(template_id)

    def search(self, **kwargs) -> Dict:
        '''
        Not Implemented
        '''
        raise NotImplementedError(
            'This method will be updated once ExploreSearchIterator is \
                implemented for v3'
        )
