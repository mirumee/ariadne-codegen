import ast
from typing import Dict, List, Optional, Tuple, Union, cast

from graphql import (
    GraphQLEnumType,
    GraphQLFieldMap,
    GraphQLInputObjectType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLSchema,
    GraphQLUnionType,
)

from ariadne_codegen.exceptions import ParsingError
from ariadne_codegen.utils import str_to_snake_case

from ..codegen import (
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
    generate_union_annotation,
)
from ..plugins.manager import PluginManager
from .constants import (
    ANY,
    CUSTOM_FIELDS_FILE_PATH,
    DICT,
    INPUT_SCALARS_MAP,
    OPTIONAL,
    TYPE_CHECKING,
    TYPING_MODULE,
    UNION,
)
from .scalars import ScalarData
from .utils import get_final_type


class CustomOperationGenerator:
    def __init__(
        self,
        graphql_fields: GraphQLFieldMap,
        base_client_import: ast.ImportFrom,
        name: str,
        base_name: str,
        enums_module_name: str = "enums",
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.graphql_fields = graphql_fields
        self.name = name
        self.base_name = base_name
        self.enums_module_name = enums_module_name
        self.plugin_manager = plugin_manager
        self.custom_scalars = custom_scalars if custom_scalars else {}

        self._imports: List[ast.ImportFrom] = []
        self._type_imports: List[ast.ImportFrom] = []
        self._initialize_imports(base_client_import)

        self._class_def = generate_class_def(name=name, base_names=[])

        self._used_enums: List[str] = []
        self._used_inputs: List[str] = []

    def _initialize_imports(self, base_client_import: ast.ImportFrom):
        self._add_import(base_client_import)
        self._add_import(
            generate_import_from(
                [OPTIONAL, ANY, DICT, TYPE_CHECKING, UNION], TYPING_MODULE
            )
        )

    def generate(self) -> ast.Module:
        """Generate module with class definition of graphql client."""
        custom_operation_classes = [
            self._generate_custom_operation_class(name, field)
            for name, field in self.graphql_fields.items()
            if isinstance(get_final_type(field), GraphQLObjectType)
        ]

        for name, field in self.graphql_fields.items():
            final_type = get_final_type(field)
            if isinstance(final_type, GraphQLObjectType):
                method_def = self._generate_method(name=name, operation_args=field.args)
                method_def.lineno = len(self._class_def.body) + 1
                self._class_def.body.append(method_def)

        if not self._class_def.body:
            self._class_def.body.append(ast.Pass())

        self._class_def.lineno = len(self._imports) + 3
        clean_arguments_def = self._generate_clean_arguments_function()

        module = generate_module(
            body=cast(List[ast.stmt], self._imports)
            + [self._generate_type_checking_import()]
            + custom_operation_classes
            + [clean_arguments_def, self._class_def],
        )
        return module

    def _generate_type_checking_import(self) -> ast.If:
        return ast.If(
            test=generate_name(TYPE_CHECKING),
            body=self._type_imports,
            orelse=[],
        )

    def _generate_custom_operation_class(self, operation, operation_field):
        operation = self._capitalize_first_letter(operation)
        class_def = generate_class_def(
            name=f"{operation}GraphQL{self.name}", base_names=[self.base_name]
        )
        operation_field_final_type = get_final_type(operation_field)
        args_annotation_names = [
            self._get_operation_field_annotation(field, operation_field_final_type)
            for field in operation_field_final_type.fields.values()
        ]

        args_annotation = self._generate_args_annotation(args_annotation_names)
        fields_method = self._generate_fields_method(operation, args_annotation)

        class_def.body.append(fields_method)
        return class_def

    def _get_operation_field_annotation(self, field, operation_field):
        field_type = get_final_type(field)
        if isinstance(field_type, GraphQLObjectType):
            self._type_imports.append(
                generate_import_from(
                    from_=CUSTOM_FIELDS_FILE_PATH.stem,
                    names=[f"{field_type.name}Fields"],
                    level=1,
                )
            )
            return generate_name(f'"{field_type.name}Fields"')
        else:
            self._type_imports.append(
                generate_import_from(
                    from_=CUSTOM_FIELDS_FILE_PATH.stem,
                    names=[f"{operation_field.name}GraphQLField"],
                    level=1,
                )
            )
            return generate_name(f'"{operation_field.name}GraphQLField"')

    def _generate_args_annotation(self, args_annotation_names):
        return (
            generate_union_annotation(args_annotation_names, nullable=False)
            if len(args_annotation_names) > 1
            else args_annotation_names[0]
        )

    def _generate_fields_method(self, operation, args_annotation):
        return generate_method_definition(
            "fields",
            arguments=generate_arguments(
                [
                    generate_arg("self"),
                    generate_arg("*args", annotation=args_annotation),
                ]
            ),
            body=[
                generate_expr(
                    value=generate_call(
                        func=generate_attribute(
                            value=generate_name("self"), attr="_fields.extend"
                        ),
                        args=[generate_name("args")],
                        keywords=[],
                    )
                ),
                generate_return(value=generate_name("self")),
            ],
            return_type=generate_name(f'"{operation}GraphQL{self.name}"'),
        )

    def _add_import(self, import_: Optional[ast.ImportFrom] = None):
        if import_:
            if self.plugin_manager:
                import_ = self.plugin_manager.generate_client_import(import_)
            if import_.names and import_.module:
                self._imports.append(import_)

    def _generate_method(self, name: str, operation_args) -> ast.FunctionDef:
        arguments = self._generate_method_arguments(operation_args)
        return generate_method_definition(
            name=str_to_snake_case(name),
            arguments=arguments,
            return_type=generate_name(
                f"{self._capitalize_first_letter(name)}GraphQL{self.name}"
            ),
            body=[self._generate_return_stmt(name, operation_args)],
            decorator_list=[generate_name("classmethod")],
        )

    def _generate_method_arguments(self, operation_args):
        cls_arg = generate_arg(name="cls")
        kw_only_args, kw_defaults = self._generate_kw_args_and_defaults(operation_args)
        return generate_arguments(
            args=[cls_arg],
            kwonlyargs=kw_only_args,
            kw_defaults=kw_defaults,
        )

    def _generate_kw_args_and_defaults(self, operation_args):
        kw_only_args = []
        kw_defaults = []
        for arg_name, arg_type in operation_args.items():
            arg_final_type = get_final_type(arg_type)
            if isinstance(arg_final_type, GraphQLInputObjectType):
                self._add_import(
                    generate_import_from(
                        names=[arg_final_type.name], from_="input_types", level=1
                    )
                )
            if isinstance(arg_final_type, GraphQLEnumType):
                self._add_import(
                    generate_import_from(
                        names=[arg_final_type.name], from_="enums", level=1
                    )
                )
            annotation, _ = self._parse_graphql_type_name(arg_final_type)
            kw_only_args.append(generate_arg(name=arg_name, annotation=annotation))
            kw_defaults.append(generate_constant(value=None))
        return kw_only_args, kw_defaults

    def _generate_return_stmt(self, name, operation_args):
        arguments_call = generate_call(
            func=generate_name("clean_arguments"),
            args=[],
            keywords=[
                generate_keyword(arg=arg_name, value=generate_name(arg_name))
                for arg_name in operation_args
            ],
        )
        return generate_return(
            value=generate_call(
                func=generate_name(
                    f"{self._capitalize_first_letter(name)}GraphQL{self.name}"
                ),
                args=[],
                keywords=[
                    generate_keyword(arg="name", value=generate_constant(value=name)),
                    generate_keyword(arguments_call, "arguments"),
                ],
            )
        )

    def _parse_graphql_type_name(
        self, type_, nullable: bool = True
    ) -> Tuple[Union[ast.Name, ast.Subscript], Optional[str]]:
        name = type_.name

        used_custom_scalar = None
        if isinstance(type_, GraphQLInputObjectType):
            self._used_inputs.append(name)
        elif isinstance(type_, GraphQLEnumType):
            self._used_enums.append(name)
        elif isinstance(type_, GraphQLScalarType):
            if name not in self.custom_scalars:
                name = INPUT_SCALARS_MAP.get(name, ANY)
            else:
                used_custom_scalar = name
                name = self.custom_scalars[name].type_name
        else:
            raise ParsingError(f"Incorrect argument type {name}")

        return generate_annotation_name(name, nullable), used_custom_scalar

    def _generate_clean_arguments_function(self) -> ast.FunctionDef:
        return ast.FunctionDef(
            name="clean_arguments",
            args=generate_arguments(
                kwarg=generate_arg("kwargs", annotation=generate_name("Any")),
            ),
            body=[
                generate_return(
                    value=ast.DictComp(
                        key=generate_name("key"),
                        value=generate_name("value"),
                        generators=[
                            ast.comprehension(
                                target=ast.Tuple(
                                    elts=[generate_name("key"), generate_name("value")],
                                    ctx=ast.Store(),
                                ),
                                iter=generate_call(func=generate_name("kwargs.items")),
                                ifs=[
                                    ast.Compare(
                                        left=generate_name("value"),
                                        ops=[ast.IsNot()],
                                        comparators=[generate_constant(value=None)],
                                    )
                                ],
                                is_async=0,
                            )
                        ],
                    )
                )
            ],
            decorator_list=[],
            returns=generate_name("Dict[str, Any]"),
            lineno=1,
        )

    @staticmethod
    def _capitalize_first_letter(s: str) -> str:
        return s[0].upper() + s[1:]
