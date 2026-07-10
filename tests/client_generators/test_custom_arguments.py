import ast

from graphql import build_schema

from ariadne_codegen.client_generators.custom_arguments import ArgumentGenerator
from ariadne_codegen.codegen import generate_import_from

from ..utils import compare_ast


def _expected_enum_import(name: str) -> ast.ImportFrom:
    """Matches generate_import_from for GraphQLEnumType in _parse_graphql_type_name."""
    return generate_import_from(names=[name], from_="enums", level=1)


def test_generate_arguments_records_enums_submodule_import_for_enum_field_argument():
    schema = build_schema(
        """
        schema { query: Query }
        enum Color { RED GREEN }
        type Query {
            paint(color: Color!): String
        }
        """
    )
    field = schema.query_type.fields["paint"]
    generator = ArgumentGenerator(custom_scalars={}, convert_to_snake_case=False)

    generator.generate_arguments(field.args)

    expected = _expected_enum_import("Color")
    assert len(generator.imports) == 1
    assert compare_ast(generator.imports[0], expected)


def test_generate_arguments_records_enums_submodule_import_for_list_of_enum_arguments():
    schema = build_schema(
        """
        schema { query: Query }
        enum SortOrder { ASC DESC }
        type Query {
            items(order: [SortOrder!]!): String
        }
        """
    )
    field = schema.query_type.fields["items"]
    generator = ArgumentGenerator(custom_scalars={}, convert_to_snake_case=False)

    generator.generate_arguments(field.args)

    expected = _expected_enum_import("SortOrder")
    assert len(generator.imports) == 1
    assert compare_ast(generator.imports[0], expected)


def test_generate_arguments_records_enums_submodule_import_for_optional_enum_argument():
    schema = build_schema(
        """
        schema { query: Query }
        enum Priority { LOW HIGH }
        type Query {
            task(priority: Priority): String
        }
        """
    )
    field = schema.query_type.fields["task"]
    generator = ArgumentGenerator(custom_scalars={}, convert_to_snake_case=False)

    generator.generate_arguments(field.args)

    expected = _expected_enum_import("Priority")
    assert len(generator.imports) == 1
    assert compare_ast(generator.imports[0], expected)
