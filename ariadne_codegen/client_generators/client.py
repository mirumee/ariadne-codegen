import ast
from typing import Dict, List, Optional, Union

from graphql import OperationDefinitionNode, OperationType

from ..codegen import (
    generate_ann_assign,
    generate_arg,
    generate_arguments,
    generate_assign,
    generate_async_for,
    generate_async_method_definition,
    generate_attribute,
    generate_await,
    generate_call,
    generate_class_def,
    generate_comp,
    generate_constant,
    generate_expr,
    generate_import_from,
    generate_keyword,
    generate_list,
    generate_list_comp,
    generate_method_definition,
    generate_module,
    generate_name,
    generate_return,
    generate_subscript,
    generate_tuple,
    generate_yield,
)
from ..exceptions import NotSupported
from ..plugins.manager import PluginManager
from .arguments import ArgumentsGenerator
from .constants import (
    ANY,
    ASYNC_ITERATOR,
    BASE_GRAPHQL_FIELD_CLASS_NAME,
    BASE_OPERATION_FILE_PATH,
    DICT,
    DOCUMENT_NODE,
    GRAPHQL_MODULE,
    KWARGS_NAMES,
    LIST,
    MODEL_VALIDATE_METHOD,
    NAME_NODE,
    OPERATION_DEFINITION_NODE,
    OPERATION_TYPE,
    OPTIONAL,
    PRINT_AST,
    SELECTION_SET_NODE,
    TYPING_MODULE,
    UNION,
    UNSET_IMPORT,
    UPLOAD_IMPORT,
)
from .scalars import ScalarData, generate_scalar_imports


class ClientGenerator:
    def __init__(
        self,
        base_client_import: ast.ImportFrom,
        arguments_generator: ArgumentsGenerator,
        name: str = "Client",
        base_client: str = "AsyncBaseClient",
        enums_module_name: str = "enums",
        input_types_module_name: str = "input_types",
        unset_import: ast.ImportFrom = UNSET_IMPORT,
        upload_import: ast.ImportFrom = UPLOAD_IMPORT,
        custom_scalars: Optional[Dict[str, ScalarData]] = None,
        plugin_manager: Optional[PluginManager] = None,
    ) -> None:
        self.name = name
        self.enums_module_name = enums_module_name
        self.input_types_module_name = input_types_module_name
        self.plugin_manager = plugin_manager
        self.custom_scalars = custom_scalars if custom_scalars else {}
        self.arguments_generator = arguments_generator

        self._imports: List[Union[ast.ImportFrom, ast.Import]] = []
        self._add_import(
            generate_import_from(
                [
                    OPTIONAL,
                    LIST,
                    DICT,
                    ANY,
                    UNION,
                    ASYNC_ITERATOR,
                ],
                TYPING_MODULE,
            )
        )
        self._add_import(base_client_import)
        self._add_import(unset_import)
        self._add_import(upload_import)

        self._class_def = generate_class_def(name=name, base_names=[base_client])
        self._gql_func_name = "gql"
        self._operation_str_variable = "query"
        self._variables_dict_variable = "variables"
        self._response_variable = "response"
        self._data_variable = "data"

    def generate(self) -> ast.Module:
        """Generate module with class definition of graphql client."""
        self._add_import(
            generate_import_from(
                names=self.arguments_generator.get_used_inputs(),
                from_=self.input_types_module_name,
                level=1,
            )
        )
        self._add_import(
            generate_import_from(
                names=self.arguments_generator.get_used_enums(),
                from_=self.enums_module_name,
                level=1,
            )
        )
        for custom_scalar_name in self.arguments_generator.get_used_custom_scalars():
            scalar_data = self.custom_scalars[custom_scalar_name]
            for import_ in generate_scalar_imports(scalar_data):
                self._add_import(import_)

        gql_func = self._generate_gql_func()
        gql_func.lineno = len(self._imports) + 1
        if self.plugin_manager:
            gql_func = self.plugin_manager.generate_gql_function(gql_func)

        self._class_def.lineno = len(self._imports) + 3
        if not self._class_def.body:
            self._class_def.body.append(ast.Pass())
        if self.plugin_manager:
            self._class_def = self.plugin_manager.generate_client_class(self._class_def)

        module = generate_module(
            body=self._imports + [gql_func, self._class_def],
        )
        if self.plugin_manager:
            module = self.plugin_manager.generate_client_module(module)
        return module

    def add_method(
        self,
        definition: OperationDefinitionNode,
        name: str,
        return_type: str,
        return_type_module: str,
        operation_str: str,
        async_: bool = True,
    ):
        """Add method to client."""
        arguments, arguments_dict = self.arguments_generator.generate(
            definition.variable_definitions
        )

        variable_names = self.get_variable_names(arguments)

        operation_name = definition.name.value if definition.name else ""
        if definition.operation == OperationType.SUBSCRIPTION:
            if not async_:
                raise NotSupported(
                    "Subscriptions are only available when using async client."
                )
            method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef] = (
                self._generate_subscription_method_def(
                    name=name,
                    operation_name=operation_name,
                    return_type=return_type,
                    arguments=arguments,
                    arguments_dict=arguments_dict,
                    operation_str=operation_str,
                    variable_names=variable_names,
                )
            )
        elif async_:
            method_def = self._generate_async_method(
                name=name,
                return_type=return_type,
                arguments=arguments,
                arguments_dict=arguments_dict,
                operation_str=operation_str,
                operation_name=operation_name,
                variable_names=variable_names,
            )
        else:
            method_def = self._generate_method(
                name=name,
                return_type=return_type,
                arguments=arguments,
                arguments_dict=arguments_dict,
                operation_str=operation_str,
                operation_name=operation_name,
                variable_names=variable_names,
            )

        method_def.lineno = len(self._class_def.body) + 1
        if self.plugin_manager:
            method_def = self.plugin_manager.generate_client_method(
                method_def, operation_definition=definition
            )

        self._class_def.body.append(method_def)
        self._add_import(
            generate_import_from(names=[return_type], from_=return_type_module, level=1)
        )

    def add_execute_custom_operation_method(self):
        self._add_import(
            generate_import_from(
                [
                    DOCUMENT_NODE,
                    OPERATION_DEFINITION_NODE,
                    NAME_NODE,
                    SELECTION_SET_NODE,
                    PRINT_AST,
                ],
                GRAPHQL_MODULE,
            )
        )
        self._add_import(
            generate_import_from(
                [BASE_GRAPHQL_FIELD_CLASS_NAME], BASE_OPERATION_FILE_PATH.stem, level=1
            )
        )
        execute_await = generate_await(
            value=generate_call(
                func=generate_attribute(value=generate_name("self"), attr="execute"),
                args=[
                    generate_call(
                        func=generate_name("print_ast"),
                        args=[generate_name("operation_ast")],
                    )
                ],
                keywords=[
                    generate_keyword(
                        arg="operation_name", value=generate_name("operation_name")
                    )
                ],
            )
        )

        operation_definition_node = generate_call(
            func=generate_name("OperationDefinitionNode"),
            keywords=[
                generate_keyword(
                    arg="operation", value=generate_name("operation_type")
                ),
                generate_keyword(
                    arg="name",
                    value=generate_call(
                        func=generate_name("NameNode"),
                        keywords=[
                            generate_keyword(
                                arg="value", value=generate_name("operation_name")
                            )
                        ],
                    ),
                ),
                generate_keyword(
                    arg="selection_set",
                    value=generate_call(
                        func=generate_name("SelectionSetNode"),
                        keywords=[
                            generate_keyword(
                                arg="selections",
                                value=generate_list_comp(
                                    elt=generate_call(
                                        func=generate_attribute(
                                            value=generate_name("field"),
                                            attr="to_ast",
                                        ),
                                    ),
                                    generators=[
                                        generate_comp(
                                            target="field",
                                            iter_="fields",
                                        )
                                    ],
                                ),
                            )
                        ],
                    ),
                ),
            ],
        )
        operation_ast = generate_call(
            func=generate_name("DocumentNode"),
            keywords=[
                generate_keyword(
                    arg="definitions",
                    value=generate_list(elements=[operation_definition_node]),
                )
            ],
        )
        body_return = generate_return(
            value=generate_call(
                func=generate_attribute(value=generate_name("self"), attr="get_data"),
                args=[generate_name("response")],
            )
        )
        async_def_node = generate_async_method_definition(
            name="execute_custom_operation",
            arguments=generate_arguments(
                args=[
                    generate_arg("self"),
                    generate_arg(
                        "*fields",
                        annotation=generate_name("GraphQLField"),
                    ),
                    generate_arg(
                        "operation_type",
                        annotation=generate_name("OperationType"),
                    ),
                    generate_arg("operation_name", annotation=generate_name("str")),
                ],
            ),
            body=[
                generate_assign(
                    targets=["operation_ast"],
                    value=operation_ast,
                ),
                generate_assign(
                    targets=["response"],
                    value=execute_await,
                ),
                body_return,
            ],
            return_type=generate_subscript(
                generate_name(DICT),
                generate_tuple([generate_name("str"), generate_name("Any")]),
            ),
        )
        self._class_def.body.append(async_def_node)

    def create_custom_operation_method(self, name, operation_type):
        self._add_import(
            generate_import_from(
                [
                    OPERATION_TYPE,
                ],
                GRAPHQL_MODULE,
            )
        )
        body_return = generate_return(
            value=generate_await(
                value=generate_call(
                    func=generate_attribute(
                        value=generate_name("self"),
                        attr="execute_custom_operation",
                    ),
                    args=[
                        generate_name("*fields"),
                    ],
                    keywords=[
                        generate_keyword(
                            arg="operation_type",
                            value=generate_attribute(
                                value=generate_name("OperationType"),
                                attr=operation_type,
                            ),
                        ),
                        generate_keyword(
                            arg="operation_name", value=generate_name("operation_name")
                        ),
                    ],
                )
            )
        )
        async_def_query = generate_async_method_definition(
            name=name,
            arguments=generate_arguments(
                args=[
                    generate_arg("self"),
                    generate_arg("*fields", annotation=generate_name("GraphQLField")),
                    generate_arg("operation_name", annotation=generate_name("str")),
                ],
            ),
            body=[body_return],
            return_type=generate_subscript(
                generate_name(DICT),
                generate_tuple([generate_name("str"), generate_name("Any")]),
            ),
        )
        self._class_def.body.append(async_def_query)

    def get_variable_names(self, arguments: ast.arguments) -> Dict[str, str]:
        mapped_variable_names = [
            self._operation_str_variable,
            self._variables_dict_variable,
            self._response_variable,
            self._data_variable,
        ]
        variable_names = {}
        argument_names = set(arg.arg for arg in arguments.args)

        for variable in mapped_variable_names:
            variable_names[variable] = (
                f"_{variable}" if variable in argument_names else variable
            )

        return variable_names

    def _add_import(self, import_: Optional[ast.ImportFrom] = None):
        if not import_:
            return
        if self.plugin_manager:
            import_ = self.plugin_manager.generate_client_import(import_)
        if import_.names and import_.module:
            self._imports.append(import_)

    def _generate_subscription_method_def(
        self,
        name: str,
        operation_name: str,
        return_type: str,
        arguments: ast.arguments,
        arguments_dict: ast.Dict,
        operation_str: str,
        variable_names: Dict[str, str],
    ) -> ast.AsyncFunctionDef:
        return generate_async_method_definition(
            name=name,
            arguments=arguments,
            return_type=generate_subscript(
                value=generate_name(ASYNC_ITERATOR), slice_=generate_name(return_type)
            ),
            body=[
                self._generate_operation_str_assign(variable_names, operation_str, 1),
                self._generate_variables_assign(variable_names, arguments_dict, 2),
                self._generate_async_generator_loop(
                    variable_names, operation_name, return_type, 3
                ),
            ],
        )

    def _generate_async_method(
        self,
        name: str,
        return_type: str,
        arguments: ast.arguments,
        arguments_dict: ast.Dict,
        operation_str: str,
        operation_name: str,
        variable_names: Dict[str, str],
    ) -> ast.AsyncFunctionDef:
        return generate_async_method_definition(
            name=name,
            arguments=arguments,
            return_type=generate_name(return_type),
            body=[
                self._generate_operation_str_assign(variable_names, operation_str, 1),
                self._generate_variables_assign(variable_names, arguments_dict, 2),
                self._generate_async_response_assign(variable_names, operation_name, 3),
                self._generate_data_retrieval(variable_names),
                self._generate_return_parsed_obj(variable_names, return_type),
            ],
        )

    def _generate_method(
        self,
        name: str,
        return_type: str,
        arguments: ast.arguments,
        arguments_dict: ast.Dict,
        operation_str: str,
        operation_name: str,
        variable_names: Dict[str, str],
    ) -> ast.FunctionDef:
        return generate_method_definition(
            name=name,
            arguments=arguments,
            return_type=generate_name(return_type),
            body=[
                self._generate_operation_str_assign(variable_names, operation_str, 1),
                self._generate_variables_assign(variable_names, arguments_dict, 2),
                self._generate_response_assign(variable_names, operation_name, 3),
                self._generate_data_retrieval(variable_names),
                self._generate_return_parsed_obj(variable_names, return_type),
            ],
        )

    def _generate_operation_str_assign(
        self, variable_names: Dict[str, str], operation_str: str, lineno: int = 1
    ) -> ast.Assign:
        return generate_assign(
            targets=[variable_names[self._operation_str_variable]],
            value=generate_call(
                func=generate_name(self._gql_func_name),
                args=[
                    [generate_constant(l + "\n") for l in operation_str.splitlines()]
                ],
            ),
            lineno=lineno,
        )

    def _generate_variables_assign(
        self, variable_names: Dict[str, str], arguments_dict: ast.Dict, lineno: int = 1
    ) -> ast.AnnAssign:
        return generate_ann_assign(
            target=variable_names[self._variables_dict_variable],
            annotation=generate_subscript(
                generate_name(DICT),
                generate_tuple([generate_name("str"), generate_name("object")]),
            ),
            value=arguments_dict,
            lineno=lineno,
        )

    def _generate_async_response_assign(
        self, variable_names: Dict[str, str], operation_name: str, lineno: int = 1
    ) -> ast.Assign:
        return generate_assign(
            targets=[variable_names[self._response_variable]],
            value=generate_await(
                self._generate_execute_call(variable_names, operation_name)
            ),
            lineno=lineno,
        )

    def _generate_response_assign(
        self,
        variable_names: Dict[str, str],
        operation_name: str,
        lineno: int = 1,
    ) -> ast.Assign:
        return generate_assign(
            targets=[variable_names[self._response_variable]],
            value=self._generate_execute_call(variable_names, operation_name),
            lineno=lineno,
        )

    def _generate_execute_call(
        self, variable_names: Dict[str, str], operation_name: str
    ) -> ast.Call:
        return generate_call(
            func=generate_attribute(generate_name("self"), "execute"),
            keywords=[
                generate_keyword(
                    value=generate_name(variable_names[self._operation_str_variable]),
                    arg="query",
                ),
                generate_keyword(
                    value=generate_constant(operation_name), arg="operation_name"
                ),
                generate_keyword(
                    value=generate_name(variable_names[self._variables_dict_variable]),
                    arg="variables",
                ),
                generate_keyword(value=generate_name(KWARGS_NAMES)),
            ],
        )

    def _generate_data_retrieval(self, variable_names: Dict[str, str]) -> ast.Assign:
        return generate_assign(
            targets=[variable_names[self._data_variable]],
            value=generate_call(
                func=generate_attribute(value=generate_name("self"), attr="get_data"),
                args=[generate_name(variable_names[self._response_variable])],
            ),
        )

    def _generate_return_parsed_obj(
        self, variable_names: Dict[str, str], return_type: str
    ) -> ast.Return:
        return generate_return(
            generate_call(
                func=generate_attribute(
                    generate_name(return_type), MODEL_VALIDATE_METHOD
                ),
                args=[generate_name(variable_names[self._data_variable])],
            )
        )

    def _generate_async_generator_loop(
        self,
        variable_names: Dict[str, str],
        operation_name: str,
        return_type: str,
        lineno: int = 1,
    ) -> ast.AsyncFor:
        return generate_async_for(
            target=generate_name(variable_names[self._data_variable]),
            iter_=generate_call(
                func=generate_attribute(value=generate_name("self"), attr="execute_ws"),
                keywords=[
                    generate_keyword(
                        value=generate_name(
                            variable_names[self._operation_str_variable]
                        ),
                        arg="query",
                    ),
                    generate_keyword(
                        value=generate_constant(operation_name), arg="operation_name"
                    ),
                    generate_keyword(
                        value=generate_name(
                            variable_names[self._variables_dict_variable]
                        ),
                        arg="variables",
                    ),
                    generate_keyword(value=generate_name(KWARGS_NAMES)),
                ],
            ),
            body=[self._generate_yield_parsed_obj(variable_names, return_type)],
            lineno=lineno,
        )

    def _generate_yield_parsed_obj(
        self, variable_names: Dict[str, str], return_type: str
    ) -> ast.Expr:
        return generate_expr(
            generate_yield(
                generate_call(
                    func=generate_attribute(
                        value=generate_name(return_type),
                        attr=MODEL_VALIDATE_METHOD,
                    ),
                    args=[generate_name(variable_names[self._data_variable])],
                )
            )
        )

    def _generate_gql_func(self) -> ast.FunctionDef:
        str_name = generate_name("str")
        arg = "q"
        return generate_method_definition(
            name=self._gql_func_name,
            arguments=generate_arguments([generate_arg(arg, str_name)]),
            return_type=str_name,
            body=[generate_return(generate_name(arg))],
        )
