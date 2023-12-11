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
from typing import List, Optional, Any

from tenable.sc.base import SCEndpoint


def _boolean_string(boolean_value: bool) -> str:
    """
    Returns a boolean string representation of a python Boolean value.
    True returns "true", False returns "false"

    Args:
        boolean_value:

    Returns: str

    """
    return "true" if boolean_value else "false"


class WasScanAPI(SCEndpoint):
    api_route = "wasScan"

    def _build_creation_request(self, **kwargs: Any) -> dict:
        """
        Builds and returns the request object for an SC WAS Scan creation.
        Note: we're converting numbers to strings in this function as the API requires it to be a string.
        Args:
            **kwargs: Properties in the WAS Scan creation request.

        Returns: dict
        """
        request = dict()

        if kwargs["name"]:
            request["name"] = self._check("name", kwargs["name"], str)

        if "type" in kwargs:
            request["type"] = self._check("type", kwargs["type"], str)

        if "description" in kwargs:
            request["description"] = self._check("description", kwargs["description"], str)

        if "repository_id" in kwargs:
            request["repository"] = {
                "id": str(kwargs["repository_id"])
            }

        if "zone_id" in kwargs:
            request["zone"] = {
                "id": str(kwargs["zone_id"])
            }

        if "dhcpTracking" in kwargs:
            request["dhcpTracking"] = _boolean_string(kwargs["dhcpTracking"])

        if "classifyMitigatedAge" in kwargs:
            request["classifyMitigatedAge"] = str(kwargs["classifyMitigatedAge"])

        if "schedule_type" in kwargs:
            request["schedule"] = {
                "type": self._check("schedule_type", kwargs["schedule_type"], str,
                                    choices=["ical", "never", "rollover", "template"])
            }

        if "reports" in kwargs:
            reports = kwargs["reports"]
            if len(reports) > 0:
                request["reports"] = [
                    {
                        "id": self._check("report_id", report[0], int),
                        "reportSource": self._check("reportSource", report[1], str,
                                                    choices=["cumulative", "patched", "individual", "lce", "archive",
                                                             "mobile"])
                    } for report in reports
                ]

        if "assets" in kwargs:
            assets = kwargs["assets"]
            if len(assets) > 0:
                request["assets"] = [
                    {
                        "id": self._check("asset", asset, int)
                    } for asset in assets
                ]

        if "credentials" in kwargs:
            credentials = kwargs["credentials"]
            if len(credentials) > 0:
                request["credentials"] = [
                    {
                        "id": self._check("credentials", credential, int)
                    } for credential in credentials
                ]

        if "emailOnLaunch" in kwargs:
            request["emailOnLaunch"] = _boolean_string(kwargs["emailOnLaunch"])

        if "emailOnFinish" in kwargs:
            request["emailOnFinish"] = _boolean_string(kwargs["emailOnFinish"])

        if "timeoutAction" in kwargs:
            request["timeoutAction"] = self._check("timeoutAction",
                                                   kwargs["timeoutAction"],
                                                   str,
                                                   choices=["discard", "import", "rollover"]
                                                   )

        if "scanningVirtualHosts" in kwargs:
            request["scanningVirtualHosts"] = _boolean_string(kwargs["scanningVirtualHosts"])

        if "rolloverType" in kwargs:
            request["rolloverType"] = self._check("rolloverType",
                                                  kwargs["rolloverType"],
                                                  str,
                                                  choices=["nextDay", "template"]
                                                  )
        if "urlList" in kwargs:
            request["urlList"] = self._check("urlList", kwargs["urlList"], str)

        if "maxScanTime" in kwargs:
            request["maxScanTime"] = str(kwargs["maxScanTime"])

        return request

    def create(self, **kwargs):
        """
        Creates a WAS Scan depending on access and permissions.

        :sc-api:`was-scan: list <Was-Scan.htm#wasScan_POST>`

        Args:
            name (str):
                The name of the scan.
            type (str, optional):
                Type of the scan.
            description (str, optional):
                A description for the scan zone.
            repository_id (int):
                Repository ID.
            zone_id (int, optional):
                Zone ID.
            dhcpTracking (boolean, optional):
                Scould Security Center do DHCP Tracking?
            classifyMitigatedAge (int, optional):
                Classify Mitigated Age
            schedule_type (str, optional):
                Schedule Type includes  "dependent" | "ical" | "never" | "rollover" | "template"
            reports (list, optional):
                This is a List of Tuples of 2 elements. The first element in the tuple should be a number (ID)
                and the last/second element should be a string (reportSource). It can be one of these strings.
                "cumulative" | "patched" | "individual" | "lce" | "archive" | "mobile"
            assets: (list, optional):
                List of Asset IDs.
            credentials (list, optional):
                List of Credential IDs.
            emailOnLaunch (boolean, optional):
                Should we send an email on launch?
            emailOnFinish (boolean, optional):
                Should we send an email upon completion of the scan?
            timeoutAction (str, optional):
                Time out action can be one of these: "discard" | "import" | "rollover"
            scanningVirtualHosts (boolean, optional):
                Should we scan Virtual Hosts?
            rolloverType (str, optional):
                Rollover type should be one of these: "nextDay" | "template"
            urlList (str, optional)
                Valid URL List
            maxScanTime (int, optional)
                Max Scan Time

        Returns:
            :obj:`dict`:
                The newly created WAS Scan.

        Examples:
            >>> zone = sc.was_scan.create(name="Example Scan")
        """
        request = self._build_creation_request(**kwargs)
        return self._api.post(self.api_route, json=request).json()['response']

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

    def details(self, id: Optional[str] = None, uuid: Optional[str] = None, fields: Optional[List[str]] = None) -> dict:
        """
        Retrieves the details of the given WAS Scan. Either id or the uuid should be present

        :sc-api:`was-scan: list <Was-Scan.htm#WASScanRESTReference-/wasScan/{id}>`

        Args:
            id (str, optional):
                ID of the WAS scan to be fetched.
            uuid (str, optional):
                UUID of the WAS scan to be fetched.
            fields (list, optional):
                A list of attributes to return for the scan.

        Returns:
            :obj:`list`:
                A list of WAS Scans.

        Examples:
            >>> sc.was_scan.details(1)
        """
        if (id is not None and uuid is not None) or (id is None and uuid is None):
            raise ValueError(
                "You can only provide id OR UUID, and not both. They cannot both be empty at the same time."
            )

        params = {}
        if fields:
            string_fields = [self._check("fields", f, str) for f in fields]
            params["fields"] = ",".join(string_fields)

        identifier = id if id else uuid

        return self._api.get(f"{self.api_route}/{identifier}", params=params).json()['response']
