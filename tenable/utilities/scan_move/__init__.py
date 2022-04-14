'''
Scan Move
=========

The following class allows to send scans from one instance of TenableIO to
another instance of TenableIO.

Methods available on ``tio.utilities.scan_move``:

.. rst-class:: hide-signature
.. autoclass:: ScanMove
    :members:
'''
from tenable.io import TenableIO


class ScanMove:
    '''
    This will contain all methods related to Users
    '''

    def __init__(self, source_tio: TenableIO, target_tio: TenableIO):
        self.source_tio = source_tio
        self.target_tio = target_tio

    def _get_scan_history(self, scan_id: str, limit: int):
        # get scan history using scan id
        scan_history = []
        count = 0

        for scan_instance in self.source_tio.v3.vm.scans.history(scan_id):

            if count == limit:
                break

            if scan_instance.get('status', '') == 'completed':
                count += 1
                scan_history.append(scan_instance.get('id'))

        return scan_history

    def move(self, limit):
        # get all scans from source instance

        scan_filter = {
            'and': [
                {'property': 'status', 'operator': 'eq', 'value': 'completed'},
                {'property': 'type', 'operator': 'eq', 'value': 'remote'}
            ]
        }

        for mv_scan in self.source_tio.v3.vm.scans.search(
            filter=scan_filter
        ):
            scan_history = self._get_scan_history(mv_scan['id'], limit)

            for scan in scan_history:
                print("Exporting Scan ID:{}, with history_id: {} now\n".format(
                    mv_scan, scan
                ))

                scan_report = self.source_tio.v3.scans.export(scan)
                imported_scan = self.target_tio.v3.scans.import_scan(
                    scan_report
                )

                print("Scan imported: {}".format(
                    imported_scan.get('scan').get('id')
                ))
