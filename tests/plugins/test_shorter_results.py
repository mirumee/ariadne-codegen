import ast
from graphql import GraphQLSchema

from ariadne_codegen.plugins import shorter_results


def test_add_import():
    module = ast.parse("from foo import bar")

    plugin = shorter_results.ShorterResultsPlugin(GraphQLSchema(), {})
    plugin.extended_imports = {
        "foo": {"baz"},
    }

    updated = plugin.generate_client_module(module)
    alias_names = [x.name for x in updated.body[0].names]

    assert "baz" in alias_names
