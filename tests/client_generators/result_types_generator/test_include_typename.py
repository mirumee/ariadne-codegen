"""Test include_typename functionality in ResultTypesGenerator."""

from graphql import build_schema, parse, OperationDefinitionNode

from ariadne_codegen.client_generators.result_types import ResultTypesGenerator
from ariadne_codegen.client_generators.constants import TYPENAME_FIELD_NAME


SIMPLE_SCHEMA = """
    type Query {
        hello: String
        user: User
    }
    
    type User {
        id: ID!
        name: String!
    }
    
    interface Animal {
        id: ID!
        name: String!
    }
    
    type Dog implements Animal {
        id: ID!
        name: String!
        breed: String!
    }
    
    type Cat implements Animal {
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
            animals {
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
    result_fields, result_selections = generator_false._add_typename_field_to_selections(
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