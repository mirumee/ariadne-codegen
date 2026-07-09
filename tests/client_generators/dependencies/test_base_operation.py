from graphql import print_ast

from ariadne_codegen.client_generators.dependencies.base_operation import (
    GraphQLField,
    GraphQLLeafField,
)


class ProductGraphQLField(GraphQLField):
    pass


class ProductFields(GraphQLField):
    id = GraphQLLeafField("id", ProductGraphQLField)
    name = GraphQLLeafField("name", ProductGraphQLField)


def test_leaf_field_builds_the_declared_field():
    field = ProductFields.name

    assert isinstance(field, ProductGraphQLField)
    assert print_ast(field.to_ast(0)) == "name"


def test_leaf_field_returns_a_new_instance_on_every_access():
    assert ProductFields.name is not ProductFields.name


def test_leaf_field_alias_does_not_leak_into_later_queries():
    """A shared class attribute would carry one query's alias into the next."""
    aliased = ProductFields.name.alias("nick")
    assert print_ast(aliased.to_ast(0)) == "nick: name"

    later_query = ProductFields.name
    assert later_query._alias is None
    assert print_ast(later_query.to_ast(0)) == "name"


def test_leaf_field_subfields_do_not_leak_into_later_queries():
    ProductFields.id._subfields.append(ProductFields.name)

    assert ProductFields.id._subfields == []


def test_leaf_field_is_accessible_from_an_instance():
    instance = ProductFields("product")

    assert isinstance(instance.name, ProductGraphQLField)
