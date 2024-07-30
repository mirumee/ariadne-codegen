from typing import Any, Dict, Optional

from .custom_fields import UpdateMetadataFields


class Mutation:
    @classmethod
    def update_metadata(cls, id: str) -> UpdateMetadataFields:
        arguments: Dict[str, Dict[str, Any]] = {"id": {"type": "ID!", "value": id}}
        cleared_arguments = {
            key: value for key, value in arguments.items() if value["value"] is not None
        }
        return UpdateMetadataFields(
            field_name="updateMetadata", arguments=cleared_arguments
        )
