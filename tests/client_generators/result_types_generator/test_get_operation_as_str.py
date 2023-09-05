from typing import cast

from graphql import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
    build_ast_schema,
    parse,
)

from ariadne_codegen.client_generators.constants import MIXIN_NAME
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ...utils import format_graphql_str
from .schema import SCHEMA_STR


def test_get_operation_as_str_returns_str_with_added_typename():
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
    expected_result = format_graphql_str(
        """
        query CustomQuery {
            query4 {
                __typename
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
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        scalars_module_name="scalars",
    )

    result = generator.get_operation_as_str()

    assert result == expected_result


def test_get_operation_as_str_returns_str_with_used_fragments():
    query_str = format_graphql_str(
        """
        query CustomQuery {
            query2 {
                ...TestFragment1
                ...TestFragment2
                field2 {
                    fieldb
                }
            }
        }
        """
    )

    used_fragment1 = format_graphql_str(
        """
        fragment TestFragment1 on CustomType {
            id
        }
    """
    )

    used_fragment2 = format_graphql_str(
        """
        fragment TestFragment2 on CustomType {
            field1 {
                fielda
            }
        }
        """
    )

    not_used_fragment = format_graphql_str(
        """
        fragment TestFragment3 on CustomType {
            field2 {
                fieldb
            }
        }
        """
    )

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        scalars_module_name="scalars",
        fragments_definitions={
            "TestFragment1": cast(
                FragmentDefinitionNode, parse(used_fragment1).definitions[0]
            ),
            "TestFragment2": cast(
                FragmentDefinitionNode, parse(used_fragment2).definitions[0]
            ),
            "TestFragment3": cast(
                FragmentDefinitionNode, parse(not_used_fragment).definitions[0]
            ),
        },
    )

    result = generator.get_operation_as_str()

    assert query_str in result
    assert used_fragment1 in result
    assert used_fragment2 in result
    assert not_used_fragment not in result
    assert result.index(used_fragment1) < result.index(used_fragment2)


def test_get_operation_as_str_returns_str_with_fragment_used_by_another_fragment():
    query_str = "query CustomQuery { query2 { ...TestFragment } }"
    test_fragment_str = """
    fragment TestFragment on CustomType {
        id
        field2 {
            ...NestedFragment
        }
    }
    """
    nested_fragment_str = "fragment NestedFragment on CustomType2 { fieldb }"
    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        scalars_module_name="scalars",
        fragments_definitions={
            "TestFragment": cast(
                FragmentDefinitionNode, parse(test_fragment_str).definitions[0]
            ),
            "NestedFragment": cast(
                FragmentDefinitionNode, parse(nested_fragment_str).definitions[0]
            ),
        },
    )

    result = generator.get_operation_as_str()

    assert "fragment TestFragment on CustomType" in result
    assert "fragment NestedFragment on CustomType2" in result


def test_get_operation_as_str_returns_fragment_used_within_nested_inline_fragment():
    query_str = """
        query CustomQuery {
            query2 {
                id
                ...OuterFragment
            }
        }
    """
    outer_fragment = """
        fragment OuterFragment on CustomType {
            unionType {
                ... on CustomType1 {
                    ...InnerFragment1
                }
                ... on CustomType2 {
                    ...InnerFragment2
                }
            }
        }
    """
    inner_fragment1 = """
        fragment InnerFragment1 on CustomType1 {
            fielda
        }
    """
    inner_fragment2 = """
        fragment InnerFragment2 on CustomType2 {
            fieldb
        }
    """

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(query_str).definitions[0]
        ),
        enums_module_name="enums",
        scalars_module_name="scalars",
        fragments_definitions={
            "OuterFragment": cast(
                FragmentDefinitionNode, parse(outer_fragment).definitions[0]
            ),
            "InnerFragment1": cast(
                FragmentDefinitionNode, parse(inner_fragment1).definitions[0]
            ),
            "InnerFragment2": cast(
                FragmentDefinitionNode, parse(inner_fragment2).definitions[0]
            ),
        },
    )

    result = generator.get_operation_as_str()

    assert "fragment OuterFragment on CustomType" in result
    assert "fragment InnerFragment1 on CustomType1" in result
    assert "fragment InnerFragment2 on CustomType2" in result


def test_get_operation_as_str_returns_operation_without_mixin_directive():
    query_str = """
        query CustomQuery {
            query2 @mixin(from: ".mixins", import: "TestMixin") {
                id
                field1 @mixin(from: ".mixins", import: "TestMixin1") {
                    fielda
                }
                field2 @mixin(from: ".mixins", import: "TestMixin2") {
                    fieldb
                }
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
    )

    result = generator.get_operation_as_str()

    assert MIXIN_NAME not in result
    # tests that operation definition still contains mixin directive
    field_query2 = generator.operation_definition.selection_set.selections[0]
    field_field1 = field_query2.selection_set.selections[1]
    field_field2 = field_query2.selection_set.selections[2]
    assert field_query2.directives[0].name.value == MIXIN_NAME
    assert field_field1.directives[0].name.value == MIXIN_NAME
    assert field_field2.directives[0].name.value == MIXIN_NAME


def test_get_operation_as_str_returns_fragments_str_without_mixin_directive():
    operation_definition = """
        query CustomQuery {
            query2 @mixin(from: ".mixins", import: "TestMixin1") {
                ...TestFragment1
                ...TestFragment2
                field2 @mixin(from: ".mixins", import: "TestMixin2") {
                    fieldb
                }
            }
        }
        """
    fragment_without_mixin_str = """
        fragment TestFragment1 on CustomType {
            id 
        }
    """
    fragment_without_mixin = cast(
        FragmentDefinitionNode, parse(fragment_without_mixin_str).definitions[0]
    )
    fragment_with_mixin_str = """
        fragment TestFragment2 on CustomType {
            field1 @mixin(from: ".mixins", import: "TestMixin3") {
                fielda
            }
        }
        """
    fragment_with_mixin = cast(
        FragmentDefinitionNode, parse(fragment_with_mixin_str).definitions[0]
    )

    generator = ResultTypesGenerator(
        schema=build_ast_schema(parse(SCHEMA_STR)),
        operation_definition=cast(
            OperationDefinitionNode, parse(operation_definition).definitions[0]
        ),
        enums_module_name="enums",
        scalars_module_name="scalars",
        fragments_definitions={
            "TestFragment1": fragment_without_mixin,
            "TestFragment2": fragment_with_mixin,
        },
    )

    result = generator.get_operation_as_str()

    assert MIXIN_NAME not in result
    field_query2 = generator.operation_definition.selection_set.selections[0]
    field_field2 = field_query2.selection_set.selections[2]
    assert field_query2.directives[0].name.value == MIXIN_NAME
    assert field_field2.directives[0].name.value == MIXIN_NAME
    field_field1 = fragment_with_mixin.selection_set.selections[0]
    assert field_field1.directives[0].name.value == MIXIN_NAME
