from restfly import APIEndpoint, AsyncAPIEndpoint

from .models import AllowedIPAddresses


class AccessControlApiAPI(APIEndpoint):
    _path = "/access-control/v1/api-security-settings"

    def get_allowed_ips(self) -> AllowedIPAddresses:
        """
        Returns the list of IPv4 and IPv6 addresses allowed to access the Tenable Cloud
        environment.
        """
        return self._get(response_model=AllowedIPAddresses)

    def update_allowed_ips(
        self, ipv4: list[str] | None = None, ipv6: list[str] | None = None
    ) -> None:
        """
        Updates the list of IPv4 and IPv6 addresses allowed to access the Tenable Cloud
        environment.
        """
        self._put(json=AllowedIPAddresses(ipv4=ipv4, ipv6=ipv6))


class AsyncAccessControlApiAPI(AsyncAPIEndpoint):
    _path = "/access-control/v1/api-security-settings"

    async def get_allowed_ips(self) -> AllowedIPAddresses:
        """
        Returns the list of IPv4 and IPv6 addresses allowed to access the Tenable Cloud
        environment.
        """
        return await self._get(response_model=AllowedIPAddresses)

    async def update_allowed_ips(
        self, ipv4: list[str] | None = None, ipv6: list[str] | None = None
    ) -> None:
        """
        Updates the list of IPv4 and IPv6 addresses allowed to access the Tenable Cloud
        environment.
        """
        await self._put(json=AllowedIPAddresses(ipv4=ipv4, ipv6=ipv6))
