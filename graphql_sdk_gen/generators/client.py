import ast

from .codegen import (
    generate_ann_assign,
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
    generate_trivial_lambda,
)
from .constants import OPTIONAL, TYPING_MODULE


class ClientGenerator:
    def __init__(self, name: str, base_client: str) -> None:
        self.name = name
        self.class_def = generate_class_def(name=name, base_names=[base_client])
        self.imports: list = [generate_import_from([OPTIONAL], TYPING_MODULE)]

        self._gql_lambda_name = "gql"
        self._operation_str_variable = "query"
        self._variables_dict_variable = "variables"
        self._response_variable = "response"
        self._data_variable = "data"

    def generate(self) -> ast.Module:
        """Generate module with class definistion of grahql client."""
        gql_lambda = generate_trivial_lambda(self._gql_lambda_name, "q")
        gql_lambda.lineno = len(self.imports) + 1
        self.class_def.lineno = len(self.imports) + 2
        if not self.class_def.body:
            self.class_def.body.append(ast.Pass())
        return ast.Module(
            body=self.imports + [gql_lambda, self.class_def],
            type_ignores=[],
        )

    def add_import(self, names: list[str], from_: str, level: int = 0) -> None:
        """Add import to be included in init file."""
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
        method_def = (
            self._generate_async_method(
                name=name,
                return_type=return_type,
                arguments=arguments,
                arguments_dict=arguments_dict,
                operation_str=operation_str,
            )
            if async_
            else self._generate_method(
                name=name,
                return_type=return_type,
                arguments=arguments,
                arguments_dict=arguments_dict,
                operation_str=operation_str,
            )
        )
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
                func=ast.Name(id=self._gql_lambda_name),
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
            annotation=generate_name("dict"),
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
