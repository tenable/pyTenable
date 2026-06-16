from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .models import (
    ACActions,
    AccessControlPermission,
    AccessControlPermissionBase,
    AccessControlPermObj,
    AccessControlSubject,
    ListPermissions,
    UserGroupPermissions,
)


class AccessControlPermissionsAPI(APIEndpoint):
    _path = "/api/v3/access-control/permissions"

    def create(
        self,
        name: str,
        actions: list[ACActions],
        objects: list[AccessControlPermObj],
        subjects: list[AccessControlSubject],
    ) -> AccessControlPermission:
        """
        Creates a new permission object

        Args:
            name: Name of the permission
            actions: List of actions the permission can perform
            objects: List of objects that the actions are acted upon
            subjects: List of subjects that the permission pertains to

        Returns:
            The created permission object
        """
        perm = AccessControlPermissionBase(
            name=name, actions=actions, objects=objects, subjects=subjects
        )
        return self._post(json=perm, response_model=AccessControlPermission)

    def get(self) -> list[AccessControlPermission]:
        """
        Lists the permissions in the system

        Returns:
            list of permission objects
        """
        resp = self._get(response_model=ListPermissions)
        return resp.permissions

    def details(self, permission_uuid: UUID) -> AccessControlPermission:
        """
        Retrieves the details for a specific permission

        Args:
            permission_uuid: The unique id for the permission object

        Returns:
            The specified permission object
        """
        return self._get(
            f"/{scrub(permission_uuid)}", response_model=AccessControlPermission
        )

    def update(
        self,
        permission_uuid: UUID,
        name: str | None = None,
        actions: list[ACActions] | None = None,
        objects: list[AccessControlPermObj] | None = None,
        subjects: list[AccessControlSubject] | None = None,
    ) -> AccessControlPermission:
        """
        Updates the permission object

        Args:
            permission_uuid: The unique id of the object to update
            name: Name of the object
            actions: List of actions the permission can perform
            objects: List of objects that the actions are acted upon
            subjects: List of subjects that the permission pertains to

        Returns:
            The updated permission object
        """
        perm = self.details(permission_uuid)
        new = AccessControlPermissionBase(
            name=name if name else perm.name,
            actions=actions if actions else perm.actions,
            objects=objects if objects else perm.objects,
            subjects=subjects if subjects else perm.subjects,
        )
        return self._put(
            f"/{scrub(permission_uuid)}",
            json=new,
            response_model=AccessControlPermission,
        )

    def delete(self, permission_uuid: UUID) -> None:
        """
        Deletes the specified permission object

        Args:
            permission_uuid: The unique id of the object to delete
        """
        self._delete(f"/{scrub(permission_uuid)}")

    def get_user_permissions(self, user_uuid: UUID) -> UserGroupPermissions:
        """
        Lists the permission objects that are applied to the user as well as the ones
        that are not applied, but available.

        Args:
            user_uuid: The unique id of the user object

        Returns:
            Assigned permissions object
        """
        return self._get(
            f"/users/{scrub(user_uuid)}", response_model=UserGroupPermissions
        )

    def get_group_permissions(self, group_uuid: UUID) -> UserGroupPermissions:
        """
        Lists the permission objects that are applied to the group as well as the ones
        that are not applied, but available.

        Args:
            group_uuid: The unique id of the group object

        Returns:
            Assigned permissions object
        """
        return self._get(
            f"/user-groups/{scrub(group_uuid)}", response_model=UserGroupPermissions
        )

    def get_self_permissions(self) -> UserGroupPermissions:
        """
        Lists the current user's permission objects.

        Returns:
            Assigned permissions object
        """
        return self._get("/users/me", response_model=UserGroupPermissions)


class AsyncAccessControlPermissionsAPI(AsyncAPIEndpoint):
    _path = "/api/v3/access-control/permissions"

    async def create(
        self,
        name: str,
        actions: list[ACActions],
        objects: list[AccessControlPermObj],
        subjects: list[AccessControlSubject],
    ) -> AccessControlPermission:
        """
        Creates a new permission object

        Args:
            name: Name of the permission
            actions: List of actions the permission can perform
            objects: List of objects that the actions are acted upon
            subjects: List of subjects that the permission pertains to

        Returns:
            The created permission object
        """
        perm = AccessControlPermissionBase(
            name=name, actions=actions, objects=objects, subjects=subjects
        )
        return await self._post(json=perm, response_model=AccessControlPermission)

    async def get(self) -> list[AccessControlPermission]:
        """
        Lists the permissions in the system

        Returns:
            list of permission objects
        """
        resp = await self._get(response_model=ListPermissions)
        return resp.permissions

    async def details(self, permission_uuid: UUID) -> AccessControlPermission:
        """
        Retrieves the details for a specific permission

        Args:
            permission_uuid: The unique id for the permission object

        Returns:
            The specified permission object
        """
        return await self._get(
            f"/{scrub(permission_uuid)}", response_model=AccessControlPermission
        )

    async def update(
        self,
        permission_uuid: UUID,
        name: str | None = None,
        actions: list[ACActions] | None = None,
        objects: list[AccessControlPermObj] | None = None,
        subjects: list[AccessControlSubject] | None = None,
    ) -> AccessControlPermission:
        """
        Updates the permission object

        Args:
            permission_uuid: The unique id of the object to update
            name: Name of the object
            actions: List of actions the permission can perform
            objects: List of objects that the actions are acted upon
            subjects: List of subjects that the permission pertains to

        Returns:
            The updated permission object
        """
        perm = await self.details(permission_uuid)
        new = AccessControlPermissionBase(
            name=name if name else perm.name,
            actions=actions if actions else perm.actions,
            objects=objects if objects else perm.objects,
            subjects=subjects if subjects else perm.subjects,
        )
        return await self._put(
            f"/{scrub(permission_uuid)}",
            json=new,
            response_model=AccessControlPermission,
        )

    async def delete(self, permission_uuid: UUID) -> None:
        """
        Deletes the specified permission object

        Args:
            permission_uuid: The unique id of the object to delete
        """
        await self._delete(f"/{scrub(permission_uuid)}")

    async def get_user_permissions(self, user_uuid: UUID) -> UserGroupPermissions:
        """
        Lists the permission objects that are applied to the user as well as the ones
        that are not applied, but available.

        Args:
            user_uuid: The unique id of the user object

        Returns:
            Assigned permissions object
        """
        return await self._get(
            f"/users/{scrub(user_uuid)}", response_model=UserGroupPermissions
        )

    async def get_group_permissions(self, group_uuid: UUID) -> UserGroupPermissions:
        """
        Lists the permission objects that are applied to the group as well as the ones
        that are not applied, but available.

        Args:
            group_uuid: The unique id of the group object

        Returns:
            Assigned permissions object
        """
        return await self._get(
            f"/user-groups/{scrub(group_uuid)}", response_model=UserGroupPermissions
        )

    async def get_self_permissions(self) -> UserGroupPermissions:
        """
        Lists the current user's permission objects.

        Returns:
            Assigned permissions object
        """
        return await self._get("/users/me", response_model=UserGroupPermissions)
