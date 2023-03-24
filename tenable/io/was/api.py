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
import typing

from tenable.io.base import TIOEndpoint
from tenable.io.was.iterator import WasIterator, WasScanConfigurationIterator


class WasAPI(TIOEndpoint):
    """
    This class contains methods related to WAS.
    """

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
            payload["AND"] = _tuples_to_filters(kwargs["and_filter"])

        if "or_filter" in kwargs:
            payload["OR"] = _tuples_to_filters(kwargs["or_filter"])

        return WasScanConfigurationIterator(self._api,
                                            _limit=self._check('limit', 200, int),
                                            _offset=self._check('offset', 0, int),
                                            _query=dict(),
                                            _path='was/v2/configs/search',
                                            _method="POST",
                                            _payload=payload,
                                            _resource='items'
                                            )

    def _get_target_scan_ids_for_parent(self, parent_scan_id: str) -> dict:
        """
        Returns the vulns by target scans of the given parent scan ID.
        """
        # This method does not have an iterator and is not public as the API invoked has not been publicly documented
        # However, the API is in use by the UI.

        offset = 0
        limit = 200

        responses = []
        first_response = self._api.post(
            path=f"was/v2/scans/{parent_scan_id}/vulnerabilities/by-targets/search?limit={limit}&offset={offset}").json()
        responses = [*responses, *first_response["items"]]
        total_pages = first_response["pagination"]["total"]

        while offset <= total_pages:
            offset += 1
            new_response = self._api.post(
                path=f"was/v2/scans/{parent_scan_id}/vulnerabilities/by-targets/search?limit={limit}&offset={offset}").json()
            responses = [*responses, *new_response["items"]]

        return responses

    def _get_target_scan_ids_for_parents(self, parent_scan_ids: [str]) -> list[dict]:
        """
        Returns a flattened list of vulns by target scans for the list of parent scan IDs provided.
        """
        responses = []
        for p in parent_scan_ids:
            resp = self._get_target_scan_ids_for_parent(p)
            responses = [*responses, *resp]

        return responses

    def download_scan_report(self, target_scan_id: str) -> dict:
        """
        Downloads the individual target scan results.
        """
        return self._api.get(
            path=f"was/v2/scans/{target_scan_id}/report",
            headers={
                "Content-Type": "application/json"
            }
        ).json()

    def export(self, **kwargs) -> WasIterator:
        """
        Export WAS Scan.

        Args:
            single_filter tuple:
                A single filter to apply to the scan configuration search. This is a tuple with three elements -
                field, operator, and value in that order.
            and_filter tuple: An array of filters that must all be satisfied. This is a list of tuples with three elements -
                field, operator, and value in that order.
            or_filter list: An array of filters where at least one must be satisfied. This is a list of tuples with three elements -
                field, operator, and value in that order.
        """

        # Get scan configuration iterator.
        scan_config = self._search_scan_configurations(**kwargs)

        # Iterate through the scan configs and collect the parent scan IDs.
        parent_scan_ids = [sc["last_scan"]["scan_id"] for sc in scan_config if sc]

        # Fetch the target scans info for all the above parent scan IDs, and flatten it.
        # We need to flatten because, each parent ID will have multiple target scans.
        target_scans = self._get_target_scan_ids_for_parents(parent_scan_ids)

        # Iterate through the target scans info and collect the target scan IDs.
        target_scan_ids_for_download = [sc["scan"]["scan_id"] for sc in target_scans if sc]

        # Return an iterator
        return WasIterator(
            api=self._api.was,
            parent_scan_id="",
            target_scan_ids=target_scan_ids_for_download
        )


def _tuples_to_filters(filter_tuples: list[tuple[str, str, typing.Any]]) -> list[dict]:
    """
    Accepts a list of tuples with three strings, and returns a filter object list.
    """
    return [_tuple_to_filter(t) for t in filter_tuples]


def _tuple_to_filter(filter_tuple: tuple[str, str, typing.Any]) -> dict:
    """
    Accepts a tuple with three strings, and returns a filter object.
    """
    return {
        "field": filter_tuple[0],
        "operator": filter_tuple[1],
        "value": filter_tuple[2]
    }
