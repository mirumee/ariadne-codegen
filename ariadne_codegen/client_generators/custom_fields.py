import ast
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from graphql import (
    GraphQLInterfaceType,
    GraphQLNamedType,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLUnionType,
)

from ariadne_codegen.client_generators.custom_arguments import ArgumentGenerator

from ..codegen import (
    generate_ann_assign,
    generate_arg,
    generate_arguments,
    generate_attribute,
    generate_call,
    generate_class_def,
    generate_constant,
    generate_expr,
    generate_import_from,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
    generate_subscript,
    generate_union_annotation,
)
from ..plugins.manager import PluginManager
from ..utils import process_name
from .constants import (
    ANY,
    BASE_GRAPHQL_FIELD_CLASS_NAME,
    BASE_OPERATION_FILE_PATH,
    DICT,
    GRAPHQL_BASE_FIELD_CLASS,
    GRAPHQL_INTERFACE_SUFFIX,
    GRAPHQL_OBJECT_SUFFIX,
    GRAPHQL_UNION_SUFFIX,
    OPTIONAL,
    TYPING_MODULE,
    UNION,
)
from .custom_generator_utils import TypeCollector, get_final_type
from .scalars import ScalarData


class CustomFieldsGenerator:
    """Generates custom fields for a given GraphQL schema using Python's AST module."""

    def __init__(
        self,
        schema: GraphQLSchema,
        convert_to_snake_case: bool = True,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.schema = schema
        self.convert_to_snake_case = convert_to_snake_case
        self.plugin_manager = plugin_manager
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self._imports: List[ast.ImportFrom] = [
            ast.ImportFrom(
                module=BASE_OPERATION_FILE_PATH.stem,
                names=[ast.alias(BASE_GRAPHQL_FIELD_CLASS_NAME)],
                level=1,
            )
        ]
        self._add_import(
            generate_import_from(
                [OPTIONAL, UNION, ANY, DICT],
                TYPING_MODULE,
            )
        )
        self.argument_generator = ArgumentGenerator(
            self.custom_scalars,
            self.convert_to_snake_case,
            self.plugin_manager,
        )
        self._class_defs: List[ast.ClassDef] = self._parse_object_type_definitions(
            TypeCollector(self.schema).collect()
        )

    def generate(self) -> ast.Module:
        """Generates an AST module containing the custom fields and required imports."""
        self.argument_generator.add_custom_scalar_imports()
        module = generate_module(
            body=cast(List[ast.stmt], self._imports + self._class_defs),
        )
        return module

    def _add_import(self, import_: Optional[ast.ImportFrom] = None) -> None:
        """Adds an import statement to the list of imports."""
        if import_:
            if self.plugin_manager:
                import_ = self.plugin_manager.generate_client_import(import_)
            if import_.names:
                self._imports.append(import_)

    def _parse_object_type_definitions(
        self, type_names: List[str]
    ) -> List[ast.ClassDef]:
        """
        Parses object type definitions from the schema
        and generates AST class definitions.
        """
        class_defs = []

        for type_name in type_names:
            graphql_type = self.schema.get_type(type_name)
            if isinstance(graphql_type, (GraphQLObjectType, GraphQLInterfaceType)):
                class_def = self._generate_class_def_body(
                    definition=graphql_type,
                    class_name=f"{graphql_type.name}{self._get_suffix(graphql_type)}",
                )
                if isinstance(graphql_type, GraphQLInterfaceType):
                    class_def.body.append(
                        self._generate_on_method(
                            f"{graphql_type.name}{GRAPHQL_INTERFACE_SUFFIX}"
                        )
                    )
                class_defs.append(class_def)

        return class_defs

    def _generate_class_def_body(
        self,
        definition: Union[GraphQLObjectType, GraphQLInterfaceType],
        class_name: str,
    ) -> ast.ClassDef:
        """
        Generates the body of a class definition for a given GraphQL object
        or interface type.
        """
        base_names = [GRAPHQL_BASE_FIELD_CLASS]
        additional_fields_typing = set()
        class_def = generate_class_def(name=class_name, base_names=base_names)
        for lineno, (org_name, field) in enumerate(
            self._get_combined_fields(definition).items(), start=1
        ):
            name = process_name(
                org_name, convert_to_snake_case=self.convert_to_snake_case
            )
            final_type = get_final_type(field)
            field_name, method_required = self._get_field_name(
                final_type, definition.name
            )
            if self._is_custom_type(final_type):
                additional_fields_typing.add(field_name)
            class_def.body.append(
                self._generate_class_field(
                    name, field_name, org_name, field, method_required, lineno
                )
            )

        class_def.body.append(
            self._generate_fields_method(
                class_name, definition.name, sorted(additional_fields_typing)
            )
        )
        class_def.body.append(self._generate_alias_method(class_name))
        return class_def

    def _get_combined_fields(
        self, definition: Union[GraphQLObjectType, GraphQLInterfaceType]
    ) -> Dict[str, ast.ClassDef]:
        """Combines fields from the definition and its interfaces."""
        fields = dict(definition.fields.items())
        for interface in getattr(definition, "interfaces", []):
            fields.update(dict(interface.fields.items()))
        return fields

    def _get_field_name(
        self, final_type: GraphQLNamedType, definition_name: str
    ) -> Tuple[str, bool]:
        """
        Returns the appropriate field name suffix based on the type of GraphQL type.
        """
        if isinstance(final_type, GraphQLObjectType):
            return f"{final_type.name}{GRAPHQL_OBJECT_SUFFIX}", True
        if isinstance(final_type, GraphQLInterfaceType):
            return f"{final_type.name}{GRAPHQL_INTERFACE_SUFFIX}", True
        if isinstance(final_type, GraphQLUnionType):
            field_name = f"{final_type.name}{GRAPHQL_UNION_SUFFIX}"
        else:
            field_name = f"{definition_name}{GRAPHQL_BASE_FIELD_CLASS}"
        self._add_import(
            generate_import_from(
                [field_name],
                from_="custom_typing_fields",
                level=1,
            )
        )
        return field_name, False

    def _is_custom_type(
        self,
        final_type: Union[GraphQLObjectType, GraphQLInterfaceType, GraphQLUnionType],
    ) -> bool:
        """Checks if the final type is a custom type (Object, Interface, or Union)."""
        return isinstance(
            final_type, (GraphQLObjectType, GraphQLInterfaceType, GraphQLUnionType)
        )

    def _generate_class_field(
        self,
        name: str,
        field_name: str,
        org_name: str,
        field: ast.ClassDef,
        method_required: bool,
        lineno: int,
    ) -> ast.stmt:
        """Handles the generation of field types."""
        if getattr(field, "args") or method_required:
            return self.generate_product_type_method(
                name, org_name, field_name, getattr(field, "args")
            )
        return generate_ann_assign(
            target=generate_name(name),
            annotation=generate_name(f'"{field_name}"'),
            value=generate_call(
                func=generate_name(field_name), args=[generate_constant(org_name)]
            ),
            lineno=lineno,
        )

    def _generate_fields_method(
        self, class_name: str, definition_name: str, additional_fields_typing: List[str]
    ) -> ast.FunctionDef:
        """Generates the `fields` method for a class."""
        field_class_name = generate_name(f"{definition_name}{GRAPHQL_BASE_FIELD_CLASS}")
        self._add_import(
            generate_import_from(
                [field_class_name.id], from_="custom_typing_fields", level=1
            )
        )
        fields_annotation: Union[ast.Name, ast.Subscript] = field_class_name
        if additional_fields_typing:
            additional_fields_typing_ann = [
                generate_name(f'"{field_typing}"')
                for field_typing in additional_fields_typing
            ]
            fields_annotation = generate_union_annotation(
                [field_class_name, *additional_fields_typing_ann], nullable=False
            )

        return generate_method_definition(
            "fields",
            arguments=generate_arguments(
                [
                    generate_arg(name="self"),
                    generate_arg(name="*subfields", annotation=fields_annotation),
                ]
            ),
            body=[
                generate_expr(
                    value=generate_constant(
                        value=f"Subfields should come from the {class_name} class"
                    )
                ),
                generate_expr(
                    value=generate_call(
                        func=generate_attribute(
                            value=generate_name("self"), attr="_subfields.extend"
                        ),
                        args=[generate_name("subfields")],
                    )
                ),
                generate_return(value=generate_name("self")),
            ],
            return_type=generate_name(f'"{class_name}"'),
        )

    def _generate_on_method(self, class_name: str) -> ast.FunctionDef:
        """Generates the `on` method for a class."""
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
            body=cast(
                List[ast.stmt],
                [
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
                    generate_return(value=generate_name("self")),
                ],
            ),
            return_type=generate_name(f'"{class_name}"'),
        )

    def generate_product_type_method(
        self, name: str, org_name: str, class_name: str, arguments: Optional[Dict[str, Any]] = None
    ) -> ast.FunctionDef:
        """Generates a method for a product type."""
        arguments = arguments or {}
        field_class_name = generate_name(class_name)
        (
            method_arguments,
            return_arguments_keys,
            return_arguments_values,
        ) = self.argument_generator.generate_arguments(arguments)
        self._imports.extend(self.argument_generator.imports)
        arguments_body: List[ast.stmt] = []
        arguments_keyword: List[ast.keyword] = []

        if arguments:
            (
                arguments_body,
                arguments_keyword,
            ) = self.argument_generator.generate_clear_arguments_section(
                return_arguments_keys, return_arguments_values
            )

        return generate_method_definition(
            name,
            arguments=method_arguments,
            body=cast(
                List[ast.stmt],
                [
                    *arguments_body,
                    generate_return(
                        value=generate_call(
                            func=field_class_name,
                            args=[generate_constant(org_name)],
                            keywords=arguments_keyword,
                        )
                    ),
                ],
            ),
            return_type=generate_name(f'"{class_name}"'),
            decorator_list=[generate_name("classmethod")],
        )

    def _get_suffix(
        self, graphql_type: Union[GraphQLObjectType, GraphQLInterfaceType]
    ) -> str:
        """Gets the appropriate suffix for a GraphQL type."""
        if isinstance(graphql_type, GraphQLObjectType):
            return GRAPHQL_OBJECT_SUFFIX
        if isinstance(graphql_type, GraphQLInterfaceType):
            return GRAPHQL_INTERFACE_SUFFIX
        raise ValueError(f"Unexpected graphql_type: {graphql_type}")

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
