import ast
from typing import Dict, List, Optional, Tuple, Union, cast

from graphql import (
    GraphQLEnumType,
    GraphQLFieldMap,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)

from ariadne_codegen.exceptions import ParsingError
from ariadne_codegen.utils import str_to_snake_case

from ..codegen import (
    generate_annotation_name,
    generate_arg,
    generate_arguments,
    generate_call,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_keyword,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
)
from ..plugins.manager import PluginManager
from .constants import (
    ANY,
    BASE_MODEL_FILE_PATH,
    CUSTOM_FIELDS_FILE_PATH,
    CUSTOM_FIELDS_TYPING_FILE_PATH,
    INPUT_SCALARS_MAP,
    OPTIONAL,
    TYPING_MODULE,
    UPLOAD_CLASS_NAME,
)
from .scalars import ScalarData
from .utils import get_final_type


class CustomOperationGenerator:
    def __init__(
        self,
        graphql_fields: GraphQLFieldMap,
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
        self._add_import(generate_import_from([OPTIONAL, ANY], TYPING_MODULE))

        self._class_def = generate_class_def(name=name, base_names=[])

        self._used_inputs: List[str] = []

    def generate(self) -> ast.Module:
        """Generate module with class definition of graphql client."""

        for name, field in self.graphql_fields.items():
            final_type = get_final_type(field)
            # if isinstance(final_type, GraphQLObjectType):
            method_def = self._generate_method(
                operation_name=name,
                operation_args=field.args,
                final_type=final_type,
            )
            method_def.lineno = len(self._class_def.body) + 1
            self._class_def.body.append(method_def)

        if not self._class_def.body:
            self._class_def.body.append(ast.Pass())

        self._class_def.lineno = len(self._imports) + 3

        module = generate_module(
            body=cast(List[ast.stmt], self._imports)
            + cast(List[ast.stmt], self._type_imports)
            + [self._class_def],
        )
        return module

    def _add_import(self, import_: Optional[ast.ImportFrom] = None):
        if import_:
            if self.plugin_manager:
                import_ = self.plugin_manager.generate_client_import(import_)
            if import_.names and import_.module:
                self._imports.append(import_)

    def _generate_method(
        self,
        operation_name: str,
        operation_args,
        final_type,
    ) -> ast.FunctionDef:
        arguments = self._generate_method_arguments(operation_args)
        from_ = CUSTOM_FIELDS_TYPING_FILE_PATH.stem
        if isinstance(final_type, GraphQLObjectType):
            return_type_name = f"{final_type.name}Fields"
            from_ = CUSTOM_FIELDS_FILE_PATH.stem
        elif isinstance(final_type, GraphQLInterfaceType):
            return_type_name = f"{final_type.name}Interface"
            from_ = CUSTOM_FIELDS_FILE_PATH.stem
        elif isinstance(final_type, GraphQLUnionType):
            return_type_name = f"{final_type.name}Union"
        else:
            return_type_name = "GraphQLField"
        self._type_imports.append(
            generate_import_from(
                from_=from_,
                names=[return_type_name],
                level=1,
            )
        )

        return generate_method_definition(
            name=str_to_snake_case(operation_name),
            arguments=arguments,
            return_type=generate_name(return_type_name),
            body=[
                self._generate_return_stmt(
                    return_type_name,
                    operation_name,
                    operation_args,
                )
            ],
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
            annotation, _ = self._parse_graphql_type_name(arg_final_type)
            kw_only_args.append(generate_arg(name=arg_name, annotation=annotation))
            kw_defaults.append(generate_constant(value=None))
        return kw_only_args, kw_defaults

    def _generate_return_stmt(self, return_type_name, operation_name, operation_args):
        keywords = [
            generate_keyword(arg=arg_name, value=generate_name(arg_name))
            for arg_name in operation_args
        ]
        return generate_return(
            value=generate_call(
                func=generate_name(return_type_name),
                args=[],
                keywords=[
                    generate_keyword(
                        arg="field_name", value=generate_constant(value=operation_name)
                    ),
                    *keywords,
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
            self._add_import(
                generate_import_from(
                    names=[name],
                    from_="input_types",
                    level=1,
                )
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
                used_custom_scalar = name
                name = self.custom_scalars[name].type_name
        else:
            raise ParsingError(f"Incorrect argument type {name}")

        return generate_annotation_name(name, nullable), used_custom_scalar

    @staticmethod
    def _capitalize_first_letter(s: str) -> str:
        return s[0].upper() + s[1:]
