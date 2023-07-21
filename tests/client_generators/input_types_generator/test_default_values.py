import ast

import pytest
from graphql import build_ast_schema, parse

from ariadne_codegen.client_generators.constants import (
    BASE_MODEL_CLASS_NAME,
    FIELD_CLASS,
    MODEL_VALIDATE_METHOD,
    OPTIONAL,
)
from ariadne_codegen.client_generators.input_types import InputTypesGenerator

from ...utils import compare_ast, get_class_def


@pytest.mark.parametrize(
    "field_str, expected_annotation, expected_value",
    [
        ("field: Int! = 5", ast.Name(id="int"), ast.Constant(value=5)),
        ("field: Float! = 1.5", ast.Name(id="float"), ast.Constant(value=1.5)),
        ('field: String! = "abc"', ast.Name(id="str"), ast.Constant(value="abc")),
        ("field: Boolean! = false", ast.Name(id="bool"), ast.Constant(value=False)),
        (
            "field: String = null",
            ast.Subscript(value=ast.Name(id=OPTIONAL), slice=ast.Name(id="str")),
            ast.Constant(value=None),
        ),
    ],
)
def test_generate_returns_module_with_parsed_inputs_scalar_field_with_default_value(
    field_str, expected_annotation, expected_value, base_model_import, upload_import
):
    schema_str = f"input TestInput {{{field_str}}}"
    generator = InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)),
        enums_module="enums",
        scalars_module_name="scalars",
        base_model_import=base_model_import,
        upload_import=upload_import,
    )
    expected_class_def = ast.ClassDef(
        name="TestInput",
        bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
        keywords=[],
        decorator_list=[],
        body=[
            ast.AnnAssign(
                target=ast.Name(id="field"),
                annotation=expected_annotation,
                value=expected_value,
                simple=1,
            )
        ],
    )
    module = generator.generate()

    class_def = get_class_def(module)
    assert compare_ast(class_def, expected_class_def)


@pytest.mark.parametrize(
    "field_str, expected_list",
    [
        (
            "field: [Int!] = [1, 2]",
            ast.List(elts=[ast.Constant(value=1), ast.Constant(value=2)]),
        ),
        (
            'field: [String!] = ["a", "b", "c"]',
            ast.List(
                elts=[
                    ast.Constant(value="a"),
                    ast.Constant(value="b"),
                    ast.Constant(value="c"),
                ]
            ),
        ),
        (
            'field: [[String]!] = [["a", "a"], ["b", "b"], ["c", "c"]]',
            ast.List(
                elts=[
                    ast.List(
                        elts=[
                            ast.Constant(value="a"),
                            ast.Constant(value="a"),
                        ]
                    ),
                    ast.List(
                        elts=[
                            ast.Constant(value="b"),
                            ast.Constant(value="b"),
                        ]
                    ),
                    ast.List(
                        elts=[
                            ast.Constant(value="c"),
                            ast.Constant(value="c"),
                        ]
                    ),
                ]
            ),
        ),
    ],
)
def test_generate_returns_module_with_parsed_inputs_list_field_with_default_value(
    field_str, expected_list, base_model_import, upload_import
):
    schema_str = f"input TestInput {{{field_str}}}"
    generator = InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)),
        enums_module="enums",
        scalars_module_name="scalars",
        base_model_import=base_model_import,
        upload_import=upload_import,
    )
    expected_field_value = ast.Call(
        func=ast.Name(id=FIELD_CLASS),
        args=[],
        keywords=[
            ast.keyword(
                arg="default_factory",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=expected_list,
                ),
            )
        ],
    )

    module = generator.generate()

    class_def = get_class_def(module)
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.name == "TestInput"
    assert len(class_def.body) == 1
    field_def = class_def.body[0]
    assert isinstance(field_def, ast.AnnAssign)
    assert field_def.value
    assert compare_ast(field_def.value, expected_field_value)


def test_generate_returns_module_with_parsed_inputs_object_field_with_default_value(
    base_model_import, upload_import
):
    schema_str = """
    input TestInput {
        field: SecondInput = {val: 5}
    }

    input SecondInput {
        val: Int!
    }
    """
    expected_field_value = ast.Call(
        func=ast.Name(id="Field"),
        args=[],
        keywords=[
            ast.keyword(
                arg="default_factory",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Call(
                        func=ast.Attribute(
                            value=ast.Subscript(
                                value=ast.Call(
                                    func=ast.Name(id="globals"), args=[], keywords=[]
                                ),
                                slice=ast.Constant(value="SecondInput"),
                            ),
                            attr=MODEL_VALIDATE_METHOD,
                        ),
                        args=[
                            ast.Dict(
                                keys=[ast.Constant(value="val")],
                                values=[ast.Constant(value=5)],
                            )
                        ],
                        keywords=[],
                    ),
                ),
            )
        ],
    )

    generator = InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)),
        enums_module="enums",
        scalars_module_name="scalars",
        base_model_import=base_model_import,
        upload_import=upload_import,
    )

    module = generator.generate()

    class_def = get_class_def(module, 0)
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.name == "TestInput"
    assert len(class_def.body) == 1
    field_def = class_def.body[0]
    assert isinstance(field_def, ast.AnnAssign)
    assert field_def.value
    assert compare_ast(field_def.value, expected_field_value)


def test_generate_returns_module_with_parsed_nested_object_as_default_value(
    base_model_import, upload_import
):
    schema_str = """
    input TestInput {
        field: SecondInput = { nested: { val: 1.5 } }
    }

    input SecondInput {
        nested: NestedInput! = { val: 2.5 }
    }

    input NestedInput {
        val: Float! 
    }
    """
    expected_field_value = ast.Call(
        func=ast.Name(id="Field"),
        args=[],
        keywords=[
            ast.keyword(
                arg="default_factory",
                value=ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[],
                    ),
                    body=ast.Call(
                        func=ast.Attribute(
                            value=ast.Subscript(
                                value=ast.Call(
                                    func=ast.Name(id="globals"), args=[], keywords=[]
                                ),
                                slice=ast.Constant(value="SecondInput"),
                            ),
                            attr=MODEL_VALIDATE_METHOD,
                        ),
                        args=[
                            ast.Dict(
                                keys=[ast.Constant(value="nested")],
                                values=[
                                    ast.Dict(
                                        keys=[ast.Constant(value="val")],
                                        values=[ast.Constant(value=1.5)],
                                    )
                                ],
                            )
                        ],
                        keywords=[],
                    ),
                ),
            )
        ],
    )
    generator = InputTypesGenerator(
        schema=build_ast_schema(parse(schema_str)),
        enums_module="enums",
        scalars_module_name="scalars",
        base_model_import=base_model_import,
        upload_import=upload_import,
    )

    module = generator.generate()

    class_def = get_class_def(module, 0)
    assert isinstance(class_def, ast.ClassDef)
    assert class_def.name == "TestInput"
    assert len(class_def.body) == 1
    field_def = class_def.body[0]
    assert isinstance(field_def, ast.AnnAssign)
    assert field_def.value
    assert compare_ast(field_def.value, expected_field_value)
