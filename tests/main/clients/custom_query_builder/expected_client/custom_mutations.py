from typing import Any, Optional

from .custom_fields import UpdateMetadataFields


class Mutation:
    @classmethod
    def update_metadata(cls, id: str) -> UpdateMetadataFields:
        return UpdateMetadataFields(
            field_name="updateMetadata", arguments={"id": {"type": "ID!", "value": id}}
        )
