from typing import Any, Optional

from .custom_fields import UpdateMetadataFields


class Mutation:
    @classmethod
    def update_metadata(cls, *, id: Optional[str] = None) -> UpdateMetadataFields:
        return UpdateMetadataFields(field_name="updateMetadata", id=id)
