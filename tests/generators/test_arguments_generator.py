import ast

from graphql import GraphQLSchema, OperationDefinitionNode, build_schema, parse

from ariadne_codegen.generators.arguments import ArgumentsGenerator
from ariadne_codegen.generators.constants import ANY, OPTIONAL

from ..utils import compare_ast


def _get_variable_definitions_from_query_str(query: str):
    document_node = parse(query)
    operation_definition = document_node.definitions[0]
    assert isinstance(operation_definition, OperationDefinitionNode)
    return operation_definition.variable_definitions


def test_generate_returns_arguments_with_correct_non_optional_names_and_annotations():
    schema_str = """
    schema { query: Query }
    type Query { _skip: ID! }

    input CustomInputType {
        fieldA: Int!
        fieldB: Float!
        fieldC: String!
        fieldD: Boolean!
    }
    """
    schema = build_schema(schema_str)
    generator = ArgumentsGenerator(schema=schema)
    query = (
        "query q($id: ID!, $name: String!, $amount: Int!, $val: Float!, "
        "$flag: Boolean!, $custom_input: CustomInputType!) {r}"
    )
    expected_names = ["self", "id", "name", "amount", "val", "flag", "custom_input"]
    expected_annotations = [
        None,
        "str",
        "str",
        "int",
        "float",
        "bool",
        "CustomInputType",
    ]
    variable_definitions = _get_variable_definitions_from_query_str(query)

    arguments, _ = generator.generate(variable_definitions)

    assert isinstance(arguments, ast.arguments)
    names = [a.arg for a in arguments.args]
    annotations = [a.annotation.id if a.annotation else None for a in arguments.args]
    assert names == expected_names
    assert annotations == expected_annotations


def test_generate_returns_arguments_with_correct_optional_annotation():
    schema_str = """
        schema { query: Query }
        type Query { _skip: ID! }
        """
    schema = build_schema(schema_str)
    generator = ArgumentsGenerator(schema=schema)
    query = "query q($id: ID) {r}"
    variable_definitions = _get_variable_definitions_from_query_str(query)

    arguments, _ = generator.generate(variable_definitions)

    assert isinstance(arguments, ast.arguments)
    assert len(arguments.args) == 2
    id_arg = arguments.args[1]
    assert id_arg.arg == "id"
    assert id_arg.annotation
    assert isinstance(id_arg.annotation, ast.Subscript)
    assert isinstance(id_arg.annotation.value, ast.Name)
    assert id_arg.annotation.value.id == OPTIONAL
    assert isinstance(id_arg.annotation.slice, ast.Name)
    assert id_arg.annotation.slice.id == "str"


def test_generate_returns_arguments_with_only_self_argument_without_annotation():
    generator = ArgumentsGenerator(schema=GraphQLSchema())
    query = "query q {r}"
    variable_definitions = _get_variable_definitions_from_query_str(query)

    arguments, _ = generator.generate(variable_definitions)

    assert isinstance(arguments, ast.arguments)
    assert len(arguments.args) == 1
    self_arg = arguments.args[0]
    assert self_arg.arg == "self"
    assert not self_arg.annotation


def test_generate_saves_used_non_scalar_types():
    schema_str = """
        schema { query: Query }
        type Query { _skip: String! }

        input Type1 { fieldA: Int! }
        input Type2 { fieldB: Int! }
        """
    schema = build_schema(schema_str)
    generator = ArgumentsGenerator(schema=schema)
    query = "query q($a1: String!, $a2: String, $a3: Type1!, $a4: Type2) {r}"
    variable_definitions = _get_variable_definitions_from_query_str(query)

    generator.generate(variable_definitions)

    used_inputs = generator.get_used_inputs()
    assert len(used_inputs) == 2
    assert used_inputs == ["Type1", "Type2"]


def test_generate_returns_arguments_and_dictionary_with_snake_case_names():
    generator = ArgumentsGenerator(schema=GraphQLSchema(), convert_to_snake_case=True)
    query = "query q($camelCase: String!, $snake_case: String!) {r}"
    variable_definitions = _get_variable_definitions_from_query_str(query)

    arguments, arguments_dict = generator.generate(variable_definitions)

    expected_arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(arg="camel_case", annotation=ast.Name(id="str")),
            ast.arg(arg="snake_case", annotation=ast.Name(id="str")),
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )
    expected_arguments_dict = ast.Dict(
        keys=[ast.Constant(value="camelCase"), ast.Constant(value="snake_case")],
        values=[ast.Name(id="camel_case"), ast.Name(id="snake_case")],
    )

    assert compare_ast(arguments, expected_arguments)
    assert compare_ast(arguments_dict, expected_arguments_dict)


def test_generate_returns_arguments_with_used_custom_scalar():
    schema_str = """
        schema { query: Query }
        type Query { _skip: String! }
        scalar CustomScalar
        """
    generator = ArgumentsGenerator(schema=build_schema(schema_str))
    query_str = "query q($arg: CustomScalar!) {r}"

    expected_arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(arg="arg", annotation=ast.Name(id=ANY)),
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )
    expected_arguments_dict = ast.Dict(
        keys=[ast.Constant(value="arg")], values=[ast.Name(id="arg")]
    )

    arguments, arguments_dict = generator.generate(
        _get_variable_definitions_from_query_str(query_str)
    )

    assert compare_ast(arguments, expected_arguments)
    assert compare_ast(arguments_dict, expected_arguments_dict)
