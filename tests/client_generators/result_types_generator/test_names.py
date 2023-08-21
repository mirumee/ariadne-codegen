import ast
from typing import cast

import pytest
from graphql import OperationDefinitionNode, build_ast_schema, parse

from ariadne_codegen.client_generators.constants import ALIAS_KEYWORD
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator
from ariadne_codegen.utils import ast_to_str

from ...utils import compare_ast, get_assignment_target_names, get_class_def
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
                ast.keyword(
                    arg=ALIAS_KEYWORD, value=ast.Constant(value="camelCaseQuery")
                )
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
        scalars_module_name="scalars",
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
                            arg=ALIAS_KEYWORD, value=ast.Constant(value="aliasedName")
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
        scalars_module_name="scalars",
        convert_to_snake_case=convert_to_snake_case,
    )

    module = generator.generate()

    class_def = get_class_def(module, 1)
    assert class_def.name == "CustomQueryCamelCaseQuery"
    assert len(class_def.body) == 1
    field_implementation = class_def.body[0]
    assert compare_ast(field_implementation, expected_field_implementation)


def test_generate_returns_module_with_valid_field_names():
    query_str = """
    query CustomQuery {
        camelCaseQuery {
            in: id
            _field4
            _Field5
            _
            schema
        }
    }
    """
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        scalars_module_name="scalars",
        convert_to_snake_case=True,
    )

    module = generator.generate()

    parsed = ast.parse(
        ast_to_str(module)
    )  # Round trip because invalid identifiers get picked up in parse
    class_def = get_class_def(parsed, name_filter="CustomQueryCamelCaseQuery")
    field_names = get_assignment_target_names(class_def)
    assert field_names == {
        "in_",
        "field4",
        "field5",
        "underscore_named_field_",
        "schema_",
    }
