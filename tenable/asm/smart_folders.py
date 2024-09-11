"""
Smart Folders
=============

Methods described in this section relate to the smart folders API and can be accessed at
``TenableASM.smart_folders``.

.. rst-class:: hide-signature
.. autoclass:: SmartFoldersAPI
    :members:
"""
from typing import Dict, List, Any
from tenable.base.endpoint import APIEndpoint


class SmartFoldersAPI(APIEndpoint):
    _path = 'smartfolders'

    def list(self) -> List[Dict[str, Any]]:
        """
        Returns the list of smart folders from ASM.

        Example:
            >>> folders = asm.smartfolders.list()
        """
        return self._get()
