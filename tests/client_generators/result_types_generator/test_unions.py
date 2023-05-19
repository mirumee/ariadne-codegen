import ast
from typing import cast

from graphql import OperationDefinitionNode, build_ast_schema, parse

from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ...utils import compare_ast, filter_class_defs, format_graphql_str
from .schema import SCHEMA_STR


def test_generate_returns_module_with_handled_typename_field():
    query_str = """
    query CustomQuery {
        query2 {
            __typename
            id
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
    expected_fields_implementations = [
        ast.AnnAssign(
            target=ast.Name(id="typename__"),
            annotation=ast.Name(id="str"),
            value=ast.Call(
                func=ast.Name(id="Field"),
                args=[],
                keywords=[
                    ast.keyword(arg="alias", value=ast.Constant(value="__typename"))
                ],
            ),
            simple=1,
        ),
        ast.AnnAssign(
            target=ast.Name(id="id"),
            annotation=ast.Name(id="str"),
            simple=1,
        ),
    ]

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert len(class_defs) == 2
    assert class_defs[0].name == "CustomQuery"
    assert class_defs[1].name == "CustomQueryQuery2"
    assert compare_ast(class_defs[1].body, expected_fields_implementations)


def test_generate_returns_module_with_classes_for_union_fields():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query4 {
                ... on CustomType1 {
                    fielda
                }
                ... on CustomType2 {
                    fieldb
                }
            }
        }
        """
    )
    expected_classes_defs = [
        ast.ClassDef(
            name="CustomQuery",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="query4"),
                    annotation=ast.Subscript(
                        value=ast.Name(id="Union"),
                        slice=ast.Tuple(
                            elts=[
                                ast.Name(id='"CustomQueryQuery4CustomType1"'),
                                ast.Name(id='"CustomQueryQuery4CustomType2"'),
                            ],
                        ),
                    ),
                    simple=1,
                )
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="CustomQueryQuery4CustomType1",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="typename__"),
                    annotation=ast.Name(id="str"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="alias", value=ast.Constant(value="__typename")
                            )
                        ],
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="fielda"),
                    annotation=ast.Name(id="int"),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="CustomQueryQuery4CustomType2",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="typename__"),
                    annotation=ast.Name(id="str"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg="alias", value=ast.Constant(value="__typename")
                            )
                        ],
                    ),
                    simple=1,
                ),
                ast.AnnAssign(
                    target=ast.Name(id="fieldb"),
                    annotation=ast.Subscript(
                        value=ast.Name(id="Optional"),
                        slice=ast.Name(id="int"),
                    ),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
    ]

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
    )

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_classes_defs)
