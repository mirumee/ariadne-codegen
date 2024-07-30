import ast
from typing import cast

import pytest
from graphql import FragmentDefinitionNode, GraphQLSchema, build_schema, parse

from ariadne_codegen.client_generators.constants import ALIAS_KEYWORD
from ariadne_codegen.client_generators.fragments import FragmentsGenerator

from ..utils import compare_ast, filter_class_defs


@pytest.fixture
def schema() -> GraphQLSchema:
    schema_str = """
    schema { query: Query }
    type Query { testQuery: CustomType! }
    type CustomType {
        id: ID!
        fieldA: String!
        fieldB: Int!
    }
    """
    return build_schema(schema_str)


@pytest.fixture
def fragment_a() -> FragmentDefinitionNode:
    return cast(
        FragmentDefinitionNode,
        parse("fragment FragmentA on CustomType { fieldA }").definitions[0],
    )


@pytest.fixture
def fragment_b() -> FragmentDefinitionNode:
    return cast(
        FragmentDefinitionNode,
        parse("fragment FragmentB on CustomType { fieldB }").definitions[0],
    )


@pytest.fixture
def test_fragment() -> FragmentDefinitionNode:
    fragment_str = """
    fragment TestFragment on CustomType {
        id
        ...FragmentA
    }"""
    return cast(FragmentDefinitionNode, parse(fragment_str).definitions[0])


def test_generate_returns_module_with_class_for_every_fragment(
    schema, fragment_a, fragment_b
):
    expected_class_defs = [
        ast.ClassDef(
            name="FragmentA",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="field_a"),
                    annotation=ast.Name(id="str"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD, value=ast.Constant(value="fieldA")
                            )
                        ],
                    ),
                    simple=1,
                )
            ],
            decorator_list=[],
            type_params=[],
        ),
        ast.ClassDef(
            name="FragmentB",
            bases=[ast.Name(id="BaseModel")],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="field_b"),
                    annotation=ast.Name(id="int"),
                    value=ast.Call(
                        func=ast.Name(id="Field"),
                        args=[],
                        keywords=[
                            ast.keyword(
                                arg=ALIAS_KEYWORD, value=ast.Constant(value="fieldB")
                            )
                        ],
                    ),
                    simple=1,
                )
            ],
            decorator_list=[],
            type_params=[],
        ),
    ]
    generator = FragmentsGenerator(
        schema=schema,
        enums_module_name="enums",
        fragments_definitions={"FragmentA": fragment_a, "FragmentB": fragment_b},
        convert_to_snake_case=True,
    )

    module = generator.generate()

    generated_class_defs = filter_class_defs(module)
    assert compare_ast(generated_class_defs, expected_class_defs)


def test_generate_returns_module_with_correct_order_of_classes(
    schema, fragment_a, test_fragment
):
    generator = FragmentsGenerator(
        schema=schema,
        enums_module_name="enums",
        fragments_definitions={
            "TestFragment": test_fragment,
            "FragmentA": fragment_a,
        },
        convert_to_snake_case=True,
    )

    module = generator.generate()

    generated_class_defs = filter_class_defs(module)
    assert [c.name for c in generated_class_defs] == ["FragmentA", "TestFragment"]


def test_generate_returns_module_without_models_for_excluded_fragments(
    schema, fragment_a, fragment_b, test_fragment
):
    generator = FragmentsGenerator(
        schema=schema,
        enums_module_name="enums",
        fragments_definitions={
            "TestFragment": test_fragment,
            "FragmentA": fragment_a,
            "FragmentB": fragment_b,
        },
        convert_to_snake_case=True,
    )

    module = generator.generate(exclude_names={"TestFragment", "FragmentB"})

    generated_class_defs = filter_class_defs(module)
    assert [c.name for c in generated_class_defs] == ["FragmentA"]


def test_generate_triggers_generate_fragments_module_hook(mocked_plugin_manager):
    generator = FragmentsGenerator(
        schema=GraphQLSchema(),
        enums_module_name="enums",
        fragments_definitions={},
        plugin_manager=mocked_plugin_manager,
    )
    generator.generate()

    assert mocked_plugin_manager.generate_fragments_module.called
