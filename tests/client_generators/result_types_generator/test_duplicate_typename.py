import ast

import pytest
from graphql import OperationDefinitionNode, build_schema, parse

from ariadne_codegen.client_generators.constants import TYPENAME_ALIAS
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

SCHEMA = """
    type Query {
        foo: Foo
    }

    interface Bar {
        id: ID!
    }

    interface Baz {
        name: String!
    }

    type Foo implements Bar & Baz {
        id: ID!
        name: String!
    }
"""


@pytest.mark.xfail(reason="Codegen emits duplicate typename__ for multi-interface types")
def test_no_duplicate_typename_when_type_implements_multiple_interfaces():
    schema = build_schema(SCHEMA)

    query_str = """
        query GetFoo {
            foo {
                ... on Bar {
                    __typename
                    id
                }
                ... on Baz {
                    __typename
                    name
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
    )

    class_defs = generator.get_classes()
    foo_class = next(c for c in class_defs if c.name == "GetFooFoo")

    typename_fields = [
        node
        for node in foo_class.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == TYPENAME_ALIAS
    ]

    assert len(typename_fields) == 1
