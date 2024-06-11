import ast
from typing import List, cast

from graphql import (
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLUnionType,
)

from ariadne_codegen.client_generators.utils import get_final_type

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
from .constants import BASE_OPERATION_FILE_PATH, OPERATION_TYPES


class CustomFieldsTypingGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
    ) -> None:
        self.schema = schema
        self.graphql_field_import = ast.ImportFrom(
            module=BASE_OPERATION_FILE_PATH.stem,
            names=[ast.alias("GraphQLField")],
            level=1,
        )
        self._public_names: List[str] = []
        self._class_defs: List[ast.ClassDef] = [
            self._generate_field_class(d) for d in self._filter_types()
        ]

    def generate(self) -> ast.Module:
        return generate_module(
            body=(
                cast(List[ast.stmt], [self.graphql_field_import])
                + cast(List[ast.stmt], [self._class_defs])
            )
        )

    def _filter_types(self):
        return [
            get_final_type(definition)
            for name, definition in self.schema.type_map.items()
            if isinstance(
                definition, (GraphQLObjectType, GraphQLInterfaceType, GraphQLUnionType)
            )
            and not name.startswith("__")
            and name not in OPERATION_TYPES
        ]

    def _generate_field_class(self, class_def: ast.ClassDef) -> ast.ClassDef:
        class_name = f"{class_def.name}GraphQLField"
        class_body: List[ast.stmt] = []
        if isinstance(class_def, GraphQLUnionType):
            class_name = f"{class_def.name}Union"
            class_body.append(self._generate_on_method(class_name))
        if class_name not in self._public_names:
            self._public_names.append(class_name)
        field_class_def = generate_class_def(
            name=class_name,
            base_names=["GraphQLField"],
            body=class_body if class_body else cast(List[ast.stmt], [ast.Pass()]),
        )
        return field_class_def

    def _generate_on_method(self, class_name: str) -> ast.FunctionDef:
        return generate_method_definition(
            "on",
            arguments=generate_arguments(
                [
                    generate_arg(name="self"),
                    generate_arg(name="type_name", annotation=generate_name("str")),
                    generate_arg(
                        name="*subfields", annotation=generate_name("GraphQLField")
                    ),
                ]
            ),
            body=[
                cast(
                    ast.stmt,
                    ast.Assign(
                        targets=[
                            generate_subscript(
                                value=generate_attribute(
                                    value=generate_name("self"),
                                    attr="_inline_fragments",
                                ),
                                slice_=generate_name("type_name"),
                            )
                        ],
                        value=generate_name("subfields"),
                        lineno=1,
                    ),
                ),
                generate_return(value=generate_name("self")),
            ],
            return_type=generate_name(f'"{class_name}"'),
        )

    def get_generated_public_names(self) -> List[str]:
        return self._public_names
