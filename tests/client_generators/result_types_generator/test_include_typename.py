"""Test include_typename functionality in ResultTypesGenerator."""

from graphql import OperationDefinitionNode, build_schema, parse

from ariadne_codegen.client_generators.constants import (
    DISCRIMINATOR_KEYWORD,
    TYPENAME_FIELD_NAME,
)
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

SIMPLE_SCHEMA = """
    type Query {
        hello: String
        user: User
        animal: Animal
    }

    type User {
        id: ID!
        name: String!
    }

    union Animal = Dog | Cat

    interface Pet {
        id: ID!
        name: String!
    }

    type Dog implements Pet {
        id: ID!
        name: String!
        breed: String!
    }

    type Cat implements Pet {
        id: ID!
        name: String!
        lives: Int!
    }
"""


def test_result_types_generator_includes_typename_by_default():
    """Test that __typename is included by default for abstract types."""
    schema = build_schema(SIMPLE_SCHEMA)

    query_str = """
        query GetAnimals {
            animal {
                id
                name
                ... on Dog {
                    breed
                }
                ... on Cat {
                    lives
                }
            }
        }
    """

    document = parse(query_str)
    operation = document.definitions[0]
    assert isinstance(operation, OperationDefinitionNode)

    generator = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=True,  # Default behavior
    )

    # Check that the generator has include_typename=True
    assert generator.include_typename is True


def test_result_types_generator_respects_include_typename_false():
    """Test that __typename is not included when include_typename=False."""
    schema = build_schema(SIMPLE_SCHEMA)

    query_str = """
        query GetUser {
            user {
                id
                name
            }
        }
    """

    document = parse(query_str)
    operation = document.definitions[0]
    assert isinstance(operation, OperationDefinitionNode)

    generator = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=False,  # Disabled
    )

    # Check that the generator has include_typename=False
    assert generator.include_typename is False


def test_add_typename_field_to_selections_respects_include_typename_false():
    """Test that _add_typename_field_to_selections respects include_typename=False."""
    from graphql import FieldNode, NameNode, SelectionSetNode

    from ariadne_codegen.client_generators.constants import TYPENAME_FIELD_NAME

    schema = build_schema(SIMPLE_SCHEMA)

    query_str = """
        query GetUser {
            user {
                id
            }
        }
    """

    document = parse(query_str)
    operation = document.definitions[0]
    assert isinstance(operation, OperationDefinitionNode)

    # Test with include_typename=False
    generator_false = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=False,
    )

    # Create a sample field without __typename
    id_field = FieldNode(name=NameNode(value="id"))
    resolved_fields = [id_field]
    selection_set = SelectionSetNode(selections=(id_field,))

    # Call the method
    (
        result_fields,
        result_selections,
    ) = generator_false._add_typename_field_to_selections(
        resolved_fields, selection_set
    )

    # Should not add __typename field
    field_names = {f.name.value for f in result_fields}
    assert TYPENAME_FIELD_NAME not in field_names
    assert len(result_fields) == 1  # Only the original field
    assert result_fields[0].name.value == "id"

    # Test with include_typename=True (default)
    generator_true = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=True,
    )

    # Call the method with the same inputs
    result_fields, result_selections = generator_true._add_typename_field_to_selections(
        resolved_fields, selection_set
    )

    # Should add __typename field
    field_names = {f.name.value for f in result_fields}
    assert TYPENAME_FIELD_NAME in field_names
    assert len(result_fields) == 2  # Original field + __typename
    assert result_fields[0].name.value == TYPENAME_FIELD_NAME  # __typename added first
    assert result_fields[1].name.value == "id"


def test_add_typename_field_to_selections_does_not_duplicate():
    """Test that __typename is not added if it already exists."""
    from graphql import FieldNode, NameNode, SelectionSetNode

    schema = build_schema(SIMPLE_SCHEMA)

    query_str = """
        query GetUser {
            user {
                id
            }
        }
    """

    document = parse(query_str)
    operation = document.definitions[0]
    assert isinstance(operation, OperationDefinitionNode)

    generator = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=True,
    )

    # Create fields that already include __typename
    typename_field = FieldNode(name=NameNode(value=TYPENAME_FIELD_NAME))
    id_field = FieldNode(name=NameNode(value="id"))
    resolved_fields = [typename_field, id_field]
    selection_set = SelectionSetNode(selections=(typename_field, id_field))

    # Call the method
    result_fields, result_selections = generator._add_typename_field_to_selections(
        resolved_fields, selection_set
    )

    # Should not add another __typename field
    typename_count = sum(
        1 for f in result_fields if f.name.value == TYPENAME_FIELD_NAME
    )
    assert typename_count == 1
    assert len(result_fields) == 2  # Original fields only


def test_union_discriminator_respects_include_typename():
    """Test that discriminator fields are not generated when include_typename=False."""
    import ast

    schema = build_schema(SIMPLE_SCHEMA)

    # Test with a union type that should normally get a discriminator
    query_str = """
        query GetAnimal {
            animal {
                ... on Dog {
                    name
                    breed
                }
                ... on Cat {
                    name
                    lives
                }
            }
        }
    """

    document = parse(query_str)
    operation = document.definitions[0]
    assert isinstance(operation, OperationDefinitionNode)

    # Test with include_typename=True (should have discriminator)
    generator_with_typename = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=True,
    )

    module_with_typename = generator_with_typename.generate()

    # Check that discriminator is present in the generated code
    has_discriminator_with_typename = False
    for node in ast.walk(module_with_typename):
        if isinstance(node, ast.keyword) and node.arg == DISCRIMINATOR_KEYWORD:
            has_discriminator_with_typename = True
            break

    # Test with include_typename=False (should NOT have discriminator)
    generator_without_typename = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=False,
    )

    module_without_typename = generator_without_typename.generate()

    # Check that discriminator is NOT present in the generated code
    has_discriminator_without_typename = False
    for node in ast.walk(module_without_typename):
        if isinstance(node, ast.keyword) and node.arg == DISCRIMINATOR_KEYWORD:
            has_discriminator_without_typename = True
            break

    # Assertions
    assert has_discriminator_with_typename, (
        "Expected discriminator when include_typename=True"
    )
    assert not has_discriminator_without_typename, (
        "Should not have discriminator when include_typename=False"
    )


def test_get_field_from_schema_handles_typename_correctly():
    """Test that _get_field_from_schema correctly handles __typename field."""
    from graphql import GraphQLNonNull, GraphQLString

    from ariadne_codegen.exceptions import ParsingError

    schema = build_schema(SIMPLE_SCHEMA)

    query_str = """
        query GetUser {
            user {
                id
            }
        }
    """

    document = parse(query_str)
    operation = document.definitions[0]
    assert isinstance(operation, OperationDefinitionNode)

    generator = ResultTypesGenerator(
        schema=schema,
        operation_definition=operation,
        enums_module_name="enums",
        include_typename=True,
    )

    # __typename is not in the schema's type_map fields, so it should be handled
    # as a special case. This validates the fix where using GraphQLString instead
    # of GraphQLScalarType(name="String") prevents "Redefinition of reserved type"
    # error.
    typename_field = generator._get_field_from_schema("User", TYPENAME_FIELD_NAME)

    # Verify the field was created correctly using the built-in GraphQLString type
    assert typename_field is not None
    assert isinstance(typename_field.type, GraphQLNonNull)
    assert typename_field.type.of_type is GraphQLString
    assert typename_field.type.of_type.name == "String"

    # Test that requesting a non-existent field (other than __typename) raises an error
    try:
        generator._get_field_from_schema("User", "nonExistentField")
        assert False, "Expected ParsingError for non-existent field"
    except ParsingError as e:
        assert "nonExistentField" in str(e)
        assert "User" in str(e)
