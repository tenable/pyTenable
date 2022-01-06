'''
Tenable.utilities
=================

The following sub-package allows for interaction with additional Tenable
Utilities

Utilities available on ``tenable.utilities``:

.. autoclass:: TenableUtilities
   :members:

.. toctree::
    :hidden:
    :glob:

    scan_bridge
'''
from tenable.utilities.scan_bridge import ScanBridge


class TenableUtilities():
    '''
    This will contain property for all additional utilities
    i.e Scan Bridge, Scan Move etc
    '''

    @property
    def scan_bridge(self):
        '''
        The interface object for the
        :doc:`Tenable.utilities Scan Bridge <scan_bridge>`.
        '''
        return ScanBridge()
