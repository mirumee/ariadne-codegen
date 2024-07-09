import ast
from typing import Dict, List, Optional, Tuple, Union, cast

from graphql import (
    GraphQLEnumType,
    GraphQLFieldMap,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)

from ..codegen import (
    generate_annotation_name,
    generate_arg,
    generate_arguments,
    generate_call,
    generate_class_def,
    generate_constant,
    generate_dict,
    generate_import_from,
    generate_keyword,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
)
from ..exceptions import ParsingError
from ..plugins.manager import PluginManager
from ..utils import process_name, str_to_snake_case
from .arguments import ArgumentsGenerator
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
from .scalars import ScalarData, generate_scalar_imports
from .utils import get_final_type


class CustomOperationGenerator:
    def __init__(
        self,
        graphql_fields: GraphQLFieldMap,
        name: str,
        base_name: str,
        arguments_generator: ArgumentsGenerator,
        enums_module_name: str = "enums",
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
        convert_to_snake_case: bool = True,
    ) -> None:
        self.graphql_fields = graphql_fields
        self.name = name
        self.base_name = base_name
        self.enums_module_name = enums_module_name
        self.plugin_manager = plugin_manager
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self._used_custom_scalars: List[str] = []
        self.arguments_generator = arguments_generator
        self.convert_to_snake_case = convert_to_snake_case

        self._imports: List[ast.ImportFrom] = []
        self._type_imports: List[ast.ImportFrom] = []
        self._add_import(generate_import_from([OPTIONAL, ANY], TYPING_MODULE))

        self._class_def = generate_class_def(name=name, base_names=[])

        self._used_inputs: List[str] = []

    def generate(self) -> ast.Module:
        """Generate module with class definition of graphql client."""
        for name, field in self.graphql_fields.items():
            final_type = get_final_type(field)
            method_def = self._generate_method(
                operation_name=name,
                operation_args=field.args,
                final_type=final_type,
            )
            method_def.lineno = len(self._class_def.body) + 1
            self._class_def.body.append(method_def)

        if not self._class_def.body:
            self._class_def.body.append(ast.Pass())

        self._add_custom_scalar_imports()

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
        return_type_name, from_ = self._get_return_type_and_from(final_type)

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
        kw_only_args, kw_defaults, args = self._generate_kw_args_and_defaults(
            operation_args,
        )
        return generate_arguments(
            args=[cls_arg, *args],
            kwonlyargs=kw_only_args,
            kw_defaults=kw_defaults,
        )

    def _generate_kw_args_and_defaults(self, operation_args):
        kw_only_args = []
        kw_defaults = []
        args = []
        for arg_name, arg_type in operation_args.items():
            arg_name = process_name(
                arg_name,
                convert_to_snake_case=self.convert_to_snake_case,
            )
            arg_final_type = get_final_type(arg_type)
            is_required = isinstance(arg_type.type, GraphQLNonNull)
            annotation, _ = self._parse_graphql_type_name(
                arg_final_type,
                not is_required,
            )
            arg = generate_arg(name=arg_name, annotation=annotation)
            if is_required:
                args.append(arg)
            else:
                kw_only_args.append(arg)
                kw_defaults.append(generate_constant(value=None))
        return kw_only_args, kw_defaults, args

    def _generate_return_stmt(self, return_type_name, operation_name, operation_args):
        arguments_dict = self._generate_arguments_dict(operation_args)

        arguments_keyword = generate_keyword(
            arg="arguments",
            value=generate_dict(
                keys=arguments_dict.keys(),
                values=arguments_dict.values(),
            ),
        )

        return generate_return(
            value=generate_call(
                func=generate_name(return_type_name),
                args=[],
                keywords=[
                    generate_keyword(
                        arg="field_name", value=generate_constant(value=operation_name)
                    ),
                    arguments_keyword,
                ],
            )
        )

    def _generate_arguments_dict(self, operation_args):
        arguments_dict = {}
        for arg_name, arg_value in operation_args.items():
            final_type = get_final_type(arg_value)
            is_required = isinstance(arg_value.type, GraphQLNonNull)
            constant_value = f"{final_type.name}!" if is_required else final_type.name
            arguments_dict[generate_constant(arg_name)] = generate_dict(
                keys=[generate_constant("type"), generate_constant("value")],
                values=[
                    generate_constant(constant_value),
                    self._get_dict_value(arg_name, arg_value),
                ],
            )
        return arguments_dict

    def _get_dict_value(self, name: str, arg_value) -> Union[ast.Name, ast.Call]:
        name = process_name(
            name,
            convert_to_snake_case=self.convert_to_snake_case,
        )
        _, used_custom_scalar = self._parse_graphql_type_name(get_final_type(arg_value))
        if used_custom_scalar:
            self._used_custom_scalars.append(used_custom_scalar)
            scalar_data = self.custom_scalars[used_custom_scalar]
            if scalar_data.serialize_name:
                return generate_call(
                    func=generate_name(scalar_data.serialize_name),
                    args=[generate_name(name)],
                )
        return generate_name(name)

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
            self._add_import(
                generate_import_from(
                    names=[name],
                    from_=self.enums_module_name,
                    level=1,
                )
            )
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
                self._used_custom_scalars.append(used_custom_scalar)
        else:
            raise ParsingError(f"Incorrect argument type {name}")

        return generate_annotation_name(name, nullable), used_custom_scalar

    def _get_return_type_and_from(self, final_type):
        if isinstance(final_type, GraphQLObjectType):
            return_type_name = f"{final_type.name}Fields"
            from_ = CUSTOM_FIELDS_FILE_PATH.stem
        elif isinstance(final_type, GraphQLInterfaceType):
            return_type_name = f"{final_type.name}Interface"
            from_ = CUSTOM_FIELDS_FILE_PATH.stem
        elif isinstance(final_type, GraphQLUnionType):
            return_type_name = f"{final_type.name}Union"
            from_ = CUSTOM_FIELDS_TYPING_FILE_PATH.stem
        else:
            return_type_name = "GraphQLField"
            from_ = CUSTOM_FIELDS_TYPING_FILE_PATH.stem
        return return_type_name, from_

    def _add_custom_scalar_imports(self):
        for custom_scalar_name in self._used_custom_scalars:
            scalar_data = self.custom_scalars[custom_scalar_name]
            for import_ in generate_scalar_imports(scalar_data):
                self._add_import(import_)

    @staticmethod
    def _capitalize_first_letter(s: str) -> str:
        return s[0].upper() + s[1:]
