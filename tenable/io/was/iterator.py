from typing import Any, List, Dict
from restfly import APIIterator


class WasIterator(APIIterator):
    """
    The WAS iterator can be used to handle downloading and processing of the data from
    WAS export.

    Attributes:
        target_scan_ids:
            The target Scan IDs for the specified parent Scan ID.
        page (list[dict]):
            The current chunk of data.
    """
    target_scan_ids: List[str]
    page: List[Dict]

    def __init__(self, api, target_scan_ids, **kwargs):
        self.target_scan_ids = target_scan_ids
        super().__init__(api, **kwargs)

    def _get_page(self) -> None:
        """
        Get the scan results for the next target scan ID.
        """
        current_target_scan_id = self.target_scan_ids.pop()
        self._log.debug(f"Getting the data for target ID: {current_target_scan_id}")
        # self.page = self._api.download_scan_report(current_target_scan_id)["findings"]

        scan_result = self._api.download_scan_report(current_target_scan_id)
        self.page = [_enriched_finding_object(scan_result, f) for f in scan_result["findings"]]

        self._log.debug(f"Target ID: {current_target_scan_id} has {len(self.page)} finding(s).")

        # Corner case - if the chunk is empty, request for another page.
        if len(self.page) < 1:
            self._get_page()

    def next(self) -> Any:
        """
        Ask for the next record in the current page.
        """

        # If we've worked through all the items in the current page, get a new page.
        if (len(self.target_scan_ids) > 0) and (len(self.page) == 0):
            self._get_page()

        # Stop iteration when there are no more target IDs to process and the current page
        # has no more elements to process.
        elif (len(self.target_scan_ids) == 0) and (len(self.page) == 0):
            raise StopIteration()

        return self.page.pop()


def _enriched_finding_object(page: Dict, finding: Dict):
    """
    Attaches config and scan info to each finding object.
    Note: This adjustment is done to enable integration with Splunk.
    """
    return {
        "finding": finding,
        "config": {
            "config_id": page["config"]["config_id"]
        },
        "scan": page["scan"],
    }
