import ast
from typing import cast

from graphql import OperationDefinitionNode, build_ast_schema, parse

from ariadne_codegen.client_generators.constants import MODEL_REBUILD_METHOD
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ...utils import compare_ast
from .schema import SCHEMA_STR


def test_generate_returns_module_with_model_rebuild_calls():
    query_str = """
    query CustomQuery {
        query1 {
            field1 {
                fielda
            }
            field2 {
                fieldb
            }
        }
    }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    expected_class_names = [
        "CustomQuery",
        "CustomQueryQuery1",
        "CustomQueryQuery1Field1",
        "CustomQueryQuery1Field2",
    ]
    expected_method_calls = [
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(value=ast.Name(id=name), attr=MODEL_REBUILD_METHOD),
                args=[],
                keywords=[],
            )
        )
        for name in expected_class_names
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        enums_module_name="enums",
        scalars_module_name="scalars",
    )

    module = generator.generate()

    method_calls = list(filter(lambda x: isinstance(x, ast.Expr), module.body))
    assert compare_ast(method_calls, expected_method_calls)
