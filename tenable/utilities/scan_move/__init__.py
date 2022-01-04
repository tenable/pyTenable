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
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class ScanMove(ExploreBaseEndpoint):
    '''
    This will contain all methods related to Users
    '''

    def __init__(self, source_tsc, target_tsc):
        self.source_tsc = source_tsc
        self.target_tsc = target_tsc

    def _get_scan_history(self, scan_id, limit):
        scan_history = []
        count = 0
        for scan_instance in self.source_tsc.v3.scans.history(scan_id):

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
        for mv_scan in self.source_tsc.v3.scans.search(scan_filter):
            if not (
                    mv_scan.status == 'completed' and mv_scan.type == 'remote'
            ):
                continue
        scan_history = self._get_scan_history(mv_scan.id, limit)

        for scan in scan_history:
            print("Exporting Scan ID:{}, with history_id: {} now\n".format(
                mv_scan, scan
            ))

            scan_report = self.source_tsc.v3.vm.scans.export(scan)
            imported_scan = self.target_tsc.v3.vm.scans.import_scan(
                scan_report
            )

            print("Scan imported: {}".format(imported_scan.get('id')))
