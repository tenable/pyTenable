from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .models import (
    AccessControlGroup,
    AccessControlUser,
    ListGroupsResponse,
    ListUsersResponse,
)


class AccessControlGroupAPI(APIEndpoint):
    _path = "/groups"

    def create(self, name: str) -> AccessControlGroup:
        """
        Creates a group

        Args:
            name: The name of the group

        Returns:
            The created group object
        """
        return self._post(json={"name": name}, response_model=AccessControlGroup)

    def update(self, group_id: int, name: str) -> AccessControlGroup:
        """
        Updates the specified group

        Args:
            group_id: Unique id for the group
            name: The new name for the group

        Returns:
            The updated group object
        """
        return self._put(
            scrub(group_id), json={"name": name}, response_model=AccessControlGroup
        )

    def delete(self, group_id: int) -> None:
        """
        Deletes the specified group

        Args:
            group_id: Unique id for the group
        """
        self._delete(scrub(group_id))

    def get(self) -> list[AccessControlGroup]:
        """
        Lists groups

        Returns:
            List of group objects
        """
        resp = self._get(response_model=ListGroupsResponse)
        return resp.groups

    def get_users(self, group_id: int) -> list[AccessControlUser]:
        """
        Lists the users that are members of the group

        Args:
            group_id: Unique id of the group

        Returns:
            List of associated user objects
        """
        resp = self._get(f"/{scrub(group_id)}", response_model=ListUsersResponse)
        return resp.users

    def add_user(self, group_id: int, user_id: int) -> None:
        """
        Adds a user to the group

        Args:
            group_id: Unique id of the group
            user_id: Unique id of the user
        """
        self._post(f"/{scrub(group_id)}/users/{scrub(user_id)}")

    def remove_user(self, group_id: int, user_id: int) -> None:
        """
        Removes a user from a group

        Args:
            group_id: Unique id of the group
            user_id: Unique id of the user
        """
        self._delete(f"/{scrub(group_id)}/users/{scrub(user_id)}")


class AsyncAccessControlGroupAPI(AsyncAPIEndpoint):
    _path = "/groups"

    async def create(self, name: str) -> AccessControlGroup:
        """
        Creates a group

        Args:
            name: The name of the group

        Returns:
            The created group object
        """
        return await self._post(json={"name": name}, response_model=AccessControlGroup)

    async def update(self, group_id: int, name: str) -> AccessControlGroup:
        """
        Updates the specified group

        Args:
            group_id: Unique id for the group
            name: The new name for the group

        Returns:
            The updated group object
        """
        return await self._put(
            f"/{scrub(group_id)}",
            json={"name": name},
            response_model=AccessControlGroup,
        )

    async def delete(self, group_id: int) -> None:
        """
        Deletes the specified group

        Args:
            group_id: Unique id for the group
        """
        await self._delete(f"/{scrub(group_id)}")

    async def get(self) -> list[AccessControlGroup]:
        """
        Lists groups

        Returns:
            List of group objects
        """
        resp = await self._get(response_model=ListGroupsResponse)
        return resp.groups

    async def get_users(self, group_id: int) -> list[AccessControlUser]:
        """
        Lists the users that are members of the group

        Args:
            group_id: Unique id of the group

        Returns:
            List of associated user objects
        """
        resp = await self._get(f"/{scrub(group_id)}", response_model=ListUsersResponse)
        return resp.users

    async def add_user(self, group_id: int, user_id: int) -> None:
        """
        Adds a user to the group

        Args:
            group_id: Unique id of the group
            user_id: Unique id of the user
        """
        await self._post(f"/{scrub(group_id)}/users/{scrub(user_id)}")

    async def remove_user(self, group_id: int, user_id: int) -> None:
        """
        Removes a user from a group

        Args:
            group_id: Unique id of the group
            user_id: Unique id of the user
        """
        await self._delete(f"/{scrub(group_id)}/users/{scrub(user_id)}")
