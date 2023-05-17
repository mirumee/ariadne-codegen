import ast

from graphql import GraphQLSchema

from ariadne_codegen.contrib.shorter_results import ShorterResultsPlugin


def test_add_import():
    module = ast.parse(
        """
from foo import bar

class Client:
    pass
"""
    )

    plugin = ShorterResultsPlugin(GraphQLSchema(), {})
    plugin.extended_imports = {
        "foo": {"baz"},
    }

    updated = plugin.generate_client_module(module)
    alias_names = [x.name for x in updated.body[0].names]

    assert "baz" in alias_names
