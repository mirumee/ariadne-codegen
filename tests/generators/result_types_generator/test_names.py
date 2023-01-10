import ast
from typing import cast

import pytest
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


@pytest.mark.parametrize(
    "convert_to_snake_case, expected_field_implementation",
    [
        (
            False,
            ast.AnnAssign(
                target=ast.Name(id="aliasedName"),
                annotation=ast.Name(id="str"),
                simple=1,
            ),
        ),
        (
            True,
            ast.AnnAssign(
                target=ast.Name(id="aliased_name"),
                annotation=ast.Name(id="str"),
                value=ast.Call(
                    func=ast.Name(id="Field"),
                    args=[],
                    keywords=[
                        ast.keyword(
                            arg="alias", value=ast.Constant(value="aliasedName")
                        )
                    ],
                ),
                simple=1,
            ),
        ),
    ],
)
def test_generate_returns_module_with_handled_graphql_alias(
    convert_to_snake_case, expected_field_implementation
):
    query_str = """
    query CustomQuery {
        camelCaseQuery {
            aliasedName: id
        }
    }
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        convert_to_snake_case=convert_to_snake_case,
    )

    module = generator.generate()

    class_def = get_class_def(module, 1)
    assert class_def.name == "CustomQueryCamelCaseQuery"
    assert len(class_def.body) == 1
    field_implementation = class_def.body[0]
    assert compare_ast(field_implementation, expected_field_implementation)
