import ast
from typing import cast

from graphql import OperationDefinitionNode, build_ast_schema, parse

from graphql_sdk_gen.generators.result_types import ResultTypesGenerator

from ...utils import compare_ast, get_class_def
from .schema import SCHEMA_STR


def test_generate_returns_module_with_query_names_converted_to_snake_case():
    query_str = """
    query CustomQuery {
        camelCaseQuery {
            id
        }
    }
    """
    expected_field_implementation = ast.AnnAssign(
        target=ast.Name(id="camel_case_query"),
        annotation=ast.Name(id='"CustomQueryCamelCaseQuery"'),
        value=ast.Call(
            func=ast.Name(id="Field"),
            args=[],
            keywords=[
                ast.keyword(arg="alias", value=ast.Constant(value="camelCaseQuery"))
            ],
        ),
        simple=1,
    )

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_def = get_class_def(module)
    assert class_def.name == "CustomQuery"
    assert len(class_def.body) == 1
    field_implementation = class_def.body[0]
    assert compare_ast(field_implementation, expected_field_implementation)
