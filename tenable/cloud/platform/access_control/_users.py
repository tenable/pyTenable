from typing import Literal
from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .models import (
    AccessControlApiKeys,
    AccessControlUser,
    AccessControlUserAuthorizations,
    AccessControlUserAuthorizationsUpdate,
    AccessControlUserCreate,
    AccessControlUserUpdate,
    ListUsersResponse,
)


class AccessControlUserAPI(APIEndpoint):
    _path = "/users"

    def create(
        self,
        *,
        username: str,
        password: str,
        name: str | None = None,
        email: str | None = None,
        role: Literal[
            0,
            "read-only",
            16,
            "basic",
            24,
            "scan_operator",
            32,
            "standard",
            40,
            "scan_manager",
            64,
            "administrator",
        ] = "basic",
    ) -> AccessControlUser:
        """
        Creates a new user.

        Args:
            username: username (login id) for the user.
            password: password for the user.
            name: Name of the user.
            email: Email address for the user.
            role:
                Role of the user. Note that either the integer id or the role name can
                be specified.

        Returns:
            The created user object
        """
        user = AccessControlUserCreate.model_validate(
            {
                "username": username,
                "password": password,
                "name": name,
                "email": email,
                "role": role,
            }
        )
        return self._post(json=user, response_model=AccessControlUser)

    def update(
        self,
        user_id: int | UUID | str,
        *,
        name: str | None = None,
        email: str | None = None,
        enabled: bool | None = None,
        role: Literal[
            0,
            "read-only",
            16,
            "basic",
            24,
            "scan_operator",
            32,
            "standard",
            40,
            "scan_manager",
            64,
            "administrator",
        ]
        | None = None,
    ) -> AccessControlUser:
        """
        Updates an existing user.

        Args:
            user_id: Id of the specified user.
            name: Name of the user.
            email: Email address of the user.
            enabled: Is the user enabled?
            role:
                Role of the user. Note that either the integer id or the role name can
                be specified.

        Returns:
            Updated user record.
        """
        user = self.details(user_id)
        updated = AccessControlUserUpdate.model_validate(
            {
                "name": name if name is not None else user.name,
                "email": email if email is not None else user.email,
                "enabled": enabled if enabled is not None else user.enabled,
                "role": role if role is not None else user.role,
            }
        )
        return self._put(
            f"/{scrub(user_id)}", json=updated, response_model=AccessControlUser
        )

    def details(self, user_id: int | UUID | str) -> AccessControlUser:
        """
        Fetches details for the specified user.

        Args:
            user_id: Id of the specified user.

        Returns:
            User record.
        """
        return self._get(f"/{scrub(user_id)}", response_model=AccessControlUser)

    def delete(
        self, user_id: int | UUID | str, *, successor_id: UUID | str | None = None
    ) -> None:
        """
        Deletes the specified user.

        Args:
            user_id: Id of the user to delete.
            successor_id: User id to inherit the objects of the deleted user.
        """
        params = {}
        if successor_id is not None:
            params["successor_user_uuid"] = str(successor_id)
        self._delete(f"/{scrub(user_id)}", params=params)

    def get(self) -> list[AccessControlUser]:
        """
        Fetches the list of users.

        Returns:
            List of user records.
        """
        resp = self._get(response_model=ListUsersResponse)
        return resp.users

    def change_password(
        self, user_id: int | UUID | str, *, password: str, temporary: bool = True
    ) -> None:
        """
        Resets the password for the specified user.

        Args:
            user_id: Id of the specified user.
            password: The new password to set for the user.
            temporary: Should the user be required to change the password next login?
        """
        self._put(
            f"/{scrub(user_id)}/chpasswd",
            json={"password": str(password), "temporary": bool(temporary)},
        )

    def enabled(self, user_id: int | UUID | str, enabled: bool) -> AccessControlUser:
        """
        Set the enabled/disabled state of a given user.

        Args:
            user_id: Id of the specified user.
            enabled: The new enabled state of the user.

        Returns:
            The updated user record.
        """
        return self._put(
            f"/{scrub(user_id)}/enabled",
            json={"enabled": bool(enabled)},
            response_model=AccessControlUser,
        )

    def generate_api_keys(self, user_id: int | UUID | str) -> AccessControlApiKeys:
        """
        Generates a new set of API keys for the user, replacing the old set.

        Args:
            user_id: If of the specified user.

        Returns:
            The new API Keys.
        """
        return self._put(f"/{scrub(user_id)}/keys", response_model=AccessControlApiKeys)

    def configure_two_factor(
        self,
        user_id: int | UUID | str,
        *,
        sms_phone: str,
        sms_enabled: bool,
        email_enabled: bool,
    ) -> None:
        """
        Configures the two-factor authentication options within Tenable Cloud.

        Args:
            user_id: Id of the specified user.
            sms_phone: The phone number to use for SMS codes.
            sms_enabled: Is SMS second factor enabled?
            email_enabled: Is email second factor enabled?
        """
        self._put(
            f"/{scrub(user_id)}/two-factor",
            json={
                "sms_phone": str(sms_phone),
                "sms_enabled": bool(sms_enabled),
                "email_enabled": bool(email_enabled),
            },
        )

    def send_sms_verification(
        self, user_id: int | UUID | str, *, sms_phone: str
    ) -> None:
        """
        Sends a one-time SMS code to be use to activate two-factor SMS verification.

        Args:
            user_id: Id of the specified user.
            sms_phone: The phone number to send the verification request to.
        """
        self._post(
            f"/{scrub(user_id)}/two-factor/send-verification",
            json={"sms_phone": str(sms_phone)},
        )

    def validate_sms_verification(
        self, user_id: int | UUID | str, *, code: str
    ) -> None:
        """
        Validates the one-time verification code send to the specified phone number.

        Args:
            user_id: Id of the specified user.
            code: Verification code sent via text message.
        """
        self._post(
            f"/{scrub(user_id)}/two-factor/verify-code",
            json={"verification_code": str(code)},
        )

    def get_authorizations(
        self, user_id: int | UUID | str
    ) -> AccessControlUserAuthorizations:
        """
        Fetch the account authorizations for the given user.

        Args:
            user_id: Id of the specified user.

        Returns:
            Currently configured authorizations.
        """
        return self._get(
            f"/{scrub(user_id)}/authorizations",
            response_model=AccessControlUserAuthorizations,
        )

    def update_authorizations(
        self,
        user_id: int | UUID | str,
        *,
        api: bool | None = None,
        password: bool | None = None,
        saml: bool | None = None,
        mfa: bool | None = None,
    ) -> None:
        """
        Update the account authorizations for the given user.

        Args:
            user_id: Id of the specified user.
            api: Are API keys allowed for the user?
            mfa: Is MFA enrollment required?
            password: Is password authentication (UI access) allowed?
            saml: Is SAML authentication allowed?
        """
        auths = self.get_authorizations(user_id)
        updates = AccessControlUserAuthorizationsUpdate(
            api=api if api is not None else auths.api,
            password=password if password is not None else auths.password,
            saml=saml if saml is not None else auths.saml,
            mfa=mfa,
        )
        self._put(f"/{scrub(user_id)}/authorizations", json=updates)


class AsyncAccessControlUserAPI(AsyncAPIEndpoint):
    _path = "/users"

    async def create(
        self,
        *,
        username: str,
        password: str,
        name: str | None = None,
        email: str | None = None,
        role: Literal[
            0,
            "read-only",
            16,
            "basic",
            24,
            "scan_operator",
            32,
            "standard",
            40,
            "scan_manager",
            64,
            "administrator",
        ] = "basic",
    ) -> AccessControlUser:
        """
        Creates a new user.

        Args:
            username: username (login id) for the user.
            password: password for the user.
            name: Name of the user.
            email: Email address for the user.
            role:
                Role of the user. Note that either the integer id or the role name can
                be specified.

        Returns:
            The created user object
        """
        user = AccessControlUserCreate.model_validate(
            {
                "username": username,
                "password": password,
                "name": name,
                "email": email,
                "role": role,
            }
        )
        return await self._post(json=user, response_model=AccessControlUser)

    async def update(
        self,
        user_id: int | UUID | str,
        *,
        name: str | None = None,
        email: str | None = None,
        enabled: bool | None = None,
        role: Literal[
            0,
            "read-only",
            16,
            "basic",
            24,
            "scan_operator",
            32,
            "standard",
            40,
            "scan_manager",
            64,
            "administrator",
        ]
        | None = None,
    ) -> AccessControlUser:
        """
        Updates an existing user.

        Args:
            user_id: Id of the specified user.
            name: Name of the user.
            email: Email address of the user.
            enabled: Is the user enabled?
            role:
                Role of the user. Note that either the integer id or the role name can
                be specified.

        Returns:
            Updated user record.
        """
        user = await self.details(user_id)
        updated = AccessControlUserUpdate.model_validate(
            {
                "name": name if name is not None else user.name,
                "email": email if email is not None else user.email,
                "enabled": enabled if enabled is not None else user.enabled,
                "role": role if role is not None else user.role,
            }
        )
        return await self._put(
            f"/{scrub(user_id)}", json=updated, response_model=AccessControlUser
        )

    async def details(self, user_id: int | UUID | str) -> AccessControlUser:
        """
        Fetches details for the specified user.

        Args:
            user_id: Id of the specified user.

        Returns:
            User record.
        """
        return await self._get(f"/{scrub(user_id)}", response_model=AccessControlUser)

    async def delete(
        self, user_id: int | UUID | str, *, successor_id: UUID | str | None = None
    ) -> None:
        """
        Deletes the specified user.

        Args:
            user_id: Id of the user to delete.
            successor_id: User id to inherit the objects of the deleted user.
        """
        params = {}
        if successor_id is not None:
            params["successor_user_uuid"] = str(successor_id)
        await self._delete(f"/{scrub(user_id)}", params=params)

    async def get(self) -> list[AccessControlUser]:
        """
        Fetches the list of users.

        Returns:
            List of user records.
        """
        resp = await self._get(response_model=ListUsersResponse)
        return resp.users

    async def change_password(
        self, user_id: int | UUID | str, *, password: str, temporary: bool = True
    ) -> None:
        """
        Resets the password for the specified user.

        Args:
            user_id: Id of the specified user.
            password: The new password to set for the user.
            temporary: Should the user be required to change the password next login?
        """
        await self._put(
            f"/{scrub(user_id)}/chpasswd",
            json={"password": str(password), "temporary": bool(temporary)},
        )

    async def enabled(
        self, user_id: int | UUID | str, enabled: bool
    ) -> AccessControlUser:
        """
        Set the enabled/disabled state of a given user.

        Args:
            user_id: Id of the specified user.
            enabled: The new enabled state of the user.

        Returns:
            The updated user record.
        """
        return await self._put(
            f"/{scrub(user_id)}/enabled",
            json={"enabled": bool(enabled)},
            response_model=AccessControlUser,
        )

    async def generate_api_keys(
        self, user_id: int | UUID | str
    ) -> AccessControlApiKeys:
        """
        Generates a new set of API keys for the user, replacing the old set.

        Args:
            user_id: If of the specified user.

        Returns:
            The new API Keys.
        """
        return await self._put(
            f"/{scrub(user_id)}/keys", response_model=AccessControlApiKeys
        )

    async def configure_two_factor(
        self,
        user_id: int | UUID | str,
        *,
        sms_phone: str,
        sms_enabled: bool,
        email_enabled: bool,
    ) -> None:
        """
        Configures the two-factor authentication options within Tenable Cloud.

        Args:
            user_id: Id of the specified user.
            sms_phone: The phone number to use for SMS codes.
            sms_enabled: Is SMS second factor enabled?
            email_enabled: Is email second factor enabled?
        """
        await self._put(
            f"/{scrub(user_id)}/two-factor",
            json={
                "sms_phone": str(sms_phone),
                "sms_enabled": bool(sms_enabled),
                "email_enabled": bool(email_enabled),
            },
        )

    async def send_sms_verification(
        self, user_id: int | UUID | str, *, sms_phone: str
    ) -> None:
        """
        Sends a one-time SMS code to be use to activate two-factor SMS verification.

        Args:
            user_id: Id of the specified user.
            sms_phone: The phone number to send the verification request to.
        """
        await self._post(
            f"/{scrub(user_id)}/two-factor/send-verification",
            json={"sms_phone": str(sms_phone)},
        )

    async def validate_sms_verification(
        self, user_id: int | UUID | str, *, code: str
    ) -> None:
        """
        Validates the one-time verification code send to the specified phone number.

        Args:
            user_id: Id of the specified user.
            code: Verification code sent via text message.
        """
        await self._post(
            f"/{scrub(user_id)}/two-factor/verify-code",
            json={"verification_code": str(code)},
        )

    async def get_authorizations(
        self, user_id: int | UUID | str
    ) -> AccessControlUserAuthorizations:
        """
        Fetch the account authorizations for the given user.

        Args:
            user_id: Id of the specified user.

        Returns:
            Currently configured authorizations.
        """
        return await self._get(
            f"/{scrub(user_id)}/authorizations",
            response_model=AccessControlUserAuthorizations,
        )

    async def update_authorizations(
        self,
        user_id: int | UUID | str,
        *,
        api: bool | None = None,
        password: bool | None = None,
        saml: bool | None = None,
        mfa: bool | None = None,
    ) -> None:
        """
        Update the account authorizations for the given user.

        Args:
            user_id: Id of the specified user.
            api: Are API keys allowed for the user?
            mfa: Is MFA enrollment required?
            password: Is password authentication (UI access) allowed?
            saml: Is SAML authentication allowed?
        """
        auths = await self.get_authorizations(user_id)
        updates = AccessControlUserAuthorizationsUpdate(
            api=api if api is not None else auths.api,
            password=password if password is not None else auths.password,
            saml=saml if saml is not None else auths.saml,
            mfa=mfa,
        )
        await self._put(f"/{scrub(user_id)}/authorizations", json=updates)
