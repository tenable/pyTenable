from typing import Annotated

from pydantic import Field

from tenable.cloud._common import BaseModel, BoolInt


class FileUploadParams(BaseModel):
    encrypted: Annotated[BoolInt | None, Field(alias="no_enc")] = None


class FileUploadResponse(BaseModel):
    file_id: Annotated[str, Field(alias="fileuploaded")]
