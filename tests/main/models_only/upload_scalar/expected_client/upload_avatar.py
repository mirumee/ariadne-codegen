from pydantic import Field

from .base_model import BaseModel


class UploadAvatar(BaseModel):
    upload_avatar: bool = Field(alias="uploadAvatar")
