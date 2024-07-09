from typing import Any, Dict, List, Optional, Tuple, Union

from graphql import (
    ArgumentNode,
    FieldNode,
    InlineFragmentNode,
    NamedTypeNode,
    NameNode,
    SelectionSetNode,
    VariableNode,
)


class GraphQLArgument:
    def __init__(self, argument_name: str):
        self._name = argument_name
        self._variable_name = argument_name

    def to_ast(self, idx: int) -> ArgumentNode:
        return ArgumentNode(
            name=NameNode(value=self._name),
            value=VariableNode(name=NameNode(value=f"{idx}_{self._variable_name}")),
        )


class GraphQLField:
    def __init__(
        self, field_name: str, arguments: Optional[Dict[str, Any]] = None
    ) -> None:
        self._field_name = field_name
        self._variables = arguments or {}
        self._arguments = [GraphQLArgument(k) for k in self._variables]
        self._subfields: List[GraphQLField] = []
        self._alias: Optional[str] = None
        self._inline_fragments: Dict[str, Tuple[GraphQLField, ...]] = {}

    def get_variables_types(self, idx: int) -> Dict[str, Any]:
        return {f"{idx}_{k}": v["type"] for k, v in self._variables.items()}

    def get_processed_variables(self, idx: int) -> Dict[str, Any]:
        return {f"{idx}_{k}": v["value"] for k, v in self._variables.items()}

    def alias(self, alias: str) -> "GraphQLField":
        self._alias = alias
        return self

    def add_subfield(self, subfield: "GraphQLField") -> None:
        self._subfields.append(subfield)

    def add_inline_fragment(self, type_name: str, *subfields: "GraphQLField") -> None:
        self._inline_fragments[type_name] = subfields

    def _build_field_name(self) -> str:
        return f"{self._alias}: {self._field_name}" if self._alias else self._field_name

    def _build_selections(self, idx: int) -> List[Union[FieldNode, InlineFragmentNode]]:
        selections: List[Union[FieldNode, InlineFragmentNode]] = [
            subfield.to_ast(idx) for subfield in self._subfields
        ]
        for name, subfields in self._inline_fragments.items():
            selections.append(
                InlineFragmentNode(
                    type_condition=NamedTypeNode(name=NameNode(value=name)),
                    selection_set=SelectionSetNode(
                        selections=[subfield.to_ast(idx) for subfield in subfields]
                    ),
                )
            )
        return selections

    def to_ast(self, idx: int) -> FieldNode:
        return FieldNode(
            name=NameNode(value=self._build_field_name()),
            arguments=[arg.to_ast(idx) for arg in self._arguments],
            selection_set=(
                SelectionSetNode(selections=self._build_selections(idx))
                if self._subfields or self._inline_fragments
                else None
            ),
        )
