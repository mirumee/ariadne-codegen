import ast
from typing import cast

import pytest
from graphql import GraphQLSchema, OperationDefinitionNode, build_schema, parse

from ariadne_codegen.client_generators.arguments import ArgumentsGenerator
from ariadne_codegen.client_generators.client import ClientGenerator
from ariadne_codegen.client_generators.constants import (
    ANY,
    ASYNC_ITERATOR,
    DICT,
    LIST,
    MODEL_VALIDATE_METHOD,
    OPTIONAL,
    TYPING_MODULE,
    UNION,
)
from ariadne_codegen.client_generators.scalars import ScalarData
from ariadne_codegen.exceptions import NotSupported

from ..utils import compare_ast, filter_imports, get_class_def, sorted_imports


def test_generate_returns_module_with_correct_class_name(
    async_base_client_import, unset_import, upload_import
):
    name = "ClientXyz"
    generator = ClientGenerator(
        name,
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=GraphQLSchema()),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )

    module = generator.generate()
    class_def = get_class_def(module)

    assert class_def
    assert class_def.name == name


def test_generate_returns_module_with_gql_lambda_definition(
    async_base_client_import, unset_import, upload_import
):
    generator = ClientGenerator(
        "ClientXYZ",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=GraphQLSchema()),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )
    expected_def = ast.FunctionDef(
        name="gql",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="q", annotation=ast.Name(id="str"))],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[ast.Return(value=ast.Name(id="q"))],
        returns=ast.Name(id="str"),
        decorator_list=[],
    )

    module = generator.generate()

    assign = next(
        filter(lambda expr: isinstance(expr, ast.FunctionDef), module.body), None
    )
    assert assign
    assert compare_ast(assign, expected_def)


def test_generate_triggers_generate_gql_function_hook(
    mocked_plugin_manager, async_base_client_import, unset_import, upload_import
):
    generator = ClientGenerator(
        "ClientXYZ",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=GraphQLSchema()),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
        plugin_manager=mocked_plugin_manager,
    )

    generator.generate()

    assert mocked_plugin_manager.generate_gql_function.called


def test_generate_triggers_generate_client_class_hook(
    mocked_plugin_manager, async_base_client_import, unset_import, upload_import
):
    generator = ClientGenerator(
        "ClientXYZ",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=GraphQLSchema()),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
        plugin_manager=mocked_plugin_manager,
    )
    generator.generate()

    assert mocked_plugin_manager.generate_client_class.called


def test_generate_triggers_generate_client_module_hook(
    mocked_plugin_manager, async_base_client_import, unset_import, upload_import
):
    generator = ClientGenerator(
        "ClientXYZ",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=GraphQLSchema()),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
        plugin_manager=mocked_plugin_manager,
    )

    generator.generate()

    assert mocked_plugin_manager.generate_client_module.called


def test_generate_returns_module_with_correct_imports(
    async_base_client_import, unset_import, upload_import
):
    schema_str = """
    schema { query: Query }
    type Query { xyz(arg1: TestScalar!, arg2: TestEnum!, arg3: TestInput): TestType }
    type TestType {
        id: ID!
        name: String!
    }
    enum TestEnum {
        A
        B
    }
    input TestInput {
        value: String
    }
    scalar TestScalar
    """
    query_str = """
    query ListXyz($arg1: TestScalar!, $arg2: TestEnum!, $arg3: TestInput) {
        xyz(arg1: $arg1, arg2: $arg2, arg3: $arg3) {
            id
            name
        }
    }
    """
    scalars = {"TestScalar": ScalarData(type_="str")}
    generator = ClientGenerator(
        "Client",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(
            schema=build_schema(schema_str), custom_scalars=scalars
        ),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
        custom_scalars=scalars,
    )
    expected_imports = [
        async_base_client_import,
        unset_import,
        upload_import,
        ast.ImportFrom(module="enums", names=[ast.alias(name="TestEnum")], level=1),
        ast.ImportFrom(module="inputs", names=[ast.alias(name="TestInput")], level=1),
        ast.ImportFrom(module="list_xyz", names=[ast.alias(name="ListXyz")], level=1),
        ast.ImportFrom(
            module=TYPING_MODULE,
            names=[
                ast.alias(name=OPTIONAL),
                ast.alias(name=LIST),
                ast.alias(name=DICT),
                ast.alias(name=ANY),
                ast.alias(name=UNION),
                ast.alias(name=ASYNC_ITERATOR),
            ],
            level=0,
        ),
    ]

    generator.add_method(
        definition=cast(OperationDefinitionNode, parse(query_str).definitions[0]),
        name="list_xyz",
        return_type="ListXyz",
        return_type_module="list_xyz",
        operation_str=query_str,
        async_=True,
    )
    module = generator.generate()

    assert compare_ast(
        sorted_imports(filter_imports(module)), sorted_imports(expected_imports)
    )


def test_add_method_adds_async_method_definition(
    async_base_client_import, unset_import, upload_import
):
    generator = ClientGenerator(
        "ClientXYZ",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=GraphQLSchema()),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )
    method_name = "list_xyz"
    return_type = "ListXyz"
    return_type_module_name = method_name

    generator.add_method(
        definition=OperationDefinitionNode(variable_definitions=()),
        name=method_name,
        return_type=return_type,
        return_type_module=return_type_module_name,
        operation_str="",
        async_=True,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]

    assert isinstance(method_def, ast.AsyncFunctionDef)
    assert method_def.name == method_name
    assert isinstance(method_def.returns, ast.Name)
    assert method_def.returns.id == return_type


def test_add_method_generates_correct_async_method_body(
    async_base_client_import, unset_import, upload_import
):
    schema_str = """
    schema { query: Query }
    type Query { xyz(arg1: Int!): TestType }
    type TestType {
        id: ID!
        name: String!
    }
    """
    query_str = """
    query ListXyz($arg1: Int!) {
        xyz(arg1: $arg1) {
            id
            name
        }
    }
    """
    generator = ClientGenerator(
        "Client",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=build_schema(schema_str)),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )
    method_name = "list_xyz"
    return_type = "ListXyz"
    return_type_module_name = method_name
    expected_method_body = [
        ast.Assign(
            targets=[ast.Name(id="query")],
            value=ast.Call(
                func=ast.Name("gql"),
                keywords=[],
                args=[[ast.Constant(value=l + "\n") for l in query_str.splitlines()]],
            ),
        ),
        ast.AnnAssign(
            target=ast.Name(id="variables"),
            annotation=ast.Subscript(
                value=ast.Name(id="Dict"),
                slice=ast.Tuple(elts=[ast.Name(id="str"), ast.Name(id="object")]),
            ),
            value=ast.Dict(
                keys=[ast.Constant(value="arg1")], values=[ast.Name(id="arg1")]
            ),
            simple=1,
        ),
        ast.Assign(
            targets=[ast.Name(id="response")],
            value=ast.Await(
                value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id="self"), attr="execute"),
                    args=[],
                    keywords=[
                        ast.keyword(arg="query", value=ast.Name(id="query")),
                        ast.keyword(arg="variables", value=ast.Name(id="variables")),
                    ],
                )
            ),
        ),
        ast.Assign(
            targets=[ast.Name(id="data")],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="self"), attr="get_data"),
                args=[ast.Name(id="response")],
                keywords=[],
            ),
        ),
        ast.Return(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="ListXyz"), attr=MODEL_VALIDATE_METHOD
                ),
                args=[ast.Name(id="data")],
                keywords=[],
            )
        ),
    ]

    generator.add_method(
        definition=cast(OperationDefinitionNode, parse(query_str).definitions[0]),
        name=method_name,
        return_type=return_type,
        return_type_module=return_type_module_name,
        operation_str=query_str,
        async_=True,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]
    assert isinstance(method_def, ast.AsyncFunctionDef)
    assert compare_ast(method_def.body, expected_method_body)


def test_add_method_adds_method_definition(
    unset_import, upload_import, base_client_import
):
    schema_str = """
    schema { query: Query }
    type Query { xyz(arg1: Int!): TestType }
    type TestType {
        id: ID!
        name: String!
    }
    """
    query_str = """
    query ListXyz($arg1: Int!) {
        xyz(arg1: $arg1) {
            id
            name
        }
    }
    """
    generator = ClientGenerator(
        "Client",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=build_schema(schema_str)),
        base_client_import=base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )
    method_name = "list_xyz"
    return_type = "ListXyz"
    return_type_module_name = method_name

    generator.add_method(
        definition=cast(OperationDefinitionNode, parse(query_str).definitions[0]),
        name=method_name,
        return_type=return_type,
        return_type_module=return_type_module_name,
        operation_str=query_str,
        async_=False,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]

    assert isinstance(method_def, ast.FunctionDef)
    assert method_def.name == method_name
    assert isinstance(method_def.returns, ast.Name)
    assert method_def.returns.id == return_type


def test_add_method_generates_correct_method_body(
    unset_import, upload_import, base_client_import
):
    schema_str = """
    schema { query: Query }
    type Query { xyz(arg1: Int!): TestType }
    type TestType {
        id: ID!
        name: String!
    }
    """
    query_str = """
    query ListXyz($arg1: Int!) {
        xyz(arg1: $arg1) {
            id
            name
        }
    }
    """
    generator = ClientGenerator(
        "Client",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=build_schema(schema_str)),
        base_client_import=base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )
    method_name = "list_xyz"
    return_type = "ListXyz"
    return_type_module_name = method_name
    expected_method_body = [
        ast.Assign(
            targets=[ast.Name(id="query")],
            value=ast.Call(
                func=ast.Name("gql"),
                keywords=[],
                args=[[ast.Constant(value=l + "\n") for l in query_str.splitlines()]],
            ),
        ),
        ast.AnnAssign(
            target=ast.Name(id="variables"),
            annotation=ast.Subscript(
                value=ast.Name(id="Dict"),
                slice=ast.Tuple(elts=[ast.Name(id="str"), ast.Name(id="object")]),
            ),
            value=ast.Dict(
                keys=[ast.Constant(value="arg1")], values=[ast.Name(id="arg1")]
            ),
            simple=1,
        ),
        ast.Assign(
            targets=[ast.Name(id="response")],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="self"), attr="execute"),
                args=[],
                keywords=[
                    ast.keyword(arg="query", value=ast.Name(id="query")),
                    ast.keyword(arg="variables", value=ast.Name(id="variables")),
                ],
            ),
        ),
        ast.Assign(
            targets=[ast.Name(id="data")],
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id="self"), attr="get_data"),
                args=[ast.Name(id="response")],
                keywords=[],
            ),
        ),
        ast.Return(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="ListXyz"), attr=MODEL_VALIDATE_METHOD
                ),
                args=[ast.Name(id="data")],
                keywords=[],
            )
        ),
    ]

    generator.add_method(
        definition=cast(OperationDefinitionNode, parse(query_str).definitions[0]),
        name=method_name,
        return_type=return_type,
        return_type_module=return_type_module_name,
        operation_str=query_str,
        async_=False,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    method_def = class_def.body[0]
    assert isinstance(method_def, ast.FunctionDef)
    assert compare_ast(method_def.body, expected_method_body)


def test_add_method_generates_async_generator_for_subscription_definition(
    async_base_client_import, unset_import, upload_import
):
    schema_str = """
    schema { subscription: Subscription }
    type Subscription { counter: Int! }
    """
    subscription_str = "subscription GetCounter { counter }"
    generator = ClientGenerator(
        "ClientXYZ",
        base_client="AsyncBaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=build_schema(schema_str)),
        base_client_import=async_base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )
    expected_method_def = ast.AsyncFunctionDef(
        name="get_counter",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg="self")],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[
            ast.Assign(
                targets=[ast.Name(id="query")],
                value=ast.Call(
                    func=ast.Name(id="gql"),
                    args=[
                        [ast.Constant(value="subscription GetCounter { counter }\n")]
                    ],
                    keywords=[],
                ),
            ),
            ast.AnnAssign(
                target=ast.Name(id="variables"),
                annotation=ast.Subscript(
                    value=ast.Name(id="Dict"),
                    slice=ast.Tuple(elts=[ast.Name(id="str"), ast.Name(id="object")]),
                ),
                value=ast.Dict(keys=[], values=[]),
                simple=1,
            ),
            ast.AsyncFor(
                target=ast.Name(id="data"),
                iter=ast.Call(
                    func=ast.Attribute(value=ast.Name(id="self"), attr="execute_ws"),
                    args=[],
                    keywords=[
                        ast.keyword(arg="query", value=ast.Name(id="query")),
                        ast.keyword(arg="variables", value=ast.Name(id="variables")),
                    ],
                ),
                body=[
                    ast.Expr(
                        value=ast.Yield(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id="GetCounter"),
                                    attr=MODEL_VALIDATE_METHOD,
                                ),
                                args=[ast.Name(id="data")],
                                keywords=[],
                            )
                        )
                    )
                ],
                orelse=[],
            ),
        ],
        decorator_list=[],
        returns=ast.Subscript(
            value=ast.Name(id="AsyncIterator"), slice=ast.Name(id="GetCounter")
        ),
    )

    generator.add_method(
        definition=cast(
            OperationDefinitionNode, parse(subscription_str).definitions[0]
        ),
        name="get_counter",
        return_type="GetCounter",
        return_type_module="get_counter",
        operation_str=subscription_str,
        async_=True,
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def
    assert compare_ast(class_def.body[0], expected_method_def)


def test_add_method_raises_not_supported_for_not_async_subscription(
    unset_import, upload_import, base_client_import
):
    subscription_str = "subscription GetCounter { counter }"
    generator = ClientGenerator(
        "Client",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(GraphQLSchema()),
        base_client_import=base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
    )

    with pytest.raises(NotSupported):
        generator.add_method(
            definition=cast(
                OperationDefinitionNode, parse(subscription_str).definitions[0]
            ),
            name="list_xyz",
            return_type="ListXyz",
            return_type_module="list_xyz",
            operation_str="",
            async_=False,
        )


def test_add_method_triggers_generate_client_method_hook(
    mocked_plugin_manager, unset_import, upload_import, base_client_import
):
    schema_str = """
    schema { query: Query }
    type Query { xyz(arg1: Int!): TestType }
    type TestType {
        id: ID!
        name: String!
    }
    """
    query_str = """
    query ListXyz($arg1: Int!) {
        xyz(arg1: $arg1) {
            id
            name
        }
    }
    """
    generator = ClientGenerator(
        "Client",
        base_client="BaseClient",
        enums_module_name="enums",
        input_types_module_name="inputs",
        arguments_generator=ArgumentsGenerator(schema=build_schema(schema_str)),
        base_client_import=base_client_import,
        unset_import=unset_import,
        upload_import=upload_import,
        plugin_manager=mocked_plugin_manager,
    )
    method_name = "list_xyz"
    return_type = "ListXyz"
    return_type_module_name = method_name

    generator.add_method(
        definition=cast(OperationDefinitionNode, parse(query_str).definitions[0]),
        name=method_name,
        return_type=return_type,
        return_type_module=return_type_module_name,
        operation_str=query_str,
        async_=False,
    )
    generator.generate()

    assert mocked_plugin_manager.generate_client_method.called
