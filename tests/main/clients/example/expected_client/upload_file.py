from pydantic import Field

from .base_model import BaseModel


class UploadFile(BaseModel):
    file_upload: bool = Field(alias="fileUpload")
