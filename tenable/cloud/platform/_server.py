from restfly import APIEndpoint, AsyncAPIEndpoint

from .models.server import ServerProperties, ServerStatus


class ServerAPI(APIEndpoint):
    _path = "/server"

    def status(self) -> ServerStatus:
        """
        Returns the current status of the Tenable Cloud instance.

        Returns:
            The server status.
        """
        return self._get("/status", response_model=ServerStatus)

    def properties(self) -> ServerProperties:
        """
        Returns the server version and other properties of the Tenable
        Cloud instance.

        Returns:
            The server properties.
        """
        return self._get("/properties", response_model=ServerProperties)


class AsyncServerAPI(AsyncAPIEndpoint):
    _path = "/server"

    async def status(self) -> ServerStatus:
        """
        Returns the current status of the Tenable Cloud instance.

        Returns:
            The server status.
        """
        return await self._get("/status", response_model=ServerStatus)

    async def properties(self) -> ServerProperties:
        """
        Returns the server version and other properties of the Tenable
        Cloud instance.

        Returns:
            The server properties.
        """
        return await self._get("/properties", response_model=ServerProperties)
