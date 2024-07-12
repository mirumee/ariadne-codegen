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
    generate_ann_assign,
    generate_annotation_name,
    generate_arg,
    generate_arguments,
    generate_assign,
    generate_call,
    generate_class_def,
    generate_comp,
    generate_constant,
    generate_dict,
    generate_import_from,
    generate_keyword,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
    generate_subscript,
    generate_tuple,
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
    DICT,
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
        self._add_import(generate_import_from([OPTIONAL, ANY, DICT], TYPING_MODULE))

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
        (
            method_arguments,
            return_arguments_keys,
            return_arguments_values,
        ) = self._generate_arguments(operation_args)
        return_type_name = self._get_return_type_and_from(final_type)

        return generate_method_definition(
            name=str_to_snake_case(operation_name),
            arguments=method_arguments,
            return_type=generate_name(return_type_name),
            body=[
                generate_ann_assign(
                    "arguments",
                    generate_subscript(
                        generate_name(DICT),
                        generate_tuple(
                            [
                                generate_name("str"),
                                generate_subscript(
                                    generate_name(DICT),
                                    generate_tuple(
                                        [
                                            generate_name("str"),
                                            generate_name(ANY),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ),
                    generate_dict(return_arguments_keys, return_arguments_values),
                ),
                generate_assign(
                    ["cleared_arguments"],
                    ast.DictComp(
                        key=generate_name("key"),
                        value=generate_name("value"),
                        generators=[
                            generate_comp(
                                target="key, value",
                                iter_="arguments.items()",
                                ifs=[
                                    ast.Compare(
                                        left=generate_subscript(
                                            value=generate_name("value"),
                                            slice_=ast.Index(
                                                value=generate_constant("value"),
                                            ),  # type: ignore
                                        ),
                                        ops=[ast.IsNot()],
                                        comparators=[generate_constant(None)],
                                    )
                                ],
                            )
                        ],
                    ),
                ),
                generate_return(
                    value=generate_call(
                        func=generate_name(return_type_name),
                        args=[],
                        keywords=[
                            generate_keyword(
                                arg="field_name",
                                value=generate_constant(value=operation_name),
                            ),
                            generate_keyword(
                                arg="arguments",
                                value=generate_name("cleared_arguments"),
                            ),
                        ],
                    )
                ),
            ],
            decorator_list=[generate_name("classmethod")],
        )

    def _generate_arguments(self, operation_args):
        cls_arg = generate_arg(name="cls")
        args, kw_only_args, kw_defaults = [], [], []
        return_arguments_keys, return_arguments_values = [], []

        for arg_name, arg_value in operation_args.items():
            final_type = get_final_type(arg_value)
            is_required = isinstance(arg_value.type, GraphQLNonNull)
            name = process_name(
                arg_name,
                convert_to_snake_case=self.convert_to_snake_case,
            )
            annotation, used_custom_scalar = self._parse_graphql_type_name(
                final_type, not is_required
            )

            self._accumulate_method_arguments(
                args, kw_only_args, kw_defaults, name, annotation, is_required
            )
            self._accumulate_return_arguments(
                return_arguments_keys,
                return_arguments_values,
                arg_name,
                name,
                final_type,
                is_required,
                used_custom_scalar,
            )

        method_arguments = self._assemble_method_arguments(
            cls_arg, args, kw_only_args, kw_defaults
        )

        return method_arguments, return_arguments_keys, return_arguments_values

    def _accumulate_method_arguments(
        self, args, kw_only_args, kw_defaults, name, annotation, is_required
    ):
        if is_required:
            args.append(generate_arg(name=name, annotation=annotation))
        else:
            kw_only_args.append(generate_arg(name=name, annotation=annotation))
            kw_defaults.append(generate_constant(value=None))

    def _accumulate_return_arguments(
        self,
        return_arguments_keys,
        return_arguments_values,
        arg_name,
        name,
        final_type,
        is_required,
        used_custom_scalar,
    ):
        constant_value = f"{final_type.name}!" if is_required else final_type.name
        return_arg_dict_value = self._generate_return_arg_value(
            name,
            used_custom_scalar,
        )

        return_arguments_keys.append(generate_constant(arg_name))
        return_arguments_values.append(
            generate_dict(
                keys=[generate_constant("type"), generate_constant("value")],
                values=[generate_constant(constant_value), return_arg_dict_value],
            )
        )

    def _generate_return_arg_value(self, name, used_custom_scalar):
        return_arg_dict_value = generate_name(name)

        if used_custom_scalar:
            self._used_custom_scalars.append(used_custom_scalar)
            scalar_data = self.custom_scalars[used_custom_scalar]
            if scalar_data.serialize_name:
                return_arg_dict_value = generate_call(
                    func=generate_name(scalar_data.serialize_name),
                    args=[generate_name(name)],
                )

        return return_arg_dict_value

    def _assemble_method_arguments(self, cls_arg, args, kw_only_args, kw_defaults):
        return generate_arguments(
            args=[cls_arg, *args],
            kwonlyargs=kw_only_args,
            kw_defaults=kw_defaults,
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
        self._type_imports.append(
            generate_import_from(
                from_=from_,
                names=[return_type_name],
                level=1,
            )
        )
        return return_type_name

    def _add_custom_scalar_imports(self):
        for custom_scalar_name in self._used_custom_scalars:
            scalar_data = self.custom_scalars[custom_scalar_name]
            for import_ in generate_scalar_imports(scalar_data):
                self._add_import(import_)

    @staticmethod
    def _capitalize_first_letter(s: str) -> str:
        return s[0].upper() + s[1:]
