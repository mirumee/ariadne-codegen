import ast
from typing import cast

from graphql import (
    OperationDefinitionNode,
    build_ast_schema,
    parse,
)

from ariadne_codegen.client_generators.constants import (
    ALIAS_KEYWORD,
    DEFAULT_KEYWORD,
    FIELD_CLASS,
    OPTIONAL,
)
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ...utils import compare_ast, format_graphql_str, get_class_def
from .schema import SCHEMA_STR


def test_default_optional_fields_true():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query1 {
                ... on CustomType {
                    field1
                    field2
                }
            }
        }
        """
    )
    expected_results = [
        ast.AnnAssign(
            target=ast.Name(id="field_1"),
            annotation=ast.Name(id='"CustomQueryQuery1Field1"'),
            value=ast.Call(
                func=ast.Name(id=FIELD_CLASS),
                args=[],
                keywords=[
                    ast.keyword(
                        arg=ALIAS_KEYWORD,
                        value=ast.Constant(value="field1"),
                    )
                ],
            ),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name(id="field_2"),
            annotation=ast.Subscript(
                value=ast.Name(id=OPTIONAL),
                slice=ast.Name(id='"CustomQueryQuery1Field2"'),
            ),
            value=ast.Call(
                func=ast.Name(id=FIELD_CLASS),
                args=[],
                keywords=[
                    ast.keyword(arg=ALIAS_KEYWORD, value=ast.Constant(value="field2")),
                    ast.keyword(arg=DEFAULT_KEYWORD, value=ast.Constant(value=None)),
                ],
            ),
            simple=1,
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        default_optional_fields_to_none=True,
    )
    result = generator.generate()
    classdef = get_class_def(result, 1)
    assert compare_ast(classdef.body[0], expected_results[0])
    assert compare_ast(classdef.body[1], expected_results[1])


def test_default_optional_fields_false():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query1 {
                ... on CustomType {
                    field1
                    field2
                }
            }
        }
        """
    )
    expected_results = [
        ast.AnnAssign(
            target=ast.Name(id="field_1"),
            annotation=ast.Name(id='"CustomQueryQuery1Field1"'),
            value=ast.Call(
                func=ast.Name(id=FIELD_CLASS),
                args=[],
                keywords=[
                    ast.keyword(
                        arg=ALIAS_KEYWORD,
                        value=ast.Constant(value="field1"),
                    )
                ],
            ),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name(id="field_2"),
            annotation=ast.Subscript(
                value=ast.Name(id=OPTIONAL),
                slice=ast.Name(id='"CustomQueryQuery1Field2"'),
            ),
            value=ast.Call(
                func=ast.Name(id=FIELD_CLASS),
                args=[],
                keywords=[
                    ast.keyword(arg=ALIAS_KEYWORD, value=ast.Constant(value="field2"))
                ],
            ),
            simple=1,
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        default_optional_fields_to_none=False,
    )
    result = generator.generate()
    classdef = get_class_def(result, 1)
    assert compare_ast(classdef.body[0], expected_results[0])
    assert compare_ast(classdef.body[1], expected_results[1])
