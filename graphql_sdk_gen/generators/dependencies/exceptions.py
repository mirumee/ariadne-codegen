class GraphQLError(Exception):
    def __init__(
        self,
        message: str,
        locations: list[dict[str, int]] = None,
        path: list[str] = None,
        extensions: dict[str, object] = None,
        orginal: dict[str, object] = None,
    ):
        self.message = message
        self.locations = locations
        self.path = path
        self.extensions = extensions
        self.orginal = orginal

    def __str__(self) -> str:
        return self.message

    @classmethod
    def from_dict(cls, error: dict):
        return cls(
            message=error["message"],
            locations=error.get("locations"),
            path=error.get("path"),
            extensions=error.get("extensions"),
            orginal=error,
        )


class GraphQLMultiError(Exception):
    def __init__(self, errors: list[GraphQLError]):
        self.errors = errors

    def __str__(self) -> str:
        return "; ".join(str(e) for e in self.errors)

    @classmethod
    def from_errors_dicts(cls, errors_dicts: list[dict]):
        return cls(errors=[GraphQLError.from_dict(e) for e in errors_dicts])
