import ast
from typing import List, cast

from graphql import (
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLUnionType,
)

from ariadne_codegen.client_generators.custom_generator_utils import get_final_type

from ..codegen import (
    generate_arg,
    generate_arguments,
    generate_attribute,
    generate_class_def,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
    generate_subscript,
)
from .constants import (
    BASE_OPERATION_FILE_PATH,
    GRAPHQL_BASE_FIELD_CLASS,
    OPERATION_TYPES,
)


class CustomFieldsTypingGenerator:
    def __init__(self, schema: GraphQLSchema) -> None:
        self.schema = schema
        self.graphql_field_import = ast.ImportFrom(
            module=BASE_OPERATION_FILE_PATH.stem,
            names=[ast.alias(GRAPHQL_BASE_FIELD_CLASS)],
            level=1,
        )
        self._public_names: List[str] = []
        self._class_defs: List[ast.ClassDef] = [
            self._generate_field_class(d) for d in self._filter_types()
        ]

    def generate(self) -> ast.Module:
        """
        Generates an AST module containing the custom fields and required imports.
        """
        return generate_module(
            body=cast(List[ast.stmt], [self.graphql_field_import])
            + cast(List[ast.stmt], self._class_defs)
        )

    def _filter_types(self) -> List[ast.ClassDef]:
        """
        Filters GraphQL types to include only objects, interfaces, and unions,
        excluding internal and operation types.
        """
        return [
            get_final_type(definition)
            for name, definition in self.schema.type_map.items()
            if isinstance(
                definition, (GraphQLObjectType, GraphQLInterfaceType, GraphQLUnionType)
            )
            and not name.startswith("__")
            and name not in OPERATION_TYPES
        ]

    def _generate_field_class(
        self,
        graphql_type: ast.ClassDef,
    ) -> ast.ClassDef:
        """
        Generates a field class for the given GraphQL type.
        """
        class_name = f"{graphql_type.name}{GRAPHQL_BASE_FIELD_CLASS}"
        class_body: List[ast.stmt] = []

        if isinstance(graphql_type, GraphQLUnionType):
            class_name = f"{graphql_type.name}Union"
            class_body.append(self._generate_on_method(class_name))
        class_body.append(self._generate_alias_method(class_name))
        if class_name not in self._public_names:
            self._public_names.append(class_name)

        field_class_def = generate_class_def(
            name=class_name,
            base_names=[GRAPHQL_BASE_FIELD_CLASS],
            body=class_body if class_body else cast(List[ast.stmt], [ast.Pass()]),
        )
        return field_class_def

    def _generate_on_method(self, class_name: str) -> ast.FunctionDef:
        """
        Generates the `on` method for a class.
        """
        return generate_method_definition(
            "on",
            arguments=generate_arguments(
                [
                    generate_arg(name="self"),
                    generate_arg(name="type_name", annotation=generate_name("str")),
                    generate_arg(
                        name="*subfields",
                        annotation=generate_name(GRAPHQL_BASE_FIELD_CLASS),
                    ),
                ]
            ),
            body=[
                ast.Assign(
                    targets=[
                        generate_subscript(
                            value=generate_attribute(
                                value=generate_name("self"), attr="_inline_fragments"
                            ),
                            slice_=generate_name("type_name"),
                        )
                    ],
                    value=generate_name("subfields"),
                    lineno=1,
                ),
                generate_return(value=generate_name("self")),
            ],
            return_type=generate_name(f'"{class_name}"'),
        )

    def _generate_alias_method(self, class_name: str) -> ast.FunctionDef:
        """
        Generates the `alias` method for a class.
        """
        return generate_method_definition(
            "alias",
            arguments=generate_arguments(
                [
                    generate_arg(name="self"),
                    generate_arg(name="alias", annotation=generate_name("str")),
                ]
            ),
            body=[
                ast.Assign(
                    targets=[
                        generate_attribute(value=generate_name("self"), attr="_alias"),
                    ],
                    value=generate_name("alias"),
                    lineno=1,
                ),
                generate_return(value=generate_name("self")),
            ],
            return_type=generate_name(f'"{class_name}"'),
        )

    def get_generated_public_names(self) -> List[str]:
        """
        Returns the list of generated public names.
        """
        return self._public_names
