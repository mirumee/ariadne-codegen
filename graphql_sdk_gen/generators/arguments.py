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
    generate_constant,
    generate_dict,
    generate_list_annotation,
    generate_name,
)
from .constants import SIMPLE_TYPE_MAP
from .utils import str_to_snake_case


class ArgumentsGenerator:
    def __init__(self, convert_to_snake_case: bool = True) -> None:
        self.convert_to_snake_case = convert_to_snake_case
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

    def _process_name(self, name: str) -> str:
        if self.convert_to_snake_case:
            return str_to_snake_case(name)
        return name

    def generate(
        self, variable_definitions: tuple[VariableDefinitionNode, ...]
    ) -> tuple[ast.arguments, ast.Dict]:
        """Generate arguments from given variable definitions."""
        arguments = generate_arguments([generate_arg("self")])
        dict_ = generate_dict()
        for variable_definition in variable_definitions:
            org_name = variable_definition.variable.name.value
            name = self._process_name(org_name)
            annotation = self._parse_type_node(variable_definition.type)

            arguments.args.append(generate_arg(name, annotation))
            dict_.keys.append(generate_constant(org_name))
            dict_.values.append(generate_name(name))
        return arguments, dict_
