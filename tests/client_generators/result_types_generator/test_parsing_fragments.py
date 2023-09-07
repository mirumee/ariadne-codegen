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


def test_get_classes_returns_empty_list_for_fragment_on_union():
    fragment_str = """
        fragment TestFragment on UnionType {
            ... on CustomType1 {
                fielda
            }
            ... on CustomType2 {
                fieldb
            }
        }
    """
    fragment_definition = cast(
        FragmentDefinitionNode, parse(fragment_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=fragment_definition,
        enums_module_name="enums",
        fragments_definitions={"TestFragment": fragment_definition},
    )

    generated_class_defs = generator.get_classes()

    assert not generated_class_defs


def test_get_classes_returns_empty_list_for_fragment_with_inline_fragments():
    fragment_str = """
        fragment TestFragment on InterfaceI {
            id
            ... on TypeA {
                fieldA
            }
            ... on TypeB {
                fieldB
            }
        }
    """
    fragment_definition = cast(
        FragmentDefinitionNode, parse(fragment_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=fragment_definition,
        enums_module_name="enums",
        fragments_definitions={"TestFragment": fragment_definition},
    )

    generated_class_defs = generator.get_classes()

    assert not generated_class_defs


def test_get_classes_returns_fragment_classes_with_handled_mixin_directive():
    fragment_str = """
        fragment TestFragment on CustomType
        @mixin(from: ".test_mixins", import: "TestMixinA")  {
            id
        }
    """
    fragment_definition = cast(
        FragmentDefinitionNode, parse(fragment_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=fragment_definition,
        enums_module_name="enums",
        fragments_definitions={"TestFragment": fragment_definition},
    )

    generated_class_defs = generator.get_classes()

    assert len(generated_class_defs) == 1
    fragment_class_def = generated_class_defs[0]
    assert fragment_class_def.name == "TestFragment"
    assert {b.id for b in fragment_class_def.bases} == {
        BASE_MODEL_CLASS_NAME,
        "TestMixinA",
    }


def test_get_imports_returns_mixin_imports():
    fragment_str = """
        fragment TestFragment on CustomType
        @mixin(from: ".test_mixins", import: "TestMixinA")  {
            id
        }
    """
    fragment_definition = cast(
        FragmentDefinitionNode, parse(fragment_str).definitions[0]
    )
    generator = ResultTypesGenerator(
        schema=build_schema(SCHEMA_STR),
        operation_definition=fragment_definition,
        enums_module_name="enums",
        fragments_definitions={"TestFragment": fragment_definition},
    )

    generated_imports = generator.get_imports()

    mixin_imports = [imp for imp in generated_imports if imp.module == ".test_mixins"]
    assert len(mixin_imports) == 1
    assert compare_ast(
        mixin_imports[0],
        ast.ImportFrom(module=".test_mixins", names=[ast.alias("TestMixinA")], level=0),
    )
