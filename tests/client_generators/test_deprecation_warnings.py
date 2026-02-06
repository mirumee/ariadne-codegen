from typing import cast

import pytest
from graphql import (
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    OperationDefinitionNode,
    parse,
)

from ariadne_codegen.client_generators.enums import EnumsGenerator
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ..utils import filter_class_defs


def test_enum_generator_emits_deprecation_warning_for_deprecated_enum_value():
    """Generating enums that contain a deprecated value should emit DeprecationWarning."""
    status_enum = GraphQLEnumType(
        name="Status",
        values={
            "OLD": GraphQLEnumValue(
                value="OLD",
                deprecation_reason="Use NEW instead.",
            ),
            "NEW": GraphQLEnumValue(value="NEW"),
        },
    )
    schema = GraphQLSchema(types=[status_enum])

    # Warning is emitted during EnumsGenerator.__init__ when parsing enum defs
    with pytest.deprecated_call(
        match=r"Enum value 'OLD' on enum 'Status' is deprecated: Use NEW instead\."
    ):
        generator = EnumsGenerator(schema=schema)
        generator.generate()


def test_enum_generator_emits_no_warning_when_no_deprecated_values():
    """Generating enums with no deprecated values should not emit DeprecationWarning."""
    status_enum = GraphQLEnumType(
        name="Status",
        values={
            "A": GraphQLEnumValue(value="A"),
            "B": GraphQLEnumValue(value="B"),
        },
    )
    schema = GraphQLSchema(types=[status_enum])
    generator = EnumsGenerator(schema=schema)

    # Should complete without raising; no deprecation warning expected
    module = generator.generate()
    class_defs = filter_class_defs(module)
    assert len(class_defs) == 1
    assert class_defs[0].name == "Status"


def test_result_types_generator_emits_deprecation_warning_for_deprecated_field():
    """Generating result types that select a deprecated field should emit DeprecationWarning."""
    query_type = GraphQLObjectType(
        name="Query",
        fields={
            "oldField": GraphQLField(
                GraphQLNonNull(GraphQLString),
                deprecation_reason="Use newField instead.",
            ),
            "newField": GraphQLField(GraphQLNonNull(GraphQLString)),
        },
    )
    schema = GraphQLSchema(query=query_type)

    query_str = """
        query TestQuery {
            oldField
            newField
        }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )

    # Warning is emitted during ResultTypesGenerator.__init__ when parsing fields
    with pytest.deprecated_call(
        match=r"Field 'oldField' on type 'Query' is deprecated: Use newField instead\."
    ):
        generator = ResultTypesGenerator(
            schema=schema,
            operation_definition=operation_definition,
            enums_module_name="enums",
        )
        generator.generate()


def test_result_types_generator_emits_no_warning_when_no_deprecated_fields_selected():
    """Selecting only non-deprecated fields should not emit DeprecationWarning."""
    query_type = GraphQLObjectType(
        name="Query",
        fields={
            "oldField": GraphQLField(
                GraphQLNonNull(GraphQLString),
                deprecation_reason="Use newField instead.",
            ),
            "newField": GraphQLField(GraphQLNonNull(GraphQLString)),
        },
    )
    schema = GraphQLSchema(query=query_type)

    query_str = """
        query TestQuery {
            newField
        }
    """
    operation_definition = cast(
        OperationDefinitionNode, parse(query_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation_definition,
        enums_module_name="enums",
    )

    # Should complete without deprecation warning (we only selected newField)
    module = generator.generate()
    class_defs = filter_class_defs(module)
    assert len(class_defs) >= 1
    assert class_defs[0].name == "TestQuery"
