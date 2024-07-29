import ast

import pytest
from graphql import build_ast_schema, parse

from ariadne_codegen.client_generators.constants import (
    ALIAS_KEYWORD,
    BASE_MODEL_CLASS_NAME,
    FIELD_CLASS,
)
from ariadne_codegen.client_generators.input_types import InputTypesGenerator

from ...utils import compare_ast, filter_class_defs


@pytest.mark.parametrize(
    "schema_str, expected_class_defs",
    [
        (
            """
            input CustomInput {
                field1: CustomInput2!
                field2: Int!
            }

            input CustomInput2 {
                field: Int!
            }
            """,
            [
                ast.ClassDef(
                    name="CustomInput",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    decorator_list=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="field_1"),
                            annotation=ast.Name(id='"CustomInput2"'),
                            value=ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=ALIAS_KEYWORD,
                                        value=ast.Constant(value="field1"),
                                    )
                                ],
                            ),
                            simple=1,
                        ),
                        ast.AnnAssign(
                            target=ast.Name(id="field_2"),
                            annotation=ast.Name(id="int"),
                            value=ast.Call(
                                func=ast.Name(id=FIELD_CLASS),
                                args=[],
                                keywords=[
                                    ast.keyword(
                                        arg=ALIAS_KEYWORD,
                                        value=ast.Constant(value="field2"),
                                    )
                                ],
                            ),
                            simple=1,
                        ),
                    ],
                    type_params=[],
                ),
                ast.ClassDef(
                    name="CustomInput2",
                    bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                    keywords=[],
                    decorator_list=[],
                    body=[
                        ast.AnnAssign(
                            target=ast.Name(id="field"),
                            annotation=ast.Name(id="int"),
                            simple=1,
                        )
                    ],
                    type_params=[],
                ),
            ],
        )
    ],
)
def test_generate_returns_module_with_parsed_input_types(
    schema_str, expected_class_defs
):
    generator = InputTypesGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_class_defs)


def test_generate_returns_module_with_classes_in_the_same_order_as_declared():
    schema_str = """
    input BeforeInput {
        field: Boolean!
    }

    input TestInput {
        field: SecondInput = { nested: { val: 1.5 } }
    }

    input SecondInput {
        nested: NestedInput! = { val: 2.5 }
    }

    input NestedInput {
        val: Float! 
    }

    input AfterInput {
        field: Boolean!
    }
    """
    expected_order = [
        "BeforeInput",
        "TestInput",
        "SecondInput",
        "NestedInput",
        "AfterInput",
    ]
    generator = InputTypesGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    generated_class_names = [c.name for c in filter_class_defs(module)]
    assert generated_class_names == expected_order
