import ast
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from graphql import (
    GraphQLEnumType,
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
    generate_comp,
    generate_constant,
    generate_dict,
    generate_import_from,
    generate_keyword,
    generate_name,
    generate_subscript,
    generate_tuple,
)
from ..exceptions import ParsingError
from ..plugins.manager import PluginManager
from ..utils import process_name
from .constants import (
    ANY,
    BASE_MODEL_FILE_PATH,
    DICT,
    INPUT_SCALARS_MAP,
    UPLOAD_CLASS_NAME,
)
from .custom_generator_utils import get_final_type
from .scalars import ScalarData, generate_scalar_imports


class ArgumentGenerator:
    """Generates method arguments for GraphQL fields."""

    def __init__(
        self,
        custom_scalars: Dict[str, ScalarData],
        convert_to_snake_case: bool,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.custom_scalars = custom_scalars
        self.convert_to_snake_case = convert_to_snake_case
        self.plugin_manager = plugin_manager
        self.imports: List[ast.ImportFrom] = []
        self._used_custom_scalars: List[str] = []

    def _add_import(self, import_: Optional[ast.ImportFrom] = None) -> None:
        """Adds an import statement to the list of imports."""
        if import_:
            if self.plugin_manager:
                import_ = self.plugin_manager.generate_client_import(import_)
            if import_.names:
                self.imports.append(import_)

    def generate_arguments(
        self, operation_args: Dict[str, Any]
    ) -> Tuple[ast.arguments, List[ast.expr], List[ast.expr]]:
        """Generates method arguments from operation arguments."""
        cls_arg = generate_arg(name="cls")
        args: List[ast.arg] = []
        kw_only_args: List[ast.arg] = []
        kw_defaults: List[ast.expr] = []
        return_arguments_keys: List[ast.expr] = []
        return_arguments_values: List[ast.expr] = []

        for arg_name, arg_value in operation_args.items():
            final_type = get_final_type(arg_value)
            is_required = isinstance(arg_value.type, GraphQLNonNull)
            name = process_name(
                arg_name, convert_to_snake_case=self.convert_to_snake_case
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
        self,
        args: List[ast.arg],
        kw_only_args: List[ast.arg],
        kw_defaults: List[ast.expr],
        name: str,
        annotation: Optional[Union[ast.Name, ast.Subscript]],
        is_required: bool,
    ) -> None:
        """Accumulates method arguments."""
        if is_required:
            args.append(generate_arg(name=name, annotation=annotation))
        else:
            kw_only_args.append(generate_arg(name=name, annotation=annotation))
            kw_defaults.append(generate_constant(value=None))

    def _accumulate_return_arguments(
        self,
        return_arguments_keys: List[ast.expr],
        return_arguments_values: List[ast.expr],
        arg_name: str,
        name: str,
        final_type: Union[GraphQLObjectType, GraphQLInterfaceType, GraphQLUnionType],
        is_required: bool,
        used_custom_scalar: Optional[str],
    ) -> None:
        """Accumulates return arguments."""
        constant_value = f"{final_type.name}!" if is_required else final_type.name
        return_arg_dict_value = self._generate_return_arg_value(
            name, used_custom_scalar
        )

        return_arguments_keys.append(generate_constant(arg_name))
        return_arguments_values.append(
            generate_dict(
                keys=[generate_constant("type"), generate_constant("value")],
                values=[generate_constant(constant_value), return_arg_dict_value],
            )
        )

    def _generate_return_arg_value(
        self, name: str, used_custom_scalar: Optional[str]
    ) -> Union[ast.Call, ast.Name]:
        """Generates the return argument value."""
        return_arg_dict_value: Union[ast.Call, ast.Name] = generate_name(name)

        if used_custom_scalar:
            self._used_custom_scalars.append(used_custom_scalar)
            scalar_data = self.custom_scalars[used_custom_scalar]
            if scalar_data.serialize_name:
                return_arg_dict_value = generate_call(
                    func=generate_name(scalar_data.serialize_name),
                    args=[generate_name(name)],
                )

        return return_arg_dict_value

    def _assemble_method_arguments(
        self,
        cls_arg: ast.arg,
        args: List[ast.arg],
        kw_only_args: List[ast.arg],
        kw_defaults: List[ast.expr],
    ) -> ast.arguments:
        """Assembles method arguments."""
        return generate_arguments(
            args=[cls_arg, *args],
            kwonlyargs=kw_only_args,
            kw_defaults=kw_defaults,  # type: ignore
        )

    def _parse_graphql_type_name(
        self,
        type_: Union[GraphQLScalarType, GraphQLInputObjectType, GraphQLEnumType],
        nullable: bool = True,
    ) -> Tuple[Union[ast.Name, ast.Subscript], Optional[str]]:
        """Parses the GraphQL type name and determines if it is a custom scalar."""
        name = type_.name
        used_custom_scalar = None
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
                used_custom_scalar = name
                name = self.custom_scalars[name].type_name
                self._used_custom_scalars.append(used_custom_scalar)
        else:
            raise ParsingError(f"Incorrect argument type {name}")
        return generate_annotation_name(name, nullable), used_custom_scalar

    def add_custom_scalar_imports(self) -> None:
        """Adds imports for custom scalars used in the schema."""
        for custom_scalar_name in self._used_custom_scalars:
            scalar_data = self.custom_scalars[custom_scalar_name]
            for import_ in generate_scalar_imports(scalar_data):
                self._add_import(import_)

    def generate_clear_arguments_section(
        self,
        return_arguments_keys: List[ast.expr],
        return_arguments_values: List[ast.expr],
    ) -> Tuple[List[ast.stmt], List[ast.keyword]]:
        arguments_body = [
            generate_ann_assign(
                generate_name("arguments"),
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
                generate_dict(
                    return_arguments_keys,  # type: ignore
                    return_arguments_values,
                ),
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
                            ifs=cast(
                                List[ast.expr],
                                [
                                    ast.Compare(
                                        left=generate_subscript(
                                            value=generate_name("value"),
                                            slice_=generate_constant("value"),
                                        ),
                                        ops=[ast.IsNot()],
                                        comparators=[generate_constant(None)],
                                    )
                                ],
                            ),
                        )
                    ],
                ),
            ),
        ]
        arguments_keyword = [
            generate_keyword(arg="arguments", value=generate_name("cleared_arguments"))
        ]
        return arguments_body, arguments_keyword
