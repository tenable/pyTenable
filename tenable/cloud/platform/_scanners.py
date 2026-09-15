from uuid import UUID

from restfly import APIEndpoint, AsyncAPIEndpoint

from tenable.utils import scrub

from .models.scanners import (
    Scanner,
    ScannerAWSTarget,
    ScannerAWSTargetListResponse,
    ScannerBulkDirective,
    ScannerConcurrentUpdate,
    ScannerConfig,
    ScannerDirective,
    ScannerDirectiveTask,
    ScannerKeyResponse,
    ScannerLinkUpdate,
    ScannerListResponse,
    ScannerScan,
    ScannerScanControl,
    ScannerScanAction,
    ScannerScanListResponse,
    ScannerTaskStatus,
    ScannerUpdate,
    ScannerUpdateResult,
)

DEFAULT_SCANNER_UUID = "00000000-0000-0000-0000-00000000000000000000000000001"


class ScannersAPI(APIEndpoint):
    _path = "/scanners"

    def get(self) -> list[Scanner]:
        """
        Returns the list of scanners.

        Returns:
            List of scanner objects.
        """
        resp = self._get(response_model=ScannerListResponse)
        return resp.scanners

    def details(self, scanner_id: int | UUID | str) -> Scanner:
        """
        Returns the details for the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.

        Returns:
            Requested scanner object.
        """
        return self._get(f"/{scrub(scanner_id)}", response_model=Scanner)

    def update(
        self,
        scanner_id: int | UUID | str,
        *,
        name: str | None = None,
        force_plugin_update: bool | None = None,
        force_ui_update: bool | None = None,
        finish_update: bool | None = None,
        registration_code: str | None = None,
        aws_update_interval: int | None = None,
    ) -> ScannerUpdateResult:
        """
        Updates the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.
            name: New name for the scanner.
            force_plugin_update: Force the scanner to perform a plugin update.
            force_ui_update: Force the scanner to perform a UI update.
            finish_update:
                Force the scanner to reboot to complete the update process.
                Only valid when automatic updates are disabled.
            registration_code: Sets the registration code for the scanner.
            aws_update_interval:
                For AWS scanners, how often (in minutes) the scanner should
                check into the platform.

        Returns:
            Updated scanner object.
        """
        return self._put(
            f"/{scrub(scanner_id)}",
            json=ScannerUpdate(
                name=name,
                force_plugin_update=force_plugin_update,
                force_ui_update=force_ui_update,
                finish_update=finish_update,
                registration_code=registration_code,
                aws_update_interval=aws_update_interval,
            ),
            response_model=ScannerUpdateResult,
        )

    def delete(self, scanner_id: int | UUID | str) -> None:
        """
        Deletes the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner to delete.
        """
        self._delete(f"/{scrub(scanner_id)}")

    def key(self, scanner_id: int | UUID | str = DEFAULT_SCANNER_UUID) -> str:
        """
        Returns the linking key for the specified scanner.

        Args:
            scanner_id:
                The ID or UUID of the scanner. Defaults to the default scanner
                UUID, which returns the container's current linking key.

        Returns:
            The scanner's linking key.
        """
        resp = self._get(f"/{scrub(scanner_id)}/key", response_model=ScannerKeyResponse)
        return resp.key

    def set_link_state(self, scanner_id: int | UUID | str, linked: bool) -> None:
        """
        Enables or disables the link between the specified scanner and the
        Tenable Cloud instance.

        Args:
            scanner_id: The unique ID of the scanner.
            linked: Should the scanner be linked (``True``) or unlinked (``False``)?
        """
        self._put(f"/{scrub(scanner_id)}/link", json=ScannerLinkUpdate(link=linked))

    def aws_targets(self, scanner_id: int | UUID | str) -> list[ScannerAWSTarget]:
        """
        Returns the list of AWS targets the scanner can reach.

        Args:
            scanner_id: The unique ID of the scanner.

        Returns:
            List of AWS target objects.
        """
        resp = self._get(
            f"/{scrub(scanner_id)}/aws-targets",
            response_model=ScannerAWSTargetListResponse,
        )
        return resp.targets

    def scans(self, scanner_id: int | UUID | str) -> list[ScannerScan]:
        """
        Returns the scans currently running on the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.

        Returns:
            List of scan objects associated with the scanner.
        """
        resp = self._get(
            f"/{scrub(scanner_id)}/scans", response_model=ScannerScanListResponse
        )
        return resp.scans

    def control_scan(
        self,
        scanner_id: int | UUID | str,
        scan_uuid: UUID | str,
        action: ScannerScanAction,
    ) -> None:
        """
        Performs an action against a scan running on the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.
            scan_uuid: The UUID of the scan.
            action: The action to take upon the scan (``stop``, ``pause``, or ``resume``).
        """
        self._post(
            f"/{scrub(scanner_id)}/scans/{scrub(scan_uuid)}/control",
            json=ScannerScanControl(action=action),
        )

    def get_config(self) -> ScannerConfig:
        """
        Returns the global scanner configuration settings.

        Returns:
            The global scanner configuration.
        """
        return self._get("/config", response_model=ScannerConfig)

    def update_config(
        self,
        *,
        concurrent_update_enabled: bool | None = None,
        concurrent_update_max_scanners: int | None = None,
    ) -> ScannerConfig:
        """
        Updates the global scanner configuration settings.

        Args:
            concurrent_update_enabled:
                Should the number of scanners that can update simultaneously
                be limited?
            concurrent_update_max_scanners:
                The maximum number of scanners that can update plugins at the
                same time. A value of ``0`` prevents scanners from updating
                plugins. Maximum value is ``1000``.

        Returns:
            Updated global scanner configuration.
        """
        config = self.get_config()
        if config.concurrent_update is None:
            config.concurrent_update = ScannerConcurrentUpdate()
        if concurrent_update_enabled is not None:
            config.concurrent_update.enabled = concurrent_update_enabled
        if concurrent_update_max_scanners is not None:
            config.concurrent_update.max_concurrent_update = (
                concurrent_update_max_scanners
            )
        return self._put("/config", json=config, response_model=ScannerConfig)

    def request_status(self, request_status_id: UUID | str) -> ScannerTaskStatus:
        """
        Returns the status of an asynchronous scanner task.

        Args:
            request_status_id: The unique ID of the asynchronous task.

        Returns:
            The status of the requested task.
        """
        return self._get(
            f"/request-status/{scrub(request_status_id)}",
            response_model=ScannerTaskStatus,
        )

    def send_directive(
        self, scanner_uuid: UUID | str, directive: ScannerDirective
    ) -> ScannerDirectiveTask:
        """
        Sends a directive (restart or settings change) to a scanner.

        Args:
            scanner_uuid: The UUID of the scanner.
            directive:
                A :class:`~.models.scanners.ScannerDirective` describing the
                instruction to send (``type="restart"`` or ``type="settings"``).

        Returns:
            Task object for tracking the directive.
        """
        return self._post(
            f"/{scrub(scanner_uuid)}/directives",
            json=directive,
            response_model=ScannerDirectiveTask,
        )

    def send_bulk_directive(
        self,
        directive: ScannerDirective,
        *,
        all_scanners: bool = False,
        scanners: list[UUID | str] | None = None,
    ) -> list[ScannerDirectiveTask]:
        """
        Sends a bulk directive (restart or settings change) to scanners.

        Args:
            directive:
                A :class:`~.models.scanners.ScannerDirective` describing the
                instruction to send (``type="restart"`` or ``type="settings"``).
            all_scanners: Send the directive to all scanners?
            scanners: The UUIDs of the scanners to send the directive to.

        Returns:
            List of task objects, one per targeted scanner.
        """
        return self._post(
            "/bulk/directives",
            json=ScannerBulkDirective(
                all_scanners=all_scanners,
                scanners=[str(s) for s in scanners] if scanners is not None else None,
                directive=directive,
            ),
            response_model=list[ScannerDirectiveTask],
        )


class AsyncScannersAPI(AsyncAPIEndpoint):
    _path = "/scanners"

    async def get(self) -> list[Scanner]:
        """
        Returns the list of scanners.

        Returns:
            List of scanner objects.
        """
        resp = await self._get(response_model=ScannerListResponse)
        return resp.scanners

    async def details(self, scanner_id: int | UUID | str) -> Scanner:
        """
        Returns the details for the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.

        Returns:
            Requested scanner object.
        """
        return await self._get(f"/{scrub(scanner_id)}", response_model=Scanner)

    async def update(
        self,
        scanner_id: int | UUID | str,
        *,
        name: str | None = None,
        force_plugin_update: bool | None = None,
        force_ui_update: bool | None = None,
        finish_update: bool | None = None,
        registration_code: str | None = None,
        aws_update_interval: int | None = None,
    ) -> ScannerUpdateResult:
        """
        Updates the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.
            name: New name for the scanner.
            force_plugin_update: Force the scanner to perform a plugin update.
            force_ui_update: Force the scanner to perform a UI update.
            finish_update:
                Force the scanner to reboot to complete the update process.
                Only valid when automatic updates are disabled.
            registration_code: Sets the registration code for the scanner.
            aws_update_interval:
                For AWS scanners, how often (in minutes) the scanner should
                check into the platform.

        Returns:
            Updated scanner object.
        """
        return await self._put(
            f"/{scrub(scanner_id)}",
            json=ScannerUpdate(
                name=name,
                force_plugin_update=force_plugin_update,
                force_ui_update=force_ui_update,
                finish_update=finish_update,
                registration_code=registration_code,
                aws_update_interval=aws_update_interval,
            ),
            response_model=ScannerUpdateResult,
        )

    async def delete(self, scanner_id: int | UUID | str) -> None:
        """
        Deletes the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner to delete.
        """
        await self._delete(f"/{scrub(scanner_id)}")

    async def key(self, scanner_id: int | UUID | str = DEFAULT_SCANNER_UUID) -> str:
        """
        Returns the linking key for the specified scanner.

        Args:
            scanner_id:
                The ID or UUID of the scanner. Defaults to the default scanner
                UUID, which returns the container's current linking key.

        Returns:
            The scanner's linking key.
        """
        resp = await self._get(
            f"/{scrub(scanner_id)}/key", response_model=ScannerKeyResponse
        )
        return resp.key

    async def set_link_state(self, scanner_id: int | UUID | str, linked: bool) -> None:
        """
        Enables or disables the link between the specified scanner and the
        Tenable Cloud instance.

        Args:
            scanner_id: The unique ID of the scanner.
            linked: Should the scanner be linked (``True``) or unlinked (``False``)?
        """
        await self._put(
            f"/{scrub(scanner_id)}/link", json=ScannerLinkUpdate(link=linked)
        )

    async def aws_targets(self, scanner_id: int | UUID | str) -> list[ScannerAWSTarget]:
        """
        Returns the list of AWS targets the scanner can reach.

        Args:
            scanner_id: The unique ID of the scanner.

        Returns:
            List of AWS target objects.
        """
        resp = await self._get(
            f"/{scrub(scanner_id)}/aws-targets",
            response_model=ScannerAWSTargetListResponse,
        )
        return resp.targets

    async def scans(self, scanner_id: int | UUID | str) -> list[ScannerScan]:
        """
        Returns the scans currently running on the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.

        Returns:
            List of scan objects associated with the scanner.
        """
        resp = await self._get(
            f"/{scrub(scanner_id)}/scans", response_model=ScannerScanListResponse
        )
        return resp.scans

    async def control_scan(
        self,
        scanner_id: int | UUID | str,
        scan_uuid: UUID | str,
        action: ScannerScanAction,
    ) -> None:
        """
        Performs an action against a scan running on the specified scanner.

        Args:
            scanner_id: The unique ID of the scanner.
            scan_uuid: The UUID of the scan.
            action: The action to take upon the scan (``stop``, ``pause``, or ``resume``).
        """
        await self._post(
            f"/{scrub(scanner_id)}/scans/{scrub(scan_uuid)}/control",
            json=ScannerScanControl(action=action),
        )

    async def get_config(self) -> ScannerConfig:
        """
        Returns the global scanner configuration settings.

        Returns:
            The global scanner configuration.
        """
        return await self._get("/config", response_model=ScannerConfig)

    async def update_config(
        self,
        *,
        concurrent_update_enabled: bool | None = None,
        concurrent_update_max_scanners: int | None = None,
    ) -> ScannerConfig:
        """
        Updates the global scanner configuration settings.

        Args:
            concurrent_update_enabled:
                Should the number of scanners that can update simultaneously
                be limited?
            concurrent_update_max_scanners:
                The maximum number of scanners that can update plugins at the
                same time. A value of ``0`` prevents scanners from updating
                plugins. Maximum value is ``1000``.

        Returns:
            Updated global scanner configuration.
        """
        config = await self.get_config()
        if config.concurrent_update is None:
            config.concurrent_update = ScannerConcurrentUpdate()
        if concurrent_update_enabled is not None:
            config.concurrent_update.enabled = concurrent_update_enabled
        if concurrent_update_max_scanners is not None:
            config.concurrent_update.max_concurrent_update = (
                concurrent_update_max_scanners
            )
        return await self._put("/config", json=config, response_model=ScannerConfig)

    async def request_status(self, request_status_id: UUID | str) -> ScannerTaskStatus:
        """
        Returns the status of an asynchronous scanner task.

        Args:
            request_status_id: The unique ID of the asynchronous task.

        Returns:
            The status of the requested task.
        """
        return await self._get(
            f"/request-status/{scrub(request_status_id)}",
            response_model=ScannerTaskStatus,
        )

    async def send_directive(
        self, scanner_uuid: UUID | str, directive: ScannerDirective
    ) -> ScannerDirectiveTask:
        """
        Sends a directive (restart or settings change) to a scanner.

        Args:
            scanner_uuid: The UUID of the scanner.
            directive:
                A :class:`~.models.scanners.ScannerDirective` describing the
                instruction to send (``type="restart"`` or ``type="settings"``).

        Returns:
            Task object for tracking the directive.
        """
        return await self._post(
            f"/{scrub(scanner_uuid)}/directives",
            json=directive,
            response_model=ScannerDirectiveTask,
        )

    async def send_bulk_directive(
        self,
        directive: ScannerDirective,
        *,
        all_scanners: bool = False,
        scanners: list[UUID | str] | None = None,
    ) -> list[ScannerDirectiveTask]:
        """
        Sends a bulk directive (restart or settings change) to scanners.

        Args:
            directive:
                A :class:`~.models.scanners.ScannerDirective` describing the
                instruction to send (``type="restart"`` or ``type="settings"``).
            all_scanners: Send the directive to all scanners?
            scanners: The UUIDs of the scanners to send the directive to.

        Returns:
            List of task objects, one per targeted scanner.
        """
        return await self._post(
            "/bulk/directives",
            json=ScannerBulkDirective(
                all_scanners=all_scanners,
                scanners=[str(s) for s in scanners] if scanners is not None else None,
                directive=directive,
            ),
            response_model=list[ScannerDirectiveTask],
        )
