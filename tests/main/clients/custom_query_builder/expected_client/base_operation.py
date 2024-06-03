from typing import Any, Dict, List, Optional, Type


def format_value(value: Any) -> str:
    return f'"{value}"' if isinstance(value, str) else str(value)


class GraphQLField:
    def __init__(self, name: str) -> None:
        self._name = name
        self._subfields: List["GraphQLField"] = []
        self._arguments: Dict[str, Any] = {}

    def __str__(self) -> str:
        subfields_str = self._format_subfields()
        args_str = self._format_arguments()
        return f"{self._name}{args_str} {subfields_str}".strip()

    def _format_subfields(self) -> str:
        if not self._subfields:
            return ""
        subfields_str = " ".join(str(subfield) for subfield in self._subfields)
        return f"{{ {subfields_str} }}"

    def _format_arguments(self) -> str:
        if not self._arguments:
            return ""
        args_str = ", ".join(
            f"{key}: {format_value(value)}" for key, value in self._arguments.items()
        )
        return f"({args_str})"

    def add_fields(self, *subfields: "GraphQLField") -> "GraphQLField":
        self._subfields.extend(subfields)
        return self

    def set_arguments(self, **kwargs: Any) -> "GraphQLField":
        self._arguments.update(kwargs)
        return self


class BaseGraphQLOperation:
    def __init__(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.arguments = arguments if arguments else {}
        self._fields: List[GraphQLField] = []
        self.inline_fragments: Dict[Any, List[str]] = {}
        self._alias: Optional[str] = None

    def __str__(self) -> str:
        fields_str = self._format_fields()
        args_str = self._format_arguments()
        query = f"{self.name}{args_str} {{ {fields_str} }}"
        return f"{self._alias}: {query}" if self._alias else query

    def _format_fields(self) -> str:
        return " ".join(str(field) for field in self._fields)

    def _format_arguments(self) -> str:
        if not self.arguments:
            return ""
        args_str = ", ".join(
            f"{key}: {format_value(value)}" for key, value in self.arguments.items()
        )
        return f"({args_str})"

    def alias(self, alias: str) -> "BaseGraphQLOperation":
        self._alias = alias
        return self

    def fields(self, *args: GraphQLField) -> "BaseGraphQLOperation":
        self._fields.extend(args)
        return self

    def on(self, on_class: Type[Any], *args: GraphQLField) -> "BaseGraphQLOperation":
        self.inline_fragments[on_class] = [str(arg) for arg in args]
        return self
