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
from tenable.base.endpoint import APIEndpoint


class WasAPI(APIEndpoint):
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
        self
        payload = dict()

        if "single_filter" in kwargs:
            payload = _tuple_to_filter(kwargs["single_filter"])

        if "single_filter" in kwargs and (("and_filter" in kwargs) or ("or_filter" in kwargs)):
            raise AttributeError("When passing single_filter, you cannot pass and_filter or or_filter alongside.")

        if "and_filter" in kwargs and ("single_filter" not in kwargs):
            payload["AND"] = _tuples_to_filters(kwargs["and_filter"])

        if "or_filter" in kwargs and ("single_filter" not in kwargs):
            payload["OR"] = _tuples_to_filters(kwargs["or_filter"])

        return payload


def _tuples_to_filters(filter_tuples: list[tuple[str, str, str]]) -> list:
    """
    Accepts a list of tuples with three strings, and returns a filter object list.
    """
    return [_tuple_to_filter(t) for t in filter_tuples]


def _tuple_to_filter(filter_tuple: tuple[str, str, str]) -> dict:
    """
    Accepts a tuple with three strings, and returns a filter object.
    """
    return {
        "field": filter_tuple[0],
        "operator": filter_tuple[1],
        "value": filter_tuple[2]
    }
