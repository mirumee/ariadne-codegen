import warnings
from pathlib import Path
from typing import cast

import pytest
from graphql import (
    GraphQLArgument,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLInputField,
    GraphQLInputObjectType,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
    GraphQLString,
    OperationDefinitionNode,
    parse,
)

from ariadne_codegen.client_generators import enums
from ariadne_codegen.client_generators.enums import EnumsGenerator
from ariadne_codegen.client_generators.input_types import InputTypesGenerator
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ..utils import filter_class_defs


def test_enum_generator_emits_deprecation_warning_for_deprecated_enum_value():
    """Generating enums that contain a deprecated value
    should emit DeprecationWarning."""
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

    with pytest.warns(DeprecationWarning) as records:
        EnumsGenerator(schema=schema).generate()

    assert [str(record.message) for record in records] == [
        "Enum value 'OLD' on enum 'Status' is deprecated: Use NEW instead."
    ]
    # stacklevel must point at generate(), not at the generator calling it
    assert Path(records[0].filename) == Path(enums.__file__)


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
    """Generating result types that select a deprecated field
    should emit DeprecationWarning."""
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


def test_enum_generator_emits_no_warning_for_enums_that_are_not_generated():
    """Generating a subgraph client from a whole graph's introspection must not
    report deprecated values of enums that are not generated."""
    used_enum = GraphQLEnumType(
        name="UsedStatus",
        values={"USED_OLD": GraphQLEnumValue(value="USED_OLD", deprecation_reason="x")},
    )
    unused_enum = GraphQLEnumType(
        name="UnusedStatus",
        values={
            "UNUSED_OLD": GraphQLEnumValue(value="UNUSED_OLD", deprecation_reason="y")
        },
    )
    schema = GraphQLSchema(types=[used_enum, unused_enum])

    with pytest.warns(DeprecationWarning) as records:
        EnumsGenerator(schema=schema).generate(types_to_include=["UsedStatus"])

    messages = [str(record.message) for record in records]
    assert messages == ["Enum value 'USED_OLD' on enum 'UsedStatus' is deprecated: x"]


def test_enum_generator_emits_no_warning_before_generate_is_called():
    """Parsing the schema must not warn on its own."""
    status_enum = GraphQLEnumType(
        name="Status",
        values={"OLD": GraphQLEnumValue(value="OLD", deprecation_reason="Use NEW.")},
    )
    schema = GraphQLSchema(types=[status_enum])

    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        EnumsGenerator(schema=schema)


def _query_with_deprecated_argument():
    return GraphQLSchema(
        query=GraphQLObjectType(
            name="Query",
            fields={
                "item": GraphQLField(
                    GraphQLNonNull(GraphQLString),
                    args={
                        "legacyId": GraphQLArgument(
                            GraphQLString, deprecation_reason="Use id."
                        ),
                        "id": GraphQLArgument(GraphQLString),
                    },
                )
            },
        )
    )


def _operation(query_str):
    return cast(OperationDefinitionNode, parse(query_str).definitions[0])


def test_result_types_generator_emits_deprecation_warning_for_deprecated_argument():
    """An operation passing a deprecated argument should emit DeprecationWarning."""
    # ResultTypesGenerator parses the operation in __init__, so it has to be built
    # inside the block.
    with pytest.warns(DeprecationWarning) as records:
        ResultTypesGenerator(
            schema=_query_with_deprecated_argument(),
            operation_definition=_operation('query TestQuery { item(legacyId: "1") }'),
            enums_module_name="enums",
        ).generate()

    assert [str(record.message) for record in records] == [
        "Argument 'legacyId' on field 'item' of type 'Query' is deprecated: Use id."
    ]


def test_result_types_generator_emits_no_warning_for_argument_that_is_not_passed():
    """Only the arguments an operation actually passes should be reported."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        ResultTypesGenerator(
            schema=_query_with_deprecated_argument(),
            operation_definition=_operation('query TestQuery { item(id: "1") }'),
            enums_module_name="enums",
        ).generate()


def _input_type(name, deprecated_field):
    return GraphQLInputObjectType(
        name=name,
        fields={
            deprecated_field: GraphQLInputField(
                GraphQLString, deprecation_reason="Use name."
            ),
            "name": GraphQLInputField(GraphQLString),
        },
    )


def test_input_types_generator_emits_deprecation_warning_for_deprecated_field():
    """Generating inputs that contain a deprecated field
    should emit DeprecationWarning."""
    schema = GraphQLSchema(types=[_input_type("ItemFilter", "oldName")])

    with pytest.warns(DeprecationWarning) as records:
        InputTypesGenerator(schema=schema).generate()

    assert [str(record.message) for record in records] == [
        "Input field 'oldName' on input 'ItemFilter' is deprecated: Use name."
    ]


def test_input_types_generator_emits_no_warning_for_inputs_that_are_not_generated():
    """With `include_all_inputs = false` the inputs no operation uses are not
    generated, so their deprecated fields must not be reported."""
    schema = GraphQLSchema(
        types=[
            _input_type("UsedFilter", "usedOldName"),
            _input_type("UnusedFilter", "unusedOldName"),
        ]
    )

    with pytest.warns(DeprecationWarning) as records:
        InputTypesGenerator(schema=schema).generate(types_to_include=["UsedFilter"])

    assert [str(record.message) for record in records] == [
        "Input field 'usedOldName' on input 'UsedFilter' is deprecated: Use name."
    ]
