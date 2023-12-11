"""
WAS Scan
==========

The following methods allow for interaction into the Tenable Security Center
:sc-api:`WAS Scan <WAS-Scan.htm>` API.  These items are typically seen under
the **WAS Scan** section of Tenable Security Center.

Methods available on ``sc.was_scan``:

.. rst-class:: hide-signature
.. autoclass:: WasScanAPI
    :members:

"""
from pprint import pprint
from typing import List, Optional

from tenable.sc.base import SCEndpoint


class WasScanAPI(SCEndpoint):
    api_route = "wasScan"

    def list(self, fields: Optional[List[str]] = None):
        """
        Retrieves the list of WAS Scans.

        :sc-api:`was-scan: list <Was-Scan.htm#wasScan_GET>`

        Args:
            fields (list, optional):
                A list of attributes to return for each scan.

        Returns:
            :obj:`list`:
                A list of WAS Scans.

        Examples:
            >>> for scan in sc.was_scan.list():
            ...     pprint(scan)
        """
        params = {}
        if fields:
            string_fields = [self._check("fields", f, str) for f in fields]
            params["fields"] = ",".join(string_fields)

        return self._api.get(self.api_route, params=params).json()['response']
