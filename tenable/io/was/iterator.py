import time
from typing import Any, List, Dict

from restfly import APIIterator

from tenable.io.base import TIOIterator


class WasIterator(APIIterator):
    """
    The WAS iterator can be used to handle downloading and processing of the data from
    WAS export.

    Attributes:
        parent_scan_id:
            The Scan ID of the parent.
        target_scan_ids:
            The target Scan IDs for the specified parent Scan ID.
        start_time:
            The timestamp denoting when the iterator was created.
        page (list[dict]):
            The current chunk of data.
    """
    start_time: str
    parent_scan_id: str
    target_scan_ids: List[str]
    page: List[Dict]

    def __init__(self, api, parent_scan_id, target_scan_ids, **kwargs):
        self.start_time = int(time.time())
        self.parent_scan_id = parent_scan_id
        self.target_scan_ids = target_scan_ids
        super().__init__(api, **kwargs)

    def _get_page(self) -> None:
        """
        Get the scan results for the next target scan ID.
        """
        current_target_scan_id = self.target_scan_ids.pop()
        self.page = self._api.download_scan_report(current_target_scan_id)["findings"]

        # Corner case - if the chunk is empty, request for another page.
        if len(self.page) < 1:
            self._get_page()

    def next(self) -> Any:
        """
        Ask for the next record in the current page.
        """

        # Raise a StopIteration exception if no more pages to download, and in the last page, no more items left to iterate.
        # if (len(self.target_scan_ids) == 0) and (len(self.page) == 0): raise StopIteration()

        # If we've worked through all the items in the current page, get a new page.
        if (len(self.target_scan_ids) > 0) and (len(self.page) == 0):
            self._get_page()

        # Stop iteration when the
        elif (len(self.target_scan_ids) == 0) and (len(self.page) == 0):
            raise StopIteration()

        return self.page.pop()


class DummyWasApi:
    _parent_scan_id = "parent"
    _target_scan_ids = ["id1", "id2", "id3"]
    _scan_response = {
        "id1": [
            {
                "first_name": "01 some name",
                "last name": "01 some last name"
            }, {
                "first_name": "02 some name",
                "last name": "02 some last name"
            }, {
                "first_name": "03 some name",
                "last name": "03 some last name"
            }
        ],
        "id2": [
            {
                "first_name": "11 some name",
                "last name": "11 some last name"
            }, {
                "first_name": "12 some name",
                "last name": "12 some last name"
            }, {
                "first_name": "13 some name",
                "last name": "13 some last name"
            }
        ],
        "id3": [
            {
                "first_name": "21 some name",
                "last name": "21 some last name"
            }
        ]
    }

    def get_parent_scan_id(self, **kwargs):
        return self._parent_scan_id

    def get_target_scan_ids(self, parent_scan_id):
        return self._target_scan_ids

    def get_scan_result(self, target_scan_id):
        return self._scan_response.get(target_scan_id)


class WasScanConfigurationIterator(TIOIterator):
    """
    The WasScanConfigurationIterator iterator provides a scalable way to work through scan configuration list result
    sets of any size.  The iterator will walk through each page of data,
    returning one record at a time.  If it reaches the end of a page of
    records, then it will request the next page of information and then continue
    to return records from the next page (and the next, and the next) until the
    counter reaches the total number of records that the API has reported.

    Attributes:
        count (int): The current number of records that have been returned
        page (list):
            The current page of data being walked through.  pages will be
            cycled through as the iterator requests more information from the
            API.
        page_count (int): The number of record returned from the current page.
        total (int):
            The total number of records that exist for the current request.
    """
    _payload = dict()

    def _get_data(self):
        """
        Request the next page of data
        """
        query = self._query
        query['limit'] = self._limit
        query['offset'] = self._offset

        resp = self._api.post(self._path, params=query, json=self._payload).json()

        # Incrementing the offset by one to be used while grabbing the next page.
        self._offset += 1

        return resp, self._resource

    def _get_page(self):
        """
        Get the next page of records
        """
        # Stop iteration if there is a page limit and the limit has been reached.
        if self._pages_total and self._pages_requested >= self._pages_total:
            raise StopIteration()

        resp, key = self._get_data()

        # `page_count` is the index of the items in each page. Here, we're resetting it to 0 when a new page is fetched.
        self.page_count = 0

        # `_pages_requested` is the total number of pages requested until now. Updating it.
        self._pages_requested += 1

        self.page = resp[key]

        # `total` is the total # of pages.
        self.total = resp['pagination']['total']

    def next(self):
        """
        Ask for the next record
        """
        # If the current index (`page_count`) is greater than the page size, that means we've reached the end of the
        # page and need to get the next page.
        if self.page_count >= len(self.page):
            self._get_page()
            if len(self.page) == 0:
                raise StopIteration()

        item = self.page[self.page_count]

        # `count` is the total # of items in all the pages.
        self.count += 1

        # updating the current index
        self.page_count += 1

        # return the item in the current index.
        return item
