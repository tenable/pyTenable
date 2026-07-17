from restfly import APIEndpoint, AsyncAPIEndpoint

from .models.filters import (
    AgentFilters,
    AssetFilters,
    CredentialFilters,
    ReportFilters,
    ScanFilters,
    ScanHistoryFilters,
    VulnerabilityFilters,
)


class FiltersAPI(APIEndpoint):
    _path = "/filters"

    def agent(self) -> AgentFilters:
        """
        Returns the Agent filters.
        """
        return self._get("/scans/agents", response_model=AgentFilters)

    def asset(self) -> AssetFilters:
        """
        Returns the Asset filters.
        """
        return self._get("/workbenches/assets", response_model=AssetFilters)

    def credential(self) -> CredentialFilters:
        """
        Returns the Credential filters.
        """
        return self._get("/credentials", response_model=CredentialFilters)

    def report(self) -> ReportFilters:
        """
        Returns the Report filters.
        """
        return self._get("/reports/export", response_model=ReportFilters)

    def scan(self) -> ScanFilters:
        """
        Returns the Scan filters.
        """
        return self._get("/scans/reports", response_model=ScanFilters)

    def scan_history(self) -> ScanHistoryFilters:
        """
        Returns the Scan History filters.
        """
        return self._get("/scans/reports/history", response_model=ScanHistoryFilters)

    def vulnerability(self) -> VulnerabilityFilters:
        """
        Returns the Vulnerability filters.
        """
        return self._get(
            "/workbenches/vulnerabilities", response_model=VulnerabilityFilters
        )


class AsyncFiltersAPI(AsyncAPIEndpoint):
    _path = "/filters"

    async def agent(self) -> AgentFilters:
        """
        Returns the Agent filters.
        """
        return await self._get("/scans/agents", response_model=AgentFilters)

    async def asset(self) -> AssetFilters:
        """
        Returns the Asset filters.
        """
        return await self._get("/workbenches/assets", response_model=AssetFilters)

    async def credential(self) -> CredentialFilters:
        """
        Returns the Credential filters.
        """
        return await self._get("/credentials", response_model=CredentialFilters)

    async def report(self) -> ReportFilters:
        """
        Returns the Report filters.
        """
        return await self._get("/reports/export", response_model=ReportFilters)

    async def scan(self) -> ScanFilters:
        """
        Returns the Scan filters.
        """
        return await self._get("/scans/reports", response_model=ScanFilters)

    async def scan_history(self) -> ScanHistoryFilters:
        """
        Returns the Scan History filters.
        """
        return await self._get(
            "/scans/reports/history", response_model=ScanHistoryFilters
        )

    async def vulnerability(self) -> VulnerabilityFilters:
        """
        Returns the Vulnerability filters.
        """
        return await self._get(
            "/workbenches/vulnerabilities", response_model=VulnerabilityFilters
        )
