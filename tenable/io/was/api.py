"""
WAS
===

The following methods allow for interaction into the Tenable Vulnerability Management
:devportal:`WAS <was>` API endpoints.

Methods available on ``tio.was``:

.. rst-class:: hide-signature
.. autoclass:: WasAPI
    :members:
"""

from tenable.io.base import TIOEndpoint, TIOIterator
from tenable.io.was.iterator import WasIterator
from typing import Any, Dict, Tuple


class WasAPI(TIOEndpoint):
    """
    This class contains methods related to WAS.
    """

    def export(self, **kwargs) -> WasIterator:
        """
        Export Web Application Scan Results based on filters applied.

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
            ... for finding in was_iterator:
            ...     print(finding)
        """

        # Get scan configuration iterator.
        scan_config = self._search_scan_configurations(**kwargs)

        # Iterate through the scan configs and collect the parent scan IDs and the finalized_at param.
        # This finalized_at property belonging to the parent will be passed down to its children's findings.
        parent_scan_ids_with_finalized_at = [_parent_id_with_finalized_at(sc) for sc in scan_config if sc]

        # initialize parent_scan_ids_with_finalized_at if it's empty.
        if not parent_scan_ids_with_finalized_at:
            parent_scan_ids_with_finalized_at = []

        self._log.debug(f"We have {len(parent_scan_ids_with_finalized_at)} parent scan ID(s) to process.")

        # Fetch the target scans info for all the above parent scan IDs, and flatten it.
        # We need to flatten because, each parent ID will have multiple target scans.
        self._log.debug(f"Fetching Target scan IDs for {len(parent_scan_ids_with_finalized_at)} parent scan ID(s)")
        target_scans = [scan for p in parent_scan_ids_with_finalized_at for scan in
                        self._get_target_scan_ids_for_parent(p)]

        # Iterate through the target scans info and collect the target scan IDs.
        target_scan_ids_with_parent_finalized_at = [_target_id_with_parent_finalized_at(ts) for ts in target_scans if ts]
        self._log.debug(f"We have {len(target_scan_ids_with_parent_finalized_at)} target scan(s) to process.")

        return WasIterator(
            api=self._api.was,
            target_scan_ids=target_scan_ids_with_parent_finalized_at
        )

    def download_scan_report(self, scan_uuid: str) -> Dict:
        """
        Downloads the individual target scan results.

        Args:
            scan_uuid (str):
             UUID of the scan whose report to download.
        """
        return self._api.get(
            path=f"was/v2/scans/{scan_uuid}/report",
            headers={
                "Content-Type": "application/json"
            }
        ).json()

    def _search_scan_configurations(self, **kwargs) -> TIOIterator:
        """
        Returns a list of web application scan configurations based on the provided filter parameters.
        """
        payload = dict()

        # Either single_filter should be passed alone. Or, any or all of these [and_filter, or_filter] can be passed.
        if "single_filter" in kwargs and (("and_filter" in kwargs) or ("or_filter" in kwargs)):
            raise AttributeError("single_filter cannot be passed alongside and_filter or or_filter.")

        if "single_filter" in kwargs:
            payload = _tuple_to_filter(kwargs["single_filter"])

        if "and_filter" in kwargs:
            payload["AND"] = [_tuple_to_filter(t) for t in kwargs["and_filter"]]

        if "or_filter" in kwargs:
            payload["OR"] = [_tuple_to_filter(t) for t in kwargs["or_filter"]]

        self._log.debug(f"Fetching the scan configuration information with filters: {payload} ...")

        return TIOIterator(
            self._api,
            _limit=self._check('limit', 200, int),
            _offset=self._check('offset', 0, int),
            _query=dict(),
            _path='was/v2/configs/search',
            _method="POST",
            _payload=payload,
            _resource='items'
        )

    def _get_target_scan_ids_for_parent(self, parent: dict) -> Dict:
        """
        Returns the vulns by target scans of the given parent scan ID.
        """
        # This method does not have an iterator and is not public as the API it invokes has not been publicly documented.
        # However, the API is in use in the Tenable Vulnerability Management UI.

        parent_scan_id = parent["parent_scan_id"]
        parent_finalized_at = parent["parent_finalized_at"]

        offset = 0
        limit = 200

        # initialize the flattened responses list
        flattened_list = []

        while True:
            # Fetch the page
            response = self._api.post(
                path=f"was/v2/scans/{parent_scan_id}/vulnerabilities/by-targets/search?limit={limit}&offset={offset}"
            ).json()

            # Collect the items; flatten; and write to the flattened list (extend).
            items_in_response = response["items"]
            items = [{
                "items": item,
                "parent_finalized_at": parent_finalized_at
            } for item in items_in_response]

            flattened_list.extend(items)

            # Increment the page number by limit
            offset += limit

            if not items_in_response:
                self._log.debug(f"Stopping the iteration as we encountered an empty response from the API.")
                break

        self._log.debug(f"Parent ID: {parent_scan_id} has {len(flattened_list)} target ID(s).")

        return flattened_list


def _tuple_to_filter(t: Tuple[str, str, Any]) -> Dict:
    """
    Accepts a tuple with three elements, and returns a filter object.
    """
    return {"field": t[0], "operator": t[1], "value": t[2]}


def _parent_id_with_finalized_at(scan_config: dict):
    return {
        "parent_scan_id": scan_config["last_scan"]["scan_id"],
        "parent_finalized_at": scan_config["last_scan"]["finalized_at"]
    }


def _target_id_with_parent_finalized_at(target_scan: dict):
    return {
        "target_scan_id": target_scan["items"]["scan"]["scan_id"],
        "parent_finalized_at": target_scan["parent_finalized_at"]
    }
