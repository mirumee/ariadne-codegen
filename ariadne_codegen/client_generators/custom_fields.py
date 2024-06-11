import ast
from typing import Dict, List, Optional, Set, Union, cast

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
)

from ariadne_codegen.exceptions import ParsingError

from ..codegen import (
    generate_ann_assign,
    generate_annotation_name,
    generate_arg,
    generate_arguments,
    generate_attribute,
    generate_call,
    generate_class_def,
    generate_constant,
    generate_expr,
    generate_import_from,
    generate_keyword,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
    generate_subscript,
    generate_union_annotation,
)
from ..utils import process_name
from .constants import (
    ANY,
    BASE_MODEL_FILE_PATH,
    BASE_OPERATION_FILE_PATH,
    INPUT_SCALARS_MAP,
    OPTIONAL,
    TYPING_MODULE,
    UNION,
    UPLOAD_CLASS_NAME,
)
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
                + cast(
                    List[ast.stmt],
                    self._class_defs,
                )
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
            if isinstance(graphql_type, GraphQLInterfaceType):
                class_def = self._generate_class_def_body(
                    definition=graphql_type,
                    class_name=f"{graphql_type.name}Interface",
                )
                class_def.body.append(
                    self._generate_on_method(f"{graphql_type.name}Interface")
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
                field_name = f"{final_type.name}Fields"
                class_def.body.append(
                    self.generate_product_type_method(
                        name, field_name, getattr(field, "args")
                    )
                )
                additional_fields_typing.add(field_name)
            elif isinstance(final_type, GraphQLInterfaceType):
                field_name = f"{final_type.name}Interface"
                class_def.body.append(
                    self.generate_product_type_method(
                        name, field_name, getattr(field, "args")
                    )
                )
                additional_fields_typing.add(field_name)
            else:
                field_name = f"{definition.name}GraphQLField"

                if isinstance(final_type, GraphQLUnionType):
                    field_name = f"{final_type.name}Union"
                    additional_fields_typing.add(field_name)
                if getattr(field, "args"):
                    class_def.body.append(
                        self.generate_product_type_method(
                            name, field_name, getattr(field, "args")
                        )
                    )
                else:
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

    def generate_product_type_method(
        self, name, class_name, arguments=None
    ) -> ast.FunctionDef:
        arguments = arguments or {}
        return_keywords = []
        field_class_name = generate_name(class_name)
        field_kwonlyargs = []
        field_kw_defaults: List[Union[ast.expr, None]] = []
        for arg_name, argument in arguments.items():
            argument_final_type = get_final_type(argument.type)
            field_kwonlyargs.append(
                generate_arg(
                    name=arg_name,
                    annotation=self._parse_graphql_type_name(argument_final_type),
                )
            )
            field_kw_defaults.append(generate_constant(value=None))
            return_keywords.append(
                generate_keyword(arg=arg_name, value=generate_name(arg_name))
            )
        return generate_method_definition(
            name,
            arguments=generate_arguments(
                args=[generate_arg(name="cls")],
                kwonlyargs=field_kwonlyargs,
                kw_defaults=field_kw_defaults,
            ),
            body=[
                generate_return(
                    value=generate_call(
                        func=field_class_name,
                        args=[generate_constant(name)],
                        keywords=return_keywords,
                    )
                ),
            ],
            return_type=generate_name(f'"{class_name}"'),
            decorator_list=[generate_name("classmethod")],
        )

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

    def _parse_graphql_type_name(
        self, type_, nullable: bool = True
    ) -> Union[ast.Name, ast.Subscript]:
        name = type_.name

        if isinstance(type_, GraphQLInputObjectType):
            self._add_import(
                generate_import_from(names=[name], from_="input_types", level=1)
            )
        elif isinstance(type_, GraphQLEnumType):
            self._add_import(generate_import_from(names=[name], level=1))
        elif isinstance(type_, GraphQLScalarType):
            if name not in self.custom_scalars:
                name = INPUT_SCALARS_MAP.get(name, ANY)
                if name == UPLOAD_CLASS_NAME:
                    self._add_import(
                        generate_import_from(
                            names=[UPLOAD_CLASS_NAME],
                            from_=BASE_MODEL_FILE_PATH.stem,
                            level=1,
                        )
                    )
            else:
                name = self.custom_scalars[name].type_name
        else:
            raise ParsingError(f"Incorrect argument type {name}")

        return generate_annotation_name(name, nullable)
