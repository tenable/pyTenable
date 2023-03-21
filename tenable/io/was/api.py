"""
WAS
===========

The following methods allow for interaction into the Tenable.io
:devportal:`WAS <was>` API endpoints.

Methods available on ``tio.was``:

.. rst-class:: hide-signature
.. autoclass:: WasAPI
    :members:
"""
import typing

from tenable.io.base import TIOEndpoint


class WasAPI(TIOEndpoint):
    """
    This class contains methods related to WAS.
    """

    def search_scan_configurations(self, **kwargs):
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

        # return self._api.post(path="was/v2/configs/search",
        #                       json=payload).json()
        # return WasScanConfigurationIterator(self._api,
        #                                     _limit=self._check('limit', 200, int),
        #                                     _offset=self._check('offset', 0, int),
        #                                     # _pages_total=self._check('pages', 3, int),
        #                                     _query=dict(),
        #                                     _path='was/v2/configs/search',
        #                                     _method="POST",
        #                                     _payload=payload,
        #                                     # _api_version=1,
        #                                     _resource='items'
        #                                     )

        # Todo replace the following logic with iterators.
        offset = 0
        limit = 200

        responses = []
        first_response = self._api.post(path=f"was/v2/configs/search/?limit={limit}&offset={offset}",
                                        json=payload).json()
        responses = [*responses, *first_response["items"]]
        total_pages = first_response["pagination"]["total"]

        while offset <= total_pages:
            offset += 1
            new_response = self._api.post(path=f"was/v2/configs/search/?limit={limit}&offset={offset}",
                                          json=payload).json()
            responses = [*responses, *new_response["items"]]

        return responses


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
