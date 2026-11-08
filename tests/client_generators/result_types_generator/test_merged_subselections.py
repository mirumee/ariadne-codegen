import ast

from graphql import (
    FragmentDefinitionNode,
    OperationDefinitionNode,
    build_schema,
    parse,
)

from ariadne_codegen.client_generators.constants import TYPENAME_ALIAS
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

SCHEMA = """
    type Query {
        foo: Foo
    }

    interface Node {
        id: ID!
    }

    interface Bar {
        id: ID!
        owner: User!
        contact: Node!
    }

    interface Baz {
        name: String!
        owner: User!
        contact: Node!
    }

    type Foo implements Bar & Baz {
        id: ID!
        name: String!
        owner: User!
        contact: Node!
    }

    type User implements Node {
        id: ID!
        name: String!
        email: String!
        profile: Profile!
    }

    type Profile {
        bio: String!
        avatar: String!
    }
"""


def _get_generator(query_str: str) -> ResultTypesGenerator:
    operation, *fragments = parse(query_str).definitions
    assert isinstance(operation, OperationDefinitionNode)
    return ResultTypesGenerator(
        schema=build_schema(SCHEMA),
        operation_definition=operation,
        enums_module_name="enums",
        fragments_definitions={
            fragment.name.value: fragment
            for fragment in fragments
            if isinstance(fragment, FragmentDefinitionNode)
        },
    )


def _get_field_names(generator: ResultTypesGenerator, class_name: str) -> list[str]:
    class_def = next(c for c in generator.get_classes() if c.name == class_name)
    return [
        node.target.id
        for node in class_def.body
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
    ]


def test_sub_selections_of_same_field_from_inline_fragments_are_merged():
    generator = _get_generator(
        """
        query GetFoo {
            foo {
                ... on Bar { owner { id } }
                ... on Baz { owner { name } }
            }
        }
        """
    )

    assert _get_field_names(generator, "GetFooFoo") == ["owner"]
    assert _get_field_names(generator, "GetFooFooOwner") == ["id", "name"]


def test_merged_sub_selections_are_deduplicated():
    generator = _get_generator(
        """
        query GetFoo {
            foo {
                ... on Bar { owner { id name } }
                ... on Baz { owner { name email } }
            }
        }
        """
    )

    assert _get_field_names(generator, "GetFooFooOwner") == ["id", "name", "email"]


def test_nested_sub_selections_are_merged():
    generator = _get_generator(
        """
        query GetFoo {
            foo {
                ... on Bar { owner { profile { bio } } }
                ... on Baz { owner { id profile { avatar } } }
            }
        }
        """
    )

    assert _get_field_names(generator, "GetFooFooOwner") == ["profile", "id"]
    assert _get_field_names(generator, "GetFooFooOwnerProfile") == ["bio", "avatar"]


def test_merged_sub_selections_of_field_from_fragment_spread_and_inline_fragment():
    generator = _get_generator(
        """
        query GetFoo {
            foo {
                ...BarOwner
                ... on Baz { owner { email } }
            }
        }

        fragment BarOwner on Bar {
            owner { id }
        }
        """
    )

    assert _get_field_names(generator, "GetFooFooOwner") == ["id", "email"]


def test_merged_sub_selections_of_abstract_field_request_typename():
    generator = _get_generator(
        """
        query GetFoo {
            foo {
                ... on Bar { contact { id } }
                ... on Baz { contact { ... on User { name } } }
            }
        }
        """
    )

    assert _get_field_names(generator, "GetFooFooContactNode") == [
        TYPENAME_ALIAS,
        "id",
    ]
    assert _get_field_names(generator, "GetFooFooContactUser") == [
        TYPENAME_ALIAS,
        "id",
        "name",
    ]
    assert "__typename" in generator.get_operation_as_str()
