from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .models.permissions import (
    ACL,
    ACLRequest,
    ObjectType,
    PermissionsListResponse,
    PermissionsUpdate,
)


class PermissionsAPI(APIEndpoint):
    _path = "/permissions"

    def get(self, object_type: ObjectType, object_id: int) -> list[ACL]:
        """
        Returns the permissions assigned to the specified object.

        Args:
            object_type: The type of object.
            object_id: The unique ID of the object.

        Returns:
            List of the object's permission ACL entries.
        """
        resp = self._get(
            f"/{scrub(object_type)}/{scrub(object_id)}",
            response_model=PermissionsListResponse,
        )
        return resp.acls

    def update(
        self, object_type: ObjectType, object_id: int, acls: list[ACLRequest]
    ) -> None:
        """
        Updates the permissions assigned to the specified object. This
        replaces the object's full set of permission ACL entries.

        Args:
            object_type: The type of object.
            object_id: The unique ID of the object.
            acls: The new list of permission ACL entries for the object.
        """
        self._put(
            f"/{scrub(object_type)}/{scrub(object_id)}",
            json=PermissionsUpdate(acls=acls),
        )


class AsyncPermissionsAPI(AsyncAPIEndpoint):
    _path = "/permissions"

    async def get(self, object_type: ObjectType, object_id: int) -> list[ACL]:
        """
        Returns the permissions assigned to the specified object.

        Args:
            object_type: The type of object.
            object_id: The unique ID of the object.

        Returns:
            List of the object's permission ACL entries.
        """
        resp = await self._get(
            f"/{scrub(object_type)}/{scrub(object_id)}",
            response_model=PermissionsListResponse,
        )
        return resp.acls

    async def update(
        self, object_type: ObjectType, object_id: int, acls: list[ACLRequest]
    ) -> None:
        """
        Updates the permissions assigned to the specified object. This
        replaces the object's full set of permission ACL entries.

        Args:
            object_type: The type of object.
            object_id: The unique ID of the object.
            acls: The new list of permission ACL entries for the object.
        """
        await self._put(
            f"/{scrub(object_type)}/{scrub(object_id)}",
            json=PermissionsUpdate(acls=acls),
        )
