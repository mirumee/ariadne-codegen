import ast
from typing import Dict, List, Optional, Set, Union, cast

from graphql import (
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLUnionType,
)

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
    generate_union_annotation,
)
from ..utils import process_name
from .constants import BASE_OPERATION_FILE_PATH, OPTIONAL, TYPING_MODULE, UNION
from .utils import TypeCollector, get_final_type


class CustomFieldsGenerator:
    def __init__(
        self,
        schema: GraphQLSchema,
        convert_to_snake_case: bool = True,
        custom_scalars=None,
    ) -> None:
        self.schema = schema
        self.convert_to_snake_case = convert_to_snake_case
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self._visited_types: Set[str] = set()
        self._field_classes: Set[str] = set()
        self._generated_modules: Dict[str, ast.Module] = {}
        self._imports: List[ast.ImportFrom] = [
            ast.ImportFrom(
                module=BASE_OPERATION_FILE_PATH.stem,
                names=[ast.alias("GraphQLField")],
                level=1,
            )
        ]
        self._add_import(generate_import_from([OPTIONAL, UNION], TYPING_MODULE))

        self._class_defs: List[ast.ClassDef] = self._parse_object_type_definitions(
            TypeCollector(self.schema).collect()
        )

    def _add_import(self, import_: Optional[ast.ImportFrom] = None):
        if not import_:
            return

        if import_.names:
            self._imports.append(import_)

    def generate(self) -> ast.Module:
        module = generate_module(
            body=(
                cast(List[ast.stmt], self._imports)
                + cast(List[ast.stmt], self._class_defs)
            ),
        )

        return module

    def _parse_object_type_definitions(self, class_definitions):
        class_defs = []
        interface_defs = []
        for type_name in class_definitions:
            graphql_type = self.schema.get_type(type_name)
            if isinstance(graphql_type, GraphQLObjectType):
                class_def = self._generate_class_def_body(
                    definition=graphql_type,
                    class_name=f"{graphql_type.name}Fields",
                )
                class_defs.append(class_def)

        return [*interface_defs, *class_defs]

    def _generate_class_def_body(
        self,
        definition: Union[GraphQLObjectType, GraphQLInterfaceType],
        class_name: str,
    ) -> ast.ClassDef:
        base_names = ["GraphQLField"]
        additional_fields_typing = set()
        definition_fields: Dict[str, ast.ClassDef] = dict(definition.fields.items())
        for interface in definition.interfaces:
            definition_fields.update(dict(interface.fields.items()))
        class_def = generate_class_def(name=class_name, base_names=base_names)

        for lineno, (org_name, field) in enumerate(definition_fields.items(), start=1):
            name = process_name(
                org_name,
                convert_to_snake_case=self.convert_to_snake_case,
            )
            final_type = get_final_type(field)
            if isinstance(final_type, GraphQLObjectType):
                class_def.body.append(
                    self.generate_product_type_method(name, f"{final_type.name}Fields")
                )
                additional_fields_typing.add(f"{final_type.name}Fields")
            else:
                field_name = f"{definition.name}GraphQLField"
                if isinstance(final_type, GraphQLInterfaceType):
                    field_name = f"{final_type.name}Interface"
                    additional_fields_typing.add(field_name)
                if isinstance(final_type, GraphQLUnionType):
                    field_name = f"{final_type.name}Union"
                    additional_fields_typing.add(field_name)
                self._add_import(generate_import_from([field_name], level=1))
                field_class_name = generate_name(field_name)

                field_implementation = generate_ann_assign(
                    target=name,
                    annotation=field_class_name,
                    value=generate_call(
                        func=field_class_name,
                        args=[generate_constant(org_name)],
                    ),
                    lineno=lineno,
                )

                class_def.body.append(field_implementation)

        class_def.body.append(
            self._generate_fields_method(
                class_name, definition.name, sorted(additional_fields_typing)
            )
        )

        return class_def

    def _generate_fields_method(
        self, class_name: str, definition_name: str, additional_fields_typing: List
    ) -> ast.FunctionDef:
        field_class_name = generate_name(f"{definition_name}GraphQLField")
        self._add_import(
            generate_import_from([f"{definition_name}GraphQLField"], level=1)
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
                    value=generate_call(
                        func=generate_attribute(
                            value=generate_name("self"),
                            attr="_subfields.extend",
                        ),
                        args=[generate_name("subfields")],
                    )
                ),
                generate_return(value=generate_name("self")),
            ],
            return_type=generate_name(f'"{class_name}"'),
        )

    def generate_product_type_method(self, name, class_name) -> ast.FunctionDef:
        field_class_name = generate_name(class_name)
        return generate_method_definition(
            name,
            arguments=generate_arguments(
                [
                    generate_arg(name="cls"),
                ]
            ),
            body=[
                generate_return(
                    value=generate_call(
                        func=field_class_name,
                        args=[generate_constant(name)],
                    )
                ),
            ],
            return_type=generate_name(f'"{class_name}"'),
            decorator_list=[generate_name("classmethod")],
        )
