from enum import Enum


class MetadataErrorCode(str, Enum):
    GRAPHQL_ERROR = "GRAPHQL_ERROR"
    INVALID = "INVALID"
    NOT_FOUND = "NOT_FOUND"
    REQUIRED = "REQUIRED"
    NOT_UPDATED = "NOT_UPDATED"
