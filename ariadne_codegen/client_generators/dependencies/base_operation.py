from typing import Any, Dict, List, Optional, Tuple, Union

from graphql import (
    ArgumentNode,
    BooleanValueNode,
    FieldNode,
    FloatValueNode,
    InlineFragmentNode,
    IntValueNode,
    NamedTypeNode,
    NameNode,
    ObjectFieldNode,
    ObjectValueNode,
    SelectionSetNode,
    StringValueNode,
)

from .base_model import BaseModel


class GraphQLArgument:
    def __init__(self, argument_name: str, value: Any):
        self._name = argument_name
        self._value = self._convert_value(value)

    def _convert_value(
        self, value: Any
    ) -> Union[
        StringValueNode, IntValueNode, FloatValueNode, BooleanValueNode, ObjectValueNode
    ]:
        if isinstance(value, str):
            return StringValueNode(value=value)
        if isinstance(value, int):
            return IntValueNode(value=str(value))
        if isinstance(value, float):
            return FloatValueNode(value=str(value))
        if isinstance(value, bool):
            return BooleanValueNode(value=value)
        if isinstance(value, BaseModel):
            fields = [
                ObjectFieldNode(name=NameNode(value=k), value=self._convert_value(v))
                for k, v in value.model_dump().items()
            ]
            return ObjectValueNode(fields=fields)
        raise TypeError(f"Unsupported argument type: {type(value)}")

    def to_ast(self) -> ArgumentNode:
        return ArgumentNode(name=NameNode(value=self._name), value=self._value)


class GraphQLField:
    def __init__(self, field_name: str, **kwargs: Any) -> None:
        self._field_name: str = field_name
        self._arguments: List[GraphQLArgument] = [
            GraphQLArgument(k, v) for k, v in kwargs.items() if v
        ]
        self._subfields: List["GraphQLField"] = []
        self._alias: Optional[str] = None
        self._inline_fragments: Dict[str, Tuple["GraphQLField", ...]] = {}

    def alias(self, alias: str) -> "GraphQLField":
        self._alias = alias
        return self

    def _build_field_name(self) -> str:
        if self._alias:
            return f"{self._alias}: {self._field_name}"
        return self._field_name

    def to_ast(self) -> FieldNode:
        selections: List[Union[FieldNode, InlineFragmentNode]] = [
            sub_field.to_ast() for sub_field in self._subfields
        ]
        if self._inline_fragments:
            selections.extend(
                [
                    InlineFragmentNode(
                        type_condition=NamedTypeNode(name=NameNode(value=name)),
                        selection_set=SelectionSetNode(
                            selections=[sub_field.to_ast() for sub_field in subfields]
                        ),
                    )
                    for name, subfields in self._inline_fragments.items()
                ]
            )
        return FieldNode(
            name=NameNode(value=self._build_field_name()),
            arguments=[arg.to_ast() for arg in self._arguments],
            selection_set=(
                SelectionSetNode(selections=selections) if selections else None
            ),
        )
