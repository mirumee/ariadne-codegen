from collections.abc import Iterable

import pytest
from graphql import GraphQLSchema, build_schema

from ariadne_codegen.client_generators.custom_generator_utils import TypeCollector


@pytest.fixture()
def schema_with_interface_via_query() -> GraphQLSchema:
    sdl = """
    interface Produce {
      id: ID!
      name: String!
    }

    type Fruit implements Produce {
      id: ID!
      name: String!
    }

    type Vegetable implements Produce {
      id: ID!
      name: String!
      isPickled: Boolean
    }

    type Vendor {
      id: ID!
      availableProduce: [Produce]
    }

    type Query {
      vendor(id: ID!): Vendor
    }
    """
    return build_schema(sdl)


@pytest.fixture()
def schema_with_cycle() -> GraphQLSchema:
    sdl = """
    type Node {
      id: ID!
      children: [Node]
    }

    type Query {
      node: Node
    }
    """
    return build_schema(sdl)


@pytest.fixture()
def schema_with_union() -> GraphQLSchema:
    sdl = """
    interface Produce {
      id: ID!
      name: String!
    }

    type Fruit implements Produce {
      id: ID!
      name: String!
    }

    type Vegetable implements Produce {
      id: ID!
      name: String!
    }

    union SearchResult = Fruit | Vegetable

    type Query {
      search: [SearchResult]
    }
    """
    return build_schema(sdl)


@pytest.fixture()
def schema_with_query_and_mutation() -> GraphQLSchema:
    sdl = """
    type Vendor {
      id: ID!
    }

    type Query {
      vendor(id: ID!): Vendor
    }

    type Mutation {
      addVendor(id: ID!): Vendor
    }
    """
    return build_schema(sdl)


@pytest.fixture()
def schema_with_interface_only_via_mutation() -> GraphQLSchema:
    sdl = """
    interface Produce {
      id: ID!
      name: String!
    }

    type Fruit implements Produce {
      id: ID!
      name: String!
    }

    type MutationPayload {
      item: Produce
    }

    type Mutation {
      upsert: MutationPayload
    }

    type Query {
      _noop: String
    }
    """
    return build_schema(sdl)


def _assert_superset(actual: Iterable[str], expected_subset: set[str]) -> None:
    """
    Assert that 'actual' contains all elements of 'expected_subset', regardless of
    order or duplicates.
    """
    actual_set = set(actual)
    missing = expected_subset - actual_set
    assert not missing, f"Missing expected types: {sorted(missing)}"


def test_collect_returns_sorted_list(
    schema_with_interface_via_query: GraphQLSchema,
) -> None:
    """
    Test that the collected types are returned in sorted order.
    """
    types = TypeCollector(schema_with_interface_via_query).collect()
    assert types == sorted(types)


def test_collect_sample_schema_exact_types(
    schema_with_interface_via_query: GraphQLSchema,
) -> None:
    """
    Test that the collected types match the expected set of types for the sample schema.
    """
    assert TypeCollector(schema_with_interface_via_query).collect() == [
        "Fruit",
        "Produce",
        "Vegetable",
        "Vendor",
    ]


def test_collect_includes_interface_and_possible_types(
    schema_with_interface_via_query: GraphQLSchema,
) -> None:
    """
    Test that the collected types include both the interface and its possible types.
    """
    types = TypeCollector(schema_with_interface_via_query).collect()
    _assert_superset(types, {"Produce", "Fruit", "Vegetable"})


def test_collect_excludes_scalars(
    schema_with_interface_via_query: GraphQLSchema,
) -> None:
    """
    Test that scalar types are excluded from the collected types.
    """
    types = TypeCollector(schema_with_interface_via_query).collect()
    assert "ID" not in types
    assert "String" not in types
    assert "Boolean" not in types


def test_collect_recursion_guard_self_referential_type(
    schema_with_cycle: GraphQLSchema,
) -> None:
    """
    Test that the ``TypeCollector`` can handle self-referential types without infinite
    recursion.
    """
    assert TypeCollector(schema_with_cycle).collect() == ["Node"]


def test_collect_union_includes_union_and_members(
    schema_with_union: GraphQLSchema,
) -> None:
    """
    Test that the collected types include both the union type and its member types.
    """
    types = TypeCollector(schema_with_union).collect()
    _assert_superset(types, {"SearchResult", "Fruit", "Vegetable"})
    assert types == sorted(types)


def test_collect_includes_mutation_root_fields(
    schema_with_query_and_mutation: GraphQLSchema,
) -> None:
    """
    Test that the collected types include those reachable from both query and mutation
    roots.
    """
    assert TypeCollector(schema_with_query_and_mutation).collect() == ["Vendor"]


def test_collect_includes_interface_reachable_from_mutation_root(
    schema_with_interface_only_via_mutation: GraphQLSchema,
) -> None:
    """
    Test that the collected types include interfaces reachable from mutation root
    fields, even if they are not reachable from query root fields.
    """
    types = TypeCollector(schema_with_interface_only_via_mutation).collect()
    _assert_superset(types, {"Produce", "Fruit", "MutationPayload"})
