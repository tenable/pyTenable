from typing import BinaryIO

from restfly import APIEndpoint, AsyncAPIEndpoint

from .models.files import FileUploadParams, FileUploadResponse


class FilesAPI(APIEndpoint):
    _path = "/file"

    def upload(self, fobj: BinaryIO, *, encrypted: bool = False) -> str:
        """
        Uploads a file into Tenable Vulnerability Management. The returned file id is
        used to reference the uploaded file in other API calls, such as when
        importing scans or targets.

        Args:
            fobj: The file object to upload.
            encrypted: Is the file being uploaded encrypted?

        Returns:
            The name of the uploaded file. If a file with the same name already
            exists, an underscore and a number are appended to the name.

        Example:
            >>> with open("scan_targets.txt", "rb") as fobj:
            ...     file_id = cloud.platform.files.upload(fobj)
        """
        resp = self._post(
            "/upload",
            params=FileUploadParams(encrypted=encrypted or None),
            files={"Filedata": fobj},
            response_model=FileUploadResponse,
        )
        return resp.file_id


class AsyncFilesAPI(AsyncAPIEndpoint):
    _path = "/file"

    async def upload(self, fobj: BinaryIO, *, encrypted: bool = False) -> str:
        """
        Uploads a file into Tenable Vulnerability Management. The returned file id is
        used to reference the uploaded file in other API calls, such as when
        importing scans or targets.

        Args:
            fobj: The file object to upload.
            encrypted: Is the file being uploaded encrypted?

        Returns:
            The name of the uploaded file. If a file with the same name already
            exists, an underscore and a number are appended to the name.

        Example:
            >>> with open("scan_targets.txt", "rb") as fobj:
            ...     file_id = await cloud.platform.files.upload(fobj)
        """
        resp = await self._post(
            "/upload",
            params=FileUploadParams(encrypted=encrypted or None),
            files={"Filedata": fobj},
            response_model=FileUploadResponse,
        )
        return resp.file_id
