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

    def _search_scan_configurations(self, **kwargs):
        """
        Returns a list of web application scan configurations.

        Args:
            single_filter tuple:
                A single filter to apply to the scan configuration search. This can be
            and_filter tuple:
                and filter
            or_filter list:
                or filter
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
        Returns the
        """
        # Todo replace the following logic with iterators.
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
        Returns the
        """
        responses = []
        for p in parent_scan_ids:
            resp = self._get_target_scan_ids_for_parent(p)
            print(f"Target Length for {p}: {len(resp)}")
            responses = [*responses, *resp]

        return responses

    def download_scan_report(self, target_scan_id: str):
        """
        Downloads the individual scan ID
        """
        return self._api.get(
            path=f"was/v2/scans/{target_scan_id}/report",
            headers={
                "Content-Type": "application/json"
            }
        ).json()

    def export(self):
        """
        Export WAS Scan
        """
        scan_config = self._search_scan_configurations(and_filter=[
            ("scans_started_at", "gte", "2023/03/16"),
            ("scans_status", "contains", ["completed"])
        ])

        parent_scans = _collect_parent_scan_ids(scan_config)

        targets = self._get_target_scan_ids_for_parents(parent_scans)
        target_scan_ids_for_download = _collect_target_scan_ids(targets)
        print(len(targets))
        print(target_scan_ids_for_download)

        return WasIterator(
            api=self._api.was,
            parent_scan_id="",
            target_scan_ids=target_scan_ids_for_download
        )


def _tuples_to_filters(filter_tuples: list[tuple[str, str, typing.Any]]) -> list:
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


def _collect_parent_scan_ids(scan_configuration: [dict]) -> [str]:
    """
    Collects and returns the parent scan IDs from the scan configuration
    """
    return [sc["last_scan"]["scan_id"] for sc in scan_configuration if sc]


def _collect_target_scan_ids(scan_configuration: [dict]) -> [str]:
    """
    Collects and returns the parent scan IDs from the scan configuration
    """
    return [sc["scan"]["scan_id"] for sc in scan_configuration if sc]
