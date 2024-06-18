'''
License
=============

Methods described in this section relate to the license API.
These methods can be accessed at ``TenableIE.license``.

.. rst-class:: hide-signature
.. autoclass:: LicenseAPI
    :members:
'''
from typing import Dict
from tenable.ie.license.schema import LicenseSchema
from tenable.base.endpoint import APIEndpoint


class LicenseAPI(APIEndpoint):
    _path = 'license'
    _schema = LicenseSchema()

    def details(self) -> Dict:
        '''
        Get license singleton

        Returns:
            dict:
                The license object

        Examples:
            >>> tie.license.details()
        '''
        return self._schema.load(self._get())

    def create(self, license: str) -> Dict:
        '''
        Create new license singleton

        Args:
            license (str):
                The license string object.

        Return:
            The license object

        Example:
            >>> tie.license.create(
            ...     license='license'
            ... )
        '''
        payload = self._schema.dump(self._schema.load({
            'license': license
        }))
        return self._schema.load(self._post(json=payload))
