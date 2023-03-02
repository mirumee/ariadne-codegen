import ast
from typing import List

from .codegen import (
    generate_ann_assign,
    generate_arg,
    generate_arguments,
    generate_assign,
    generate_async_method_definition,
    generate_attribute,
    generate_await,
    generate_call,
    generate_class_def,
    generate_constant,
    generate_import_from,
    generate_keyword,
    generate_method_definition,
    generate_name,
    generate_return,
    generate_subscript,
    generate_tuple,
)
from .constants import ANY, LIST, OPTIONAL, TYPING_MODULE


class ClientGenerator:
    def __init__(self, name: str, base_client: str) -> None:
        self.name = name
        self.class_def = generate_class_def(name=name, base_names=[base_client])
        self.imports: list = [
            generate_import_from([OPTIONAL, LIST, ANY], TYPING_MODULE)
        ]

        self._gql_func_name = "gql"
        self._operation_str_variable = "query"
        self._variables_dict_variable = "variables"
        self._response_variable = "response"
        self._data_variable = "data"

    def generate(self) -> ast.Module:
        """Generate module with class definition of grahql client."""
        gql_func = self._generate_gql_func()
        gql_func.lineno = len(self.imports) + 1
        self.class_def.lineno = len(self.imports) + 3
        if not self.class_def.body:
            self.class_def.body.append(ast.Pass())
        return ast.Module(
            body=self.imports + [gql_func, self.class_def],
            type_ignores=[],
        )

    def add_import(self, names: List[str], from_: str, level: int = 0) -> None:
        """Add import to be included in module file."""
        self.imports.append(generate_import_from(names=names, from_=from_, level=level))

    def add_method(
        self,
        name: str,
        return_type: str,
        arguments: ast.arguments,
        arguments_dict: ast.Dict,
        operation_str: str,
        async_: bool = True,
    ):
        """Add method to client."""
        kwargs = {
            "name": name,
            "return_type": return_type,
            "arguments": arguments,
            "arguments_dict": arguments_dict,
            "operation_str": operation_str,
        }
        method_def = (self._generate_async_method if async_ else self._generate_method)(**kwargs)
        method_def.lineno = len(self.class_def.body) + 1
        self.class_def.body.append(method_def)

    def _generate_async_method(
        self,
        name: str,
        return_type: str,
        arguments: ast.arguments,
        arguments_dict: ast.Dict,
        operation_str: str,
    ) -> ast.AsyncFunctionDef:
        return generate_async_method_definition(
            name=name,
            arguments=arguments,
            return_type=generate_name(return_type),
            body=[
                self._generate_operation_str_assign(operation_str, 1),
                self._generate_variables_assign(arguments_dict, 2),
                self._generate_async_response_assign(3),
                self._generate_data_retrieval(),
                self._generate_return_parsed_obj(return_type),
            ],
        )

    def _generate_method(
        self,
        name: str,
        return_type: str,
        arguments: ast.arguments,
        arguments_dict: ast.Dict,
        operation_str: str,
    ) -> ast.FunctionDef:
        return generate_method_definition(
            name=name,
            arguments=arguments,
            return_type=generate_name(return_type),
            body=[
                self._generate_operation_str_assign(operation_str, 1),
                self._generate_variables_assign(arguments_dict, 2),
                self._generate_response_assign(3),
                self._generate_data_retrieval(),
                self._generate_return_parsed_obj(return_type),
            ],
        )

    def _generate_operation_str_assign(
        self, operation_str: str, lineno: int = 1
    ) -> ast.Assign:
        return generate_assign(
            targets=[self._operation_str_variable],
            value=generate_call(
                func=generate_name(self._gql_func_name),
                args=[
                    [generate_constant(l + "\n") for l in operation_str.splitlines()]
                ],
            ),
            lineno=lineno,
        )

    def _generate_variables_assign(
        self, arguments_dict: ast.Dict, lineno: int = 1
    ) -> ast.AnnAssign:
        return generate_ann_assign(
            target=self._variables_dict_variable,
            annotation=generate_subscript(
                generate_name("dict"),
                generate_tuple([generate_name("str"), generate_name("object")]),
            ),
            value=arguments_dict,
            lineno=lineno,
        )

    def _generate_async_response_assign(self, lineno: int = 1) -> ast.Assign:
        return generate_assign(
            targets=[self._response_variable],
            value=generate_await(self._generate_execute_call()),
            lineno=lineno,
        )

    def _generate_response_assign(self, lineno: int = 1) -> ast.Assign:
        return generate_assign(
            targets=[self._response_variable],
            value=self._generate_execute_call(),
            lineno=lineno,
        )

    def _generate_execute_call(self) -> ast.Call:
        return generate_call(
            func=generate_attribute(generate_name("self"), "execute"),
            keywords=[
                generate_keyword("query", generate_name(self._operation_str_variable)),
                generate_keyword(
                    "variables", generate_name(self._variables_dict_variable)
                ),
            ],
        )

    def _generate_data_retrieval(self) -> ast.Assign:
        return generate_assign(
            targets=[self._data_variable],
            value=generate_call(
                func=generate_attribute(value=generate_name("self"), attr="get_data"),
                args=[generate_name(self._response_variable)],
            ),
        )

    def _generate_return_parsed_obj(self, return_type: str) -> ast.Return:
        return generate_return(
            generate_call(
                func=generate_attribute(generate_name(return_type), "parse_obj"),
                args=[generate_name(self._data_variable)],
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
