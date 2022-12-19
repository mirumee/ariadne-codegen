import ast

from graphql import build_ast_schema, parse

from graphql_sdk_gen.generators.constants import UPDATE_FORWARD_REFS_METHOD
from graphql_sdk_gen.generators.input_types import InputTypesGenerator

from ...utils import compare_ast, filter_ast_objects


def test_generate_returns_modules_with_update_forward_refs_calls():
    schema_str = """
    input CustomInput {
        field: Int!
    }

    input TestInput {
        nested: NestedInput
    }

    input NestedInput {
        value: Int!
    }
    """
    expected_method_calls = [
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="CustomInput"), attr=UPDATE_FORWARD_REFS_METHOD
                ),
                args=[],
                keywords=[],
            )
        ),
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="NestedInput"), attr=UPDATE_FORWARD_REFS_METHOD
                ),
                args=[],
                keywords=[],
            )
        ),
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="TestInput"), attr=UPDATE_FORWARD_REFS_METHOD
                ),
                args=[],
                keywords=[],
            )
        ),
    ]
    generator = InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)), enums_module="enums"
    )

    module = generator.generate()

    method_calls = filter_ast_objects(module, ast.Expr)

    assert compare_ast(method_calls, expected_method_calls)
