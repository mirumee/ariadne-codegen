import ast

from graphql import GraphQLSchema, OperationDefinitionNode, build_schema, parse

from ariadne_codegen.client_generators.arguments import ArgumentsGenerator
from ariadne_codegen.client_generators.constants import (
    ANY,
    OPTIONAL,
    UNION,
    UNSET_NAME,
    UNSET_TYPE_NAME,
    UPLOAD_CLASS_NAME,
)
from ariadne_codegen.client_generators.scalars import ScalarData

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
    expected_arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(
                arg="id",
                annotation=ast.Subscript(
                    value=ast.Name(id=UNION),
                    slice=ast.Tuple(
                        elts=[
                            ast.Subscript(
                                value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")
                            ),
                            ast.Name(id=UNSET_TYPE_NAME),
                        ]
                    ),
                ),
            ),
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[ast.Name(id="UNSET")],
    )

    arguments, _ = generator.generate(variable_definitions)

    assert compare_ast(arguments, expected_arguments)


def test_generate_returns_arguments_with_default_value_for_optional_args():
    schema_str = """
        schema { query: Query }
        type Query { q(a: String, b: Float!, c: Int, d: Boolean!): Result! }
        type Result { r: String}
        """
    schema = build_schema(schema_str)
    generator = ArgumentsGenerator(schema=schema)
    query = "query q($a: String, $b: Float!, $c: Int, $d: Boolean!) {r}"
    variable_definitions = _get_variable_definitions_from_query_str(query)
    expected_arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(arg="b", annotation=ast.Name(id="float")),
            ast.arg(arg="d", annotation=ast.Name(id="bool")),
            ast.arg(
                arg="a",
                annotation=ast.Subscript(
                    value=ast.Name(id=UNION),
                    slice=ast.Tuple(
                        elts=[
                            ast.Subscript(
                                value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")
                            ),
                            ast.Name(id=UNSET_TYPE_NAME),
                        ]
                    ),
                ),
            ),
            ast.arg(
                arg="c",
                annotation=ast.Subscript(
                    value=ast.Name(id=UNION),
                    slice=ast.Tuple(
                        elts=[
                            ast.Subscript(
                                value=ast.Name(id=OPTIONAL), slice=ast.Name(id="int")
                            ),
                            ast.Name(id=UNSET_TYPE_NAME),
                        ]
                    ),
                ),
            ),
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[ast.Name(id=UNSET_NAME), ast.Name(id=UNSET_NAME)],
    )

    arguments, _ = generator.generate(variable_definitions)

    assert compare_ast(arguments, expected_arguments)


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


def test_generate_returns_arguments_and_dictionary_with_valid_names():
    generator = ArgumentsGenerator(schema=GraphQLSchema(), convert_to_snake_case=True)
    query = (
        "query q($from: String!, $and: String!, $in: String!, "
        "$_fieldA: String!, $_FieldB: String!) {r}"
    )
    variable_definitions = _get_variable_definitions_from_query_str(query)

    arguments, arguments_dict = generator.generate(variable_definitions)

    expected_arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(arg="from_", annotation=ast.Name(id="str")),
            ast.arg(arg="and_", annotation=ast.Name(id="str")),
            ast.arg(arg="in_", annotation=ast.Name(id="str")),
            ast.arg(arg="field_a", annotation=ast.Name(id="str")),
            ast.arg(arg="field_b", annotation=ast.Name(id="str")),
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )
    expected_arguments_dict = ast.Dict(
        keys=[
            ast.Constant(value="from"),
            ast.Constant(value="and"),
            ast.Constant(value="in"),
            ast.Constant(value="_fieldA"),
            ast.Constant(value="_FieldB"),
        ],
        values=[
            ast.Name(id="from_"),
            ast.Name(id="and_"),
            ast.Name(id="in_"),
            ast.Name(id="field_a"),
            ast.Name(id="field_b"),
        ],
    )

    assert compare_ast(arguments, expected_arguments)
    assert compare_ast(arguments_dict, expected_arguments_dict)


def test_generate_returns_arguments_with_not_mapped_custom_scalar():
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


def test_generate_returns_arguments_with_custom_scalar_and_used_serialize_method():
    schema_str = """
        schema { query: Query }
        type Query { _skip: String! }
        scalar SCALARABC
        """
    query_str = "query q($arg: SCALARABC!) {r}"
    generator = ArgumentsGenerator(
        schema=build_schema(schema_str),
        custom_scalars={
            "SCALARABC": ScalarData(
                type_="ScalarABC", serialize="serialize_abc", graphql_name="SCALARABC"
            )
        },
    )
    expected_arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(arg="arg", annotation=ast.Name(id="ScalarABC")),
        ],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[],
    )
    expected_arguments_dict = ast.Dict(
        keys=[ast.Constant(value="arg")],
        values=[
            ast.Call(
                func=ast.Name(id="serialize_abc"),
                args=[ast.Name(id="arg")],
                keywords=[],
            )
        ],
    )

    arguments, arguments_dict = generator.generate(
        _get_variable_definitions_from_query_str(query_str)
    )

    assert compare_ast(arguments, expected_arguments)
    assert compare_ast(arguments_dict, expected_arguments_dict)


def test_generate_returns_arguments_with_upload_scalar():
    schema_str = """
        schema { query: Query }
        type Query { _skip: String! }
        scalar Upload
        """
    generator = ArgumentsGenerator(schema=build_schema(schema_str))
    query_str = "query q($arg: Upload!) {r}"

    expected_arguments = ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg="self"),
            ast.arg(arg="arg", annotation=ast.Name(id=UPLOAD_CLASS_NAME)),
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


def test_generate_triggers_generate_arguments_hook(mocked_plugin_manager):
    schema_str = """
        schema { query: Query }
        type Query { _skip: String! }
        """
    generator = ArgumentsGenerator(
        schema=build_schema(schema_str), plugin_manager=mocked_plugin_manager
    )

    generator.generate(
        _get_variable_definitions_from_query_str("query q($arg: String!) { _skip }")
    )

    assert mocked_plugin_manager.generate_arguments.called


def test_generate_triggers_generate_arguments_dict_hook(mocked_plugin_manager):
    schema_str = """
        schema { query: Query }
        type Query { _skip: String! }
        """
    generator = ArgumentsGenerator(
        schema=build_schema(schema_str), plugin_manager=mocked_plugin_manager
    )

    generator.generate(
        _get_variable_definitions_from_query_str("query q($arg: String!) { _skip }")
    )

    assert mocked_plugin_manager.generate_arguments_dict.called


def test_generate_triggers_process_name_hook_for_every_arg(mocked_plugin_manager):
    schema_str = """
        schema { query: Query }
        type Query { _skip: String! }
        """
    generator = ArgumentsGenerator(
        schema=build_schema(schema_str), plugin_manager=mocked_plugin_manager
    )

    generator.generate(
        _get_variable_definitions_from_query_str(
            "query q($arg1: String!, $arg2: String) { _skip }"
        )
    )

    assert mocked_plugin_manager.process_name.call_count == 2
    name1 = mocked_plugin_manager.process_name.mock_calls[0].args[0]
    name2 = mocked_plugin_manager.process_name.mock_calls[1].args[0]
    assert name1 == "arg_1"
    assert name2 == "arg_2"
