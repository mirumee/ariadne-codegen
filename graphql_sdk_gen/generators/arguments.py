import ast
from typing import Union

from graphql import (
    ListTypeNode,
    NamedTypeNode,
    NonNullTypeNode,
    TypeNode,
    VariableDefinitionNode,
)

from ..exceptions import ParsingError
from .codegen import (
    generate_annotation_name,
    generate_arg,
    generate_arguments,
    generate_list_annotation,
)
from .constants import SIMPLE_TYPE_MAP


class ArgumentsGenerator:
    def __init__(self) -> None:
        self.used_types: list[str] = []

    def _parse_type_node(
        self,
        node: Union[NamedTypeNode, ListTypeNode, NonNullTypeNode, TypeNode],
        nullable: bool = True,
    ) -> Union[ast.Name, ast.Subscript]:
        if isinstance(node, NamedTypeNode):
            return self._parse_named_type_node(node, nullable)
        if isinstance(node, ListTypeNode):
            return generate_list_annotation(
                self._parse_type_node(node.type, nullable), nullable
            )
        if isinstance(node, NonNullTypeNode):
            return self._parse_type_node(node.type, False)

        raise ParsingError("Invalid argument type.")

    def _parse_named_type_node(
        self, node: NamedTypeNode, nullable: bool = True
    ) -> Union[ast.Name, ast.Subscript]:
        name = node.name.value

        if name in SIMPLE_TYPE_MAP:
            name = SIMPLE_TYPE_MAP[name]
        else:
            self.used_types.append(name)

        return generate_annotation_name(name, nullable)

    def generate(
        self, variable_definitions: tuple[VariableDefinitionNode, ...]
    ) -> ast.arguments:
        """Generate arguments from given variable definitions."""
        arguments = generate_arguments([generate_arg("self")])
        for variable_definition in variable_definitions:
            name = variable_definition.variable.name.value
            annotation = self._parse_type_node(variable_definition.type)
            arguments.args.append(generate_arg(name, annotation))
        return arguments
