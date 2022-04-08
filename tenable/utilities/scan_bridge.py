'''
Scan Bridge
===========

The following class allows to send TenableIO scan information
to a TenableSC repository.

Usage: ``from tenable.utilities import ScanBridge``:

.. rst-class:: hide-signature
.. autoclass:: ScanBridge
    :members:
'''
import os

from tenable.io import TenableIO
from tenable.sc import TenableSC


class ScanBridge(object):
    '''
    The ScanBridge Class can be used as a bridge to send the Tenable.IO scans
    data to the given Tenable.SC repo_id using the bridge function.

    Args:
        tsc (TenableSC object):
            A TenableSC class object at which scans are to be migrated.
        tio (TenableIO object):
            The TenableIO class object where scans details is present.

    Example:
        >>> from tenable.utilities import ScanBridge
        ... from tenable.io import TenableIO
        ... from tenable.sc import TenableSC
        ... tsc = TenableSC(username, password, url)
        ... tio = TenableIO(access_key, secret_key, url)
        ... sb = ScanBridge(tsc, tio)
    '''
    def __init__(self, tsc: TenableSC, tio: TenableIO):
        '''
        Init method for ScanBridge class.
        '''
        self.tio = tio
        self.tsc = tsc

    def bridge(self, scan_id: int, repo_id: int) -> None:
        '''
        This method sends the TenableIO scan details to the provided TenableSC repo


        Args:
            scan_id (int):
                The TenableIO scan_id whose details is to be migrated.
            repo_id (int):
                The repo_id of Tenable SC instance where scan details
                will be imported.

        Example:
            >>> sb = ScanBridge(tsc, tio)
            ... sb.bridge(48,7)
        '''
        try:
            with open(f'{scan_id}.nessus', 'wb') as nessus:
                self.tio.scans.export(scan_id, fobj=nessus)
                # self.tio.v3.vm.scans.export(scan_id, fobj=nessus)
            with open(f'{scan_id}.nessus') as file:
                self.tsc.scan_instances.import_scan(file, repo_id)
        finally:
            if os.path.exists(f'{scan_id}.nessus'):
                os.remove(f'{scan_id}.nessus')
