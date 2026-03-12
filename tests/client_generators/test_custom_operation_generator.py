import ast

from graphql import build_schema

from ariadne_codegen.client_generators.arguments import ArgumentsGenerator
from ariadne_codegen.client_generators.custom_operation import CustomOperationGenerator

from ..utils import get_class_def


def _get_method_names(class_def: ast.ClassDef) -> list[str]:
    """Return names of methods (FunctionDef) in the class body."""
    return [node.name for node in class_def.body if isinstance(node, ast.FunctionDef)]


def test_reserved_word_as_operation_name_generates_suffixed_method():
    schema_str = """
    schema { query: Query }
    type Query {
        return(id: ID!): ReturnType
    }
    type ReturnType {
        id: ID!
        value: String
    }
    """
    schema = build_schema(schema_str)
    arguments_generator = ArgumentsGenerator(
        schema=schema,
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
    )
    generator = CustomOperationGenerator(
        graphql_fields=schema.query_type.fields,
        name="Query",
        base_name="GraphQLOperation",
        enums_module_name="enums",
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
        arguments_generator=arguments_generator,
    )
    module = generator.generate()
    query_class = get_class_def(module, name_filter="Query")
    assert query_class is not None
    method_names = _get_method_names(query_class)
    assert "return_" in method_names
    assert "return" not in method_names


def test_builtin_name_as_operation_name_generates_suffixed_method():
    schema_str = """
    schema { query: Query }
    type Query {
        str(id: ID!): StrType
    }
    type StrType {
        id: ID!
    }
    """
    schema = build_schema(schema_str)
    arguments_generator = ArgumentsGenerator(
        schema=schema,
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
    )
    generator = CustomOperationGenerator(
        graphql_fields=schema.query_type.fields,
        name="Query",
        base_name="GraphQLOperation",
        enums_module_name="enums",
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
        arguments_generator=arguments_generator,
    )
    module = generator.generate()
    query_class = get_class_def(module, name_filter="Query")
    assert query_class is not None
    method_names = _get_method_names(query_class)
    assert "str_" in method_names
    assert "str" not in method_names


def test_normal_operation_name_unchanged():
    schema_str = """
    schema { query: Query }
    type Query {
        getUser(id: ID!): User
    }
    type User {
        id: ID!
        name: String
    }
    """
    schema = build_schema(schema_str)
    arguments_generator = ArgumentsGenerator(
        schema=schema,
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
    )
    generator = CustomOperationGenerator(
        graphql_fields=schema.query_type.fields,
        name="Query",
        base_name="GraphQLOperation",
        enums_module_name="enums",
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
        arguments_generator=arguments_generator,
    )
    module = generator.generate()
    query_class = get_class_def(module, name_filter="Query")
    assert query_class is not None
    method_names = _get_method_names(query_class)
    assert "get_user" in method_names


def test_generated_module_formats_with_black():
    from ariadne_codegen.utils import ast_to_str

    schema_str = """
    schema { query: Query }
    type Query {
        return(id: ID!): ReturnType
    }
    type ReturnType {
        id: ID!
    }
    """
    schema = build_schema(schema_str)
    arguments_generator = ArgumentsGenerator(
        schema=schema,
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
    )
    generator = CustomOperationGenerator(
        graphql_fields=schema.query_type.fields,
        name="Query",
        base_name="GraphQLOperation",
        enums_module_name="enums",
        convert_to_snake_case=True,
        custom_scalars={},
        plugin_manager=None,
        arguments_generator=arguments_generator,
    )
    module = generator.generate()
    # Should not raise (e.g. Black InvalidInput for "def return(...)")
    code = ast_to_str(module)
    assert "def return_" in code
    assert "def return(" not in code
