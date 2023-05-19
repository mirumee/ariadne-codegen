import ast
from typing import cast

from graphql import FragmentDefinitionNode, build_schema, parse

from ariadne_codegen.client_generators.constants import BASE_MODEL_CLASS_NAME
from ariadne_codegen.client_generators.result_types import ResultTypesGenerator

from ...utils import compare_ast
from .schema import SCHEMA_STR


def test_get_classes_returns_list_with_types_generated_from_fragment():
    fragment_str = """
        fragment TestFragment on CustomType {
            id
            field1 { fielda }
        }
    """
    fragment_definition = cast(
        FragmentDefinitionNode, parse(fragment_str).definitions[0]
    )
    expected_class_defs = [
        ast.ClassDef(
            name="TestFragment",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="id"), annotation=ast.Name(id="str"), simple=1
                ),
                ast.AnnAssign(
                    target=ast.Name(id="field1"),
                    annotation=ast.Name(id='"TestFragmentField1"'),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="TestFragmentField1",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="fielda"),
                    annotation=ast.Name(id="int"),
                    simple=1,
                )
            ],
            decorator_list=[],
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=fragment_definition,
        enums_module_name="enums",
    )

    generated_class_defs = generator.get_classes()

    assert compare_ast(generated_class_defs, expected_class_defs)
    assert set(generator.get_generated_public_names()) == {
        c.name for c in expected_class_defs
    }


def test_get_classes_returns_types_generated_from_fragment_which_uses_other_fragment():
    fragment_str = """
        fragment TestFragment on CustomType {
            id
            field1 { ...TestNestedFragment }
        }

        fragment TestNestedFragment on CustomType1 {
            fielda
        }
    """
    fragment_definition, nested_fragment_definition = cast(
        FragmentDefinitionNode, parse(fragment_str).definitions
    )
    expected_class_defs = [
        ast.ClassDef(
            name="TestFragment",
            bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
            keywords=[],
            body=[
                ast.AnnAssign(
                    target=ast.Name(id="id"), annotation=ast.Name(id="str"), simple=1
                ),
                ast.AnnAssign(
                    target=ast.Name(id="field1"),
                    annotation=ast.Name(id='"TestFragmentField1"'),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
        ast.ClassDef(
            name="TestFragmentField1",
            bases=[ast.Name(id="TestNestedFragment")],
            keywords=[],
            body=[ast.Pass()],
            decorator_list=[],
        ),
    ]
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=fragment_definition,
        enums_module_name="enums",
        fragments_definitions={
            "TestFragment": fragment_definition,
            "TestNestedFragment": nested_fragment_definition,
        },
    )

    generated_class_defs = generator.get_classes()

    assert compare_ast(generated_class_defs, expected_class_defs)
    assert set(generator.get_generated_public_names()) == {
        c.name for c in expected_class_defs
    }
