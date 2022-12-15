import ast
from typing import cast

from graphql import OperationDefinitionNode, build_ast_schema, parse

from graphql_sdk_gen.generators.result_types import ResultTypesGenerator

from ...utils import compare_ast
from .schema import SCHEMA_STR


def test_generate_returns_module_with_enum_imports():
    query_str = """
    query CustomQuery {
        query2 {
            field3
        }
    }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=operation_definition,
        enums_module_name="enums",
    )

    module = generator.generate()

    assert isinstance(module, ast.Module)
    import_ = list(filter(lambda e: isinstance(e, ast.ImportFrom), module.body))[-1]
    assert compare_ast(
        import_,
        ast.ImportFrom(module="enums", names=[ast.alias("CustomEnum")], level=1),
    )
