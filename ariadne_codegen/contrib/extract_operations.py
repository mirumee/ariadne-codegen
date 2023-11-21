import ast
from pathlib import Path
from typing import Dict, List, Union, cast

import isort
from black import Mode, format_str
from graphql import (
    ExecutableDefinitionNode,
    GraphQLSchema,
    NameNode,
    OperationDefinitionNode,
    OperationType,
)

from ariadne_codegen.client_generators.comments import get_comment
from ariadne_codegen.codegen import (
    generate_assign,
    generate_constant,
    generate_import_from,
    generate_list,
    generate_module,
    generate_name,
)
from ariadne_codegen.config import get_client_settings
from ariadne_codegen.plugins.base import Plugin
from ariadne_codegen.utils import format_multiline_strings, str_to_snake_case


class ExtractOperationsPlugin(Plugin):
    def __init__(self, schema: GraphQLSchema, config_dict: Dict) -> None:
        super().__init__(schema=schema, config_dict=config_dict)
        self.settings = get_client_settings(config_dict=self.config_dict)
        self.operations_module_name = (
            self.config_dict.get("tool", {})
            .get("ariadne-codegen", {})
            .get("extract-operations", {})
            .get("operations_module_name", "operations")
        )

        self._operations_gqls: Dict[str, str] = {}
        self._operations_variables: Dict[str, str] = {}

    def generate_init_module(self, module: ast.Module) -> ast.Module:
        if module.body:
            variables_names = list(self._operations_variables.values())
            module.body.insert(
                0,
                generate_import_from(
                    names=variables_names,
                    from_=self.operations_module_name,
                    level=1,
                ),
            )
            all_assign = cast(ast.Assign, module.body[-1])
            already_imported_names = [
                cast(ast.Constant, const).value
                for const in cast(ast.List, all_assign.value).elts
            ]
            cast(ast.List, all_assign.value).elts = [
                generate_constant(name)
                for name in sorted(already_imported_names + variables_names)
            ]

        self._generate_operations_module()
        return ast.fix_missing_locations(module)

    def generate_client_method(
        self,
        method_def: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        operation_definition: OperationDefinitionNode,
    ) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
        method_def.body = method_def.body[1:]
        if operation_definition.operation == OperationType.SUBSCRIPTION:
            call = cast(ast.AsyncFor, method_def.body[1]).iter
        elif self.settings.async_client:
            call = cast(ast.Await, cast(ast.Assign, method_def.body[1]).value).value
        else:
            call = cast(ast.Assign, method_def.body[1]).value

        for keyword in cast(ast.Call, call).keywords:
            if keyword.arg == "query":
                keyword.value = generate_name(
                    self._operations_variables[
                        cast(NameNode, operation_definition.name).value
                    ]
                )

        return ast.fix_missing_locations(method_def)

    def generate_operation_str(
        self, operation_str: str, operation_definition: ExecutableDefinitionNode
    ) -> str:
        operation_name = cast(NameNode, operation_definition.name).value
        self._operations_gqls[operation_name] = operation_str
        self._operations_variables[operation_name] = self._get_gql_variable_name(
            operation_name
        )
        return operation_str

    def generate_client_module(self, module: ast.Module) -> ast.Module:
        module.body.insert(
            0,
            generate_import_from(
                names=list(self._operations_variables.values()),
                from_=self.operations_module_name,
                level=1,
            ),
        )
        return ast.fix_missing_locations(module)

    def _get_gql_variable_name(self, operation_name: str) -> str:
        snake_case_name = str_to_snake_case(operation_name)
        return snake_case_name.upper() + "_GQL"

    def _generate_operations_module(self):
        module = self._get_operations_module()
        code = self._module_to_str(module)
        operations_path = (
            Path(self.settings.target_package_path)
            .joinpath(self.settings.target_package_name)
            .joinpath(f"{self.operations_module_name}.py")
        )
        operations_path.write_text(code, encoding="utf-8")

    def _get_operations_module(self) -> ast.Module:
        all_assign = generate_assign(
            targets=["__all__"],
            value=generate_list(
                [
                    generate_constant(name)
                    for name in sorted(self._operations_variables.values())
                ]
            ),
        )
        variables_assigns = [
            generate_assign(
                targets=[self._operations_variables[name]],
                value=[generate_constant(l + "\n") for l in gql.splitlines()],
            )
            for name, gql in self._operations_gqls.items()
        ]
        return generate_module(
            body=cast(List[ast.stmt], [all_assign] + variables_assigns)
        )

    def _module_to_str(self, module: ast.Module) -> str:
        code = ast.unparse(module)
        code_with_break_lines = "\n\n".join(code.splitlines())
        code_with_formatted_strings = format_multiline_strings(
            code_with_break_lines, offset=0
        )
        formatted_code = format_str(
            isort.code(code_with_formatted_strings), mode=Mode()
        )
        comment = get_comment(
            strategy=self.settings.include_comments, source=self.settings.queries_path
        )
        if comment:
            return comment + "\n\n" + formatted_code
        return formatted_code
