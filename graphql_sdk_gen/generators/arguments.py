import ast
from typing import Union

from graphql import (
    ListTypeNode,
    NamedTypeNode,
    NonNullTypeNode,
    TypeNode,
    VariableDefinitionNode,
)

from ..exceptions import NotSupported
from .constants import LIST, OPTIONAL, SIMPLE_TYPE_MAP


class ArgumentsGenerator:
    def __init__(self) -> None:
        self.non_scalar_types: list = []

    def _parse_named_type_node(
        self, node: NamedTypeNode, nullable: bool = True
    ) -> Union[ast.Name, ast.Subscript]:
        name = node.name.value
        if name in SIMPLE_TYPE_MAP:
            name = SIMPLE_TYPE_MAP[name]
        else:
            self.non_scalar_types.append(name)
        result = ast.Name(id=name)
        if nullable:
            return self._nullable(result)
        return result

    def _parse_not_null_type_node(
        self, node: NonNullTypeNode, _
    ) -> Union[ast.Name, ast.Subscript, None]:
        return self._parse_type_node(node.type, False)

    def _parse_list_type_node(
        self, node: ListTypeNode, nullable: bool = True
    ) -> ast.Subscript:
        result = ast.Subscript(
            value=ast.Name(id=LIST), slice=self._parse_type_node(node.type, nullable)
        )
        if nullable:
            return self._nullable(result)
        return result

    def _nullable(self, slice_: Union[ast.Name, ast.Subscript]) -> ast.Subscript:
        return ast.Subscript(value=ast.Name(id=OPTIONAL), slice=slice_)

    def _parse_type_node(
        self,
        node: Union[NamedTypeNode, ListTypeNode, NonNullTypeNode, TypeNode],
        nullable: bool = True,
    ) -> Union[None, ast.Name, ast.Subscript]:
        mapping = {
            NamedTypeNode: self._parse_named_type_node,
            ListTypeNode: self._parse_list_type_node,
            NonNullTypeNode: self._parse_not_null_type_node,
            TypeNode: lambda node: None,
        }
        return mapping[type(node)](node, nullable)

    def generate(
        self, variable_definitions: tuple[VariableDefinitionNode]
    ) -> ast.arguments:
        arguments = ast.arguments(
            posonlyargs=[],
            args=[
                ast.arg(arg="self"),
            ],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        )
        for variable_definition in variable_definitions:
            name = variable_definition.variable.name.value
            annotation = self._parse_type_node(variable_definition.type)
            arguments.args.append(ast.arg(arg=name, annotation=annotation))
            if variable_definition.default_value:
                raise NotSupported("Default values for query params are not supported.")

        return arguments
