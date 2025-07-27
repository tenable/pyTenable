"""
Findings
========

Methods described in this section relate to the inventory findings API.
These methods can be accessed at ``TenableExposureManagement.inventory.findings``.

.. rst-class:: hide-signature
.. autoclass:: FindingsAPI
    :members:

"""

from typing import Optional
from urllib.parse import urlencode

from tenable.base.endpoint import APIEndpoint
from tenable.tenableone.inventory.findings.schema import Findings
from tenable.tenableone.inventory.schema import Field, Properties, QueryMode, PropertyFilter, SortDirection


class FindingsAPI(APIEndpoint):
    def list_properties(self) -> list[Field]:
        """
        Retrieve finding properties

        Returns:
            The finding properties.

        Examples:
            >>> properties = tenable_inventory.finding.list_properties()
            >>> for finding_property in properties:
            ...     pprint(finding_property)

        """
        finding_properties_response: dict[str, list[dict]] = self._get(
            path="api/v1/t1/inventory/findings/properties"
        )
        return Properties(**finding_properties_response).data
    #
    # def list(
    #         self,
    #         query_text: Optional[str] = None,
    #         query_mode: Optional[QueryMode] = None,
    #         filters: Optional[list[PropertyFilter]] = None,
    #         extra_properties: Optional[list[str]] = None,
    #         offset: Optional[int] = None,
    #         limit: Optional[int] = None,
    #         sort_by: Optional[str] = None,
    #         sort_direction: Optional[SortDirection] = None,
    # ) -> Findings:
    #     """
    #     Retrieve findings
    #
    #     Args:
    #        query_text (str, optional):
    #            The text to search for.
    #        query_mode (QueryMode, optional):
    #            The search mode. Defaults to QueryMode.SIMPLE.
    #        filters (list, optional):
    #            A list of filters to apply. Defaults to None.
    #        extra_properties (list, optional):
    #            Additional properties to include in the response. Defaults to None.
    #        offset (int, optional):
    #            Number of records to skip. Defaults to 0.
    #        limit (int, optional):
    #            Maximum number of records per page. Defaults to 1000.
    #        sort_by (str, optional):
    #            Field to sort by.
    #        sort_direction (SortDirection, optional):
    #            Sorting direction, either SortDirection.ASC or SortDirection.DESC.
    #
    #     Returns:
    #        The request assets.
    #
    #     Example:
    #        >>> tenable_inventory_findings = tenable_inventory.finding.list()
    #        >>> for finding in tenable_inventory_findings:
    #        ...     pprint(finding)
    #
    #     """
    #     payload = {}
    #
    #     # TODO: check what is the actual contract
    #     if query_text is not None and query_mode is not None and filters is not None:
    #         payload = {
    #             "query": {"text": query_text, "mode": query_mode.value},
    #             "filters": [filter_.model_dump(mode="json") for filter_ in filters]
    #             if filters is not None
    #             else [],
    #         }
    #     base_path = "api/v1/t1/inventory/findings/search"
    #     query_params = {}
    #
    #     if extra_properties is not None:
    #         query_params["extra_properties"] = ",".join(extra_properties)
    #     if offset is not None:
    #         query_params["offset"] = offset
    #     if limit is not None:
    #         query_params["limit"] = limit
    #     if sort_by is not None and sort_direction is not None:
    #         query_params["sort"] = f"{sort_by}:{sort_direction}"
    #
    #     if query_params:
    #         query_string = urlencode(query_params)
    #         path = f"{base_path}?{query_string}"
    #     else:
    #         path = base_path
    #
    #     findings_response: dict = self._post(path=path, json=payload)
    #     return Findings(**findings_response)