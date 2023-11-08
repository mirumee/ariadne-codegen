import ast
from pathlib import Path
from textwrap import dedent

import pytest
from graphql import parse, print_ast

from ariadne_codegen.contrib.extract_operations import ExtractOperationsPlugin

from ..utils import compare_ast


@pytest.fixture
def config_dict(tmp_path):
    schema_path = tmp_path / "schema.graphql"
    schema_path.touch()
    queries_path = tmp_path / "queries.graphql"
    queries_path.touch()
    generated_client_path = tmp_path / "generated_client"
    generated_client_path.mkdir()
    return {
        "tool": {
            "ariadne-codegen": {
                "schema_path": schema_path.as_posix(),
                "queries_path": queries_path.as_posix(),
                "target_package_path": tmp_path.as_posix(),
                "target_package_name": "generated_client",
                "include_comments": "none",
            }
        }
    }


@pytest.fixture
def empty_init_module():
    return ast.Module(
        body=[
            ast.Assign(targets=[ast.Name(id="__all__")], value=ast.List(elts=[])),
        ],
        type_ignores=[],
    )


@pytest.mark.parametrize(
    "config_update, name",
    [
        ({}, "operations"),
        (
            {"operations": {"operations_module_name": "custom_module_name"}},
            "custom_module_name",
        ),
    ],
)
def test_plugin_gets_module_name_from_config_dict(config_dict, config_update, name):
    dict_ = config_dict.copy()
    dict_["tool"]["ariadne-codegen"].update(config_update)

    assert (
        ExtractOperationsPlugin(schema=None, config_dict=dict_).operations_module_name
        == name
    )


def test_generate_init_module_returns_module_with_added_import(
    config_dict, empty_init_module
):
    node = parse("query testXyz { xyz }").definitions[0]
    plugin = ExtractOperationsPlugin(schema=None, config_dict=config_dict)
    plugin.generate_operation_str(print_ast(node), operation_definition=node)

    init_module = plugin.generate_init_module(empty_init_module)

    assert compare_ast(
        init_module,
        ast.Module(
            body=[
                ast.ImportFrom(
                    module="operations", names=[ast.alias(name="testXyz_GQL")], level=1
                ),
                ast.Assign(
                    targets=[ast.Name(id="__all__")],
                    value=ast.List(elts=[ast.Constant(value="testXyz_GQL")]),
                ),
            ],
            type_ignores=[],
        ),
    )


def test_generate_init_module_creates_operations_file(config_dict, empty_init_module):
    node = parse("query testXyz { xyz }").definitions[0]
    plugin = ExtractOperationsPlugin(schema=None, config_dict=config_dict)
    plugin.generate_operation_str(print_ast(node), operation_definition=node)

    plugin.generate_init_module(empty_init_module)

    operations_file_path = (
        Path(config_dict["tool"]["ariadne-codegen"]["target_package_path"])
        .joinpath(config_dict["tool"]["ariadne-codegen"]["target_package_name"])
        .joinpath("operations.py")
    )
    expected_content = '''
    testXyz_GQL = """
    query testXyz {
      xyz
    }
    """
    __all__ = ["testXyz_GQL"]
    '''
    with operations_file_path.open(encoding="utf-8") as file_:
        assert file_.read() == dedent(expected_content).lstrip()


def test_generate_client_method_returns_async_method_with_used_gql_variable(
    config_dict,
):
    node = parse("query testXyz { xyz }").definitions[0]
    plugin = ExtractOperationsPlugin(schema=None, config_dict=config_dict)
    plugin.generate_operation_str(print_ast(node), operation_definition=node)

    variables_assign = ast.AnnAssign(
        target=ast.Name(id="variables"),
        annotation=ast.Subscript(
            value=ast.Name(id="Dict"),
            slice=ast.Tuple(
                elts=[
                    ast.Name(id="str"),
                    ast.Name(id="object"),
                ]
            ),
        ),
        value=ast.Dict(keys=[], values=[]),
        simple=1,
    )
    data_assign = ast.Assign(
        targets=[ast.Name(id="data")],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="self"),
                attr="get_data",
            ),
            args=[ast.Name(id="response")],
            keywords=[],
        ),
    )
    return_stmt = (
        ast.Return(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="Bbb"), attr="model_validate"),
                args=[ast.Name(id="data")],
                keywords=[],
            )
        ),
    )
    method_def = ast.AsyncFunctionDef(
        name="bbb",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="self")],
            kwarg=ast.arg(arg="kwargs", annotation=ast.Name(id="Any")),
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[
            ast.Assign(
                targets=[ast.Name(id="query")],
                value=ast.Call(
                    func=ast.Name(id="gql"),
                    args=[ast.Constant(value=print_ast(node))],
                    keywords=[],
                ),
            ),
            variables_assign,
            ast.Assign(
                targets=[ast.Name(id="response")],
                value=ast.Await(
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id="self"), attr="execute"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="query",
                                value=ast.Name(id="query"),
                            ),
                            ast.keyword(
                                arg="variables",
                                value=ast.Name(id="variables"),
                            ),
                        ],
                    )
                ),
            ),
            data_assign,
            return_stmt,
        ],
        decorator_list=[],
        returns=ast.Name(id="Bbb"),
    )

    modified_method_def = plugin.generate_client_method(
        method_def, operation_definition=node
    )

    assert compare_ast(
        modified_method_def,
        ast.AsyncFunctionDef(
            name="bbb",
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="self")],
                kwarg=ast.arg(arg="kwargs", annotation=ast.Name(id="Any")),
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                variables_assign,
                ast.Assign(
                    targets=[ast.Name(id="response")],
                    value=ast.Await(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="self"), attr="execute"
                            ),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg="query",
                                    value=ast.Name(id="testXyz_GQL"),
                                ),
                                ast.keyword(
                                    arg="variables",
                                    value=ast.Name(id="variables"),
                                ),
                            ],
                        )
                    ),
                ),
                data_assign,
                return_stmt,
            ],
            decorator_list=[],
            returns=ast.Name(id="Bbb"),
        ),
    )


def test_generate_client_method_returns_method_with_used_gql_variable(
    config_dict,
):
    config_dict["tool"]["ariadne-codegen"]["async_client"] = False
    node = parse("query testXyz { xyz }").definitions[0]
    plugin = ExtractOperationsPlugin(schema=None, config_dict=config_dict)
    plugin.generate_operation_str(print_ast(node), operation_definition=node)

    variables_assign = ast.AnnAssign(
        target=ast.Name(id="variables"),
        annotation=ast.Subscript(
            value=ast.Name(id="Dict"),
            slice=ast.Tuple(
                elts=[
                    ast.Name(id="str"),
                    ast.Name(id="object"),
                ]
            ),
        ),
        value=ast.Dict(keys=[], values=[]),
        simple=1,
    )
    data_assign = ast.Assign(
        targets=[ast.Name(id="data")],
        value=ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="self"),
                attr="get_data",
            ),
            args=[ast.Name(id="response")],
            keywords=[],
        ),
    )
    return_stmt = (
        ast.Return(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="Bbb"), attr="model_validate"),
                args=[ast.Name(id="data")],
                keywords=[],
            )
        ),
    )
    method_def = ast.FunctionDef(
        name="bbb",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="self")],
            kwarg=ast.arg(arg="kwargs", annotation=ast.Name(id="Any")),
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[
            ast.Assign(
                targets=[ast.Name(id="query")],
                value=ast.Call(
                    func=ast.Name(id="gql"),
                    args=[ast.Constant(value=print_ast(node))],
                    keywords=[],
                ),
            ),
            variables_assign,
            ast.Assign(
                targets=[ast.Name(id="response")],
                value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id="self"), attr="execute"),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="query",
                            value=ast.Name(id="query"),
                        ),
                        ast.keyword(
                            arg="variables",
                            value=ast.Name(id="variables"),
                        ),
                    ],
                ),
            ),
            data_assign,
            return_stmt,
        ],
        decorator_list=[],
        returns=ast.Name(id="Bbb"),
    )

    modified_method_def = plugin.generate_client_method(
        method_def, operation_definition=node
    )

    assert compare_ast(
        modified_method_def,
        ast.FunctionDef(
            name="bbb",
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="self")],
                kwarg=ast.arg(arg="kwargs", annotation=ast.Name(id="Any")),
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                variables_assign,
                ast.Assign(
                    targets=[ast.Name(id="response")],
                    value=ast.Call(
                        func=ast.Attribute(value=ast.Name(id="self"), attr="execute"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="query",
                                value=ast.Name(id="testXyz_GQL"),
                            ),
                            ast.keyword(
                                arg="variables",
                                value=ast.Name(id="variables"),
                            ),
                        ],
                    ),
                ),
                data_assign,
                return_stmt,
            ],
            decorator_list=[],
            returns=ast.Name(id="Bbb"),
        ),
    )


def test_generate_client_method_returns_async_generator_with_used_gql_variable(
    config_dict,
):
    config_dict["tool"]["ariadne-codegen"]["async_client"] = False
    node = parse("subscription testXyz { xyz }").definitions[0]
    plugin = ExtractOperationsPlugin(schema=None, config_dict=config_dict)
    plugin.generate_operation_str(print_ast(node), operation_definition=node)

    variables_assign = ast.AnnAssign(
        target=ast.Name(id="variables"),
        annotation=ast.Subscript(
            value=ast.Name(id="Dict"),
            slice=ast.Tuple(elts=[ast.Name(id="str"), ast.Name(id="object")]),
        ),
        value=ast.Dict(keys=[], values=[]),
        simple=1,
    )
    for_body = [
        ast.Expr(
            value=ast.Yield(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="GetUsersCounter"),
                        attr="model_validate",
                    ),
                    args=[ast.Name(id="data")],
                    keywords=[],
                )
            )
        )
    ]
    method_def = ast.AsyncFunctionDef(
        name="get_users_counter",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="self")],
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=ast.arg(arg="kwargs", annotation=ast.Name(id="Any")),
            defaults=[],
        ),
        body=[
            ast.Assign(
                targets=[ast.Name(id="query")],
                value=ast.Call(
                    func=ast.Name(id="gql"),
                    args=[ast.Constant(value=print_ast(node))],
                    keywords=[],
                ),
            ),
            variables_assign,
            ast.AsyncFor(
                target=ast.Name(id="data"),
                iter=ast.Call(
                    func=ast.Attribute(value=ast.Name(id="self"), attr="execute_ws"),
                    args=[],
                    keywords=[
                        ast.keyword(arg="query", value=ast.Name(id="query")),
                        ast.keyword(arg="variables", value=ast.Name(id="variables")),
                        ast.keyword(value=ast.Name(id="kwargs")),
                    ],
                ),
                body=for_body,
                orelse=[],
            ),
        ],
        decorator_list=[],
        returns=ast.Subscript(
            value=ast.Name(id="AsyncIterator"), slice=ast.Name(id="GetUsersCounter")
        ),
    )

    modified_method_def = plugin.generate_client_method(
        method_def, operation_definition=node
    )

    assert compare_ast(
        modified_method_def,
        ast.AsyncFunctionDef(
            name="get_users_counter",
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="self")],
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=ast.arg(arg="kwargs", annotation=ast.Name(id="Any")),
                defaults=[],
            ),
            body=[
                variables_assign,
                ast.AsyncFor(
                    target=ast.Name(id="data"),
                    iter=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="self"), attr="execute_ws"
                        ),
                        args=[],
                        keywords=[
                            ast.keyword(arg="query", value=ast.Name(id="testXyz_GQL")),
                            ast.keyword(
                                arg="variables", value=ast.Name(id="variables")
                            ),
                            ast.keyword(value=ast.Name(id="kwargs")),
                        ],
                    ),
                    body=for_body,
                    orelse=[],
                ),
            ],
            decorator_list=[],
            returns=ast.Subscript(
                value=ast.Name(id="AsyncIterator"), slice=ast.Name(id="GetUsersCounter")
            ),
        ),
    )


def test_generate_client_module_adds_import_to_generated_module(config_dict):
    node = parse("query testXyz { xyz }").definitions[0]
    plugin = ExtractOperationsPlugin(schema=None, config_dict=config_dict)
    plugin.generate_operation_str(print_ast(node), operation_definition=node)

    module = plugin.generate_client_module(ast.Module(body=[], type_ignores=[]))

    assert compare_ast(
        module,
        ast.Module(
            body=[
                ast.ImportFrom(
                    module="operations", names=[ast.alias(name="testXyz_GQL")], level=1
                )
            ],
            type_ignores=[],
        ),
    )
