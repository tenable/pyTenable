"""
WAS
===

The following methods allow for interaction into the Tenable.io
:devportal:`WAS <was>` API endpoints.

Methods available on ``tio.was``:

.. rst-class:: hide-signature
.. autoclass:: WasAPI
    :members:
"""

from tenable.io.base import TIOEndpoint
from tenable.io.was.iterator import WasIterator, WasScanConfigurationIterator
from typing import Any, Dict, Tuple


class WasAPI(TIOEndpoint):
    """
    This class contains methods related to WAS.
    """

    def export(self, **kwargs) -> WasIterator:
        """
        Export WAS Scan.

        Args:
            single_filter (tuple):
                A single filter to apply to the scan configuration search. This is a tuple with three elements -
                field, operator, and value in that order.
            and_filter (list): An array of filters that must all be satisfied. This is a list of tuples with three elements -
                field, operator, and value in that order.
            or_filter (list): An array of filters where at least one must be satisfied. This is a list of tuples with three elements -
                field, operator, and value in that order.

        Returns:
            WasIterator

        Examples:

            Passing AND filter to the API

            >>> was_iterator = tio.was.export(
            ...     and_filter=[
            ...         ("scans_started_at", "gte", "2023/03/24"),
            ...         ("scans_status", "contains", ["completed"])
            ...     ]
            ... )
            ...
            ...for finding in was_iterator:
            ...     print(finding)
        """

        # Get scan configuration iterator.
        scan_config = self._search_scan_configurations(**kwargs)

        # Iterate through the scan configs and collect the parent scan IDs.
        parent_scan_ids = [sc["last_scan"]["scan_id"] for sc in scan_config if sc]
        self._log.debug(f"We have {len(parent_scan_ids)} parent scan ID(s) to process.")


        # Fetch the target scans info for all the above parent scan IDs, and flatten it.
        # We need to flatten because, each parent ID will have multiple target scans.
        self._log.debug(f"Fetching Target scan IDs for {len(parent_scan_ids)} parent scan ID(s)")
        target_scans = [scan for pid in parent_scan_ids for scan in self._get_target_scan_ids_for_parent(pid)]

        # Iterate through the target scans info and collect the target scan IDs.
        target_scan_ids_for_download = [sc["scan"]["scan_id"] for sc in target_scans if sc]
        self._log.debug(f"We have {len(target_scan_ids_for_download)} target scan(s) to process.")

        return WasIterator(
            api=self._api.was,
            target_scan_ids=target_scan_ids_for_download
        )

    def download_scan_report(self, target_scan_id: str) -> Dict:
        """
        Downloads the individual target scan results.
        """
        return self._api.get(
            path=f"was/v2/scans/{target_scan_id}/report",
            headers={
                "Content-Type": "application/json"
            }
        ).json()

    def _search_scan_configurations(self, **kwargs) -> WasScanConfigurationIterator:
        """
        Returns a list of web application scan configurations.
        """
        payload = dict()

        if "single_filter" in kwargs and (("and_filter" in kwargs) or ("or_filter" in kwargs)):
            raise AttributeError("single_filter cannot be passed alongside and_filter or or_filter.")

        if "single_filter" in kwargs:
            payload = _tuple_to_filter(kwargs["single_filter"])

        if "and_filter" in kwargs:
            payload["AND"] = [_tuple_to_filter(t) for t in kwargs["and_filter"]]

        if "or_filter" in kwargs:
            payload["OR"] = [_tuple_to_filter(t) for t in kwargs["or_filter"]]

        self._log.debug("Fetching the scan configuration information...")
        return WasScanConfigurationIterator(self._api,
                                            _limit=self._check('limit', 200, int),
                                            _offset=self._check('offset', 0, int),
                                            _query=dict(),
                                            _path='was/v2/configs/search',
                                            _method="POST",
                                            _payload=payload,
                                            _resource='items'
                                            )

    def _get_target_scan_ids_for_parent(self, parent_scan_id: str) -> Dict:
        """
        Returns the vulns by target scans of the given parent scan ID.
        """
        # This method does not have an iterator and is not public as the API it invokes has not been publicly documented.
        # However, the API is in use in the Tenable.io UI.

        # page number - we start with 0, and for every new page, we increment by 1.
        offset = 0
        # Max number of records in each page
        limit = 200

        # flattened responses list
        flattened_list = []

        while True:
            # Fetch the page
            response = self._api.post(
                path=f"was/v2/scans/{parent_scan_id}/vulnerabilities/by-targets/search?limit={limit}&offset={offset}"
            ).json()

            # Collect the items, flatten, and write to the flattened list (extend).
            items = response["items"]
            flattened_list.extend(items)

            # Increment the page number by 1
            offset += 1

            # Exit the loop if the page # becomes >= to the total # of pages.
            if not items or offset >= response["pagination"]["total"]:
                break

        self._log.debug(f"Parent ID: {parent_scan_id} has {len(flattened_list)} target ID(s).")

        return flattened_list


def _tuple_to_filter(t: Tuple[str, str, Any]) -> Dict:
    """
    Accepts a tuple with three strings, and returns a filter object.
    """
    return {"field": t[0], "operator": t[1], "value": t[2]}
