from typing import Any, Dict, List, Optional, Set, Tuple, Union

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
    """
    Represents a GraphQL argument and allows conversion to an AST structure.
    """

    def __init__(self, argument_name: str, argument_value: Any) -> None:
        self._name = argument_name
        self._value = argument_value

    def to_ast(self) -> ArgumentNode:
        """Converts the argument to an ArgumentNode AST object."""
        return ArgumentNode(
            name=NameNode(value=self._name),
            value=VariableNode(name=NameNode(value=self._value)),
        )


class GraphQLField:
    """
    Represents a GraphQL field with its name, arguments, subfields, alias,
    and inline fragments.

    Attributes:
        formatted_variables (Dict[str, Dict[str, Any]]): The formatted arguments
        of the GraphQL field.
    """

    def __init__(
        self, field_name: str, arguments: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> None:
        self._field_name = field_name
        self._variables = arguments or {}
        self.formatted_variables: Dict[str, Dict[str, Any]] = {}
        self._subfields: List[GraphQLField] = []
        self._alias: Optional[str] = None
        self._inline_fragments: Dict[str, Tuple[GraphQLField, ...]] = {}

    def alias(self, alias: str) -> "GraphQLField":
        """Sets an alias for the GraphQL field and returns the instance."""
        self._alias = alias
        return self

    def _build_field_name(self) -> str:
        """Builds the field name, including the alias if present."""
        return f"{self._alias}: {self._field_name}" if self._alias else self._field_name

    def _build_selections(
        self, idx: int, used_names: Set[str]
    ) -> List[Union[FieldNode, InlineFragmentNode]]:
        """Builds the selection set for the current GraphQL field,
        including subfields and inline fragments."""
        # Create selections from subfields
        selections: List[Union[FieldNode, InlineFragmentNode]] = [
            subfield.to_ast(idx, used_names) for subfield in self._subfields
        ]

        # Add inline fragments
        for name, subfields in self._inline_fragments.items():
            selections.append(
                InlineFragmentNode(
                    type_condition=NamedTypeNode(name=NameNode(value=name)),
                    selection_set=SelectionSetNode(
                        selections=[
                            subfield.to_ast(idx, used_names) for subfield in subfields
                        ]
                    ),
                )
            )

        return selections

    def _format_variable_name(
        self, idx: int, var_name: str, used_names: Set[str]
    ) -> str:
        """Generates a unique variable name by appending an index and,
        if necessary, an additional counter to avoid duplicates."""
        base_name = f"{var_name}_{idx}"
        unique_name = base_name
        counter = 1

        # Ensure the generated name is unique
        while unique_name in used_names:
            unique_name = f"{base_name}_{counter}"
            counter += 1

        # Add the unique name to the set of used names
        used_names.add(unique_name)

        return unique_name

    def _collect_all_variables(self, idx: int, used_names: Set[str]) -> None:
        """
        Collects and formats all variables for the current GraphQL field,
        ensuring unique names.
        """
        self.formatted_variables = {}

        for k, v in self._variables.items():
            unique_name = self._format_variable_name(idx, k, used_names)
            self.formatted_variables[unique_name] = {
                "name": k,
                "type": v["type"],
                "value": v["value"],
            }

    def to_ast(self, idx: int, used_names: Optional[Set[str]] = None) -> FieldNode:
        """Converts the current GraphQL field to an AST (Abstract Syntax Tree) node."""
        if used_names is None:
            used_names = set()

        self._collect_all_variables(idx, used_names)

        return FieldNode(
            name=NameNode(value=self._build_field_name()),
            arguments=[
                GraphQLArgument(v["name"], k).to_ast()
                for k, v in self.formatted_variables.items()
            ],
            selection_set=(
                SelectionSetNode(selections=self._build_selections(idx, used_names))
                if self._subfields or self._inline_fragments
                else None
            ),
        )

    def get_formatted_variables(self) -> Dict[str, Dict[str, Any]]:
        """
        Retrieves all formatted variables for the current GraphQL field,
        including those from subfields and inline fragments.
        """
        formatted_variables = self.formatted_variables.copy()

        # Collect variables from subfields
        for subfield in self._subfields:
            subfield.get_formatted_variables()
            formatted_variables.update(subfield.formatted_variables)

        # Collect variables from inline fragments
        for subfields in self._inline_fragments.values():
            for subfield in subfields:
                subfield.get_formatted_variables()
                formatted_variables.update(subfield.formatted_variables)
        return formatted_variables
