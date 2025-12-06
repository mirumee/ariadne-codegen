import ast

import pytest
from graphql import build_ast_schema, parse

from ariadne_codegen.client_generators.constants import (
    ALIAS_KEYWORD,
    BASE_MODEL_CLASS_NAME,
    FIELD_CLASS,
)
from ariadne_codegen.client_generators.input_types import InputTypesGenerator
from ariadne_codegen.utils import ast_to_str

from ...utils import compare_ast, get_assignment_target_names, get_class_def


@pytest.mark.parametrize(
    "schema_str, expected_class_def",
    [
        (
            """
            input CustomInput {
                inputField1: String!
                input_field2: String!
                inputfield3: String!
            }
            """,
            ast.ClassDef(
                name="CustomInput",
                bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                keywords=[],
                body=[
                    ast.AnnAssign(
                        target=ast.Name(id="input_field_1"),
                        annotation=ast.Name(id="str"),
                        value=ast.Call(
                            func=ast.Name(id=FIELD_CLASS),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg=ALIAS_KEYWORD,
                                    value=ast.Constant(value="inputField1"),
                                )
                            ],
                        ),
                        simple=1,
                    ),
                    ast.AnnAssign(
                        target=ast.Name(id="input_field_2"),
                        annotation=ast.Name(id="str"),
                        value=ast.Call(
                            func=ast.Name(id=FIELD_CLASS),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg=ALIAS_KEYWORD,
                                    value=ast.Constant(value="input_field2"),
                                )
                            ],
                        ),
                        simple=1,
                    ),
                    ast.AnnAssign(
                        target=ast.Name(id="inputfield_3"),
                        annotation=ast.Name(id="str"),
                        value=ast.Call(
                            func=ast.Name(id=FIELD_CLASS),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg=ALIAS_KEYWORD,
                                    value=ast.Constant(value="inputfield3"),
                                )
                            ],
                        ),
                        simple=1,
                    ),
                ],
                decorator_list=[],
                type_params=[],
            ),
        ),
        (
            """
            input CustomInput {
                inputField1: String! = "abcd"
                inputField2: [Int!]! = [1, 2, 3]
            }
            """,
            ast.ClassDef(
                name="CustomInput",
                bases=[ast.Name(id=BASE_MODEL_CLASS_NAME)],
                keywords=[],
                body=[
                    ast.AnnAssign(
                        target=ast.Name(id="input_field_1"),
                        annotation=ast.Name(id="str"),
                        value=ast.Call(
                            func=ast.Name(id=FIELD_CLASS),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg=ALIAS_KEYWORD,
                                    value=ast.Constant(value="inputField1"),
                                ),
                                ast.keyword(
                                    arg="default", value=ast.Constant(value="abcd")
                                ),
                            ],
                        ),
                        simple=1,
                    ),
                    ast.AnnAssign(
                        target=ast.Name(id="input_field_2"),
                        annotation=ast.Subscript(
                            value=ast.Name(id="list"), slice=ast.Name(id="int")
                        ),
                        value=ast.Call(
                            func=ast.Name(id=FIELD_CLASS),
                            args=[],
                            keywords=[
                                ast.keyword(
                                    arg=ALIAS_KEYWORD,
                                    value=ast.Constant(value="inputField2"),
                                ),
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
                                        body=ast.List(
                                            elts=[
                                                ast.Constant(value=1),
                                                ast.Constant(value=2),
                                                ast.Constant(value=3),
                                            ]
                                        ),
                                    ),
                                ),
                            ],
                        ),
                        simple=1,
                    ),
                ],
                decorator_list=[],
                type_params=[],
            ),
        ),
    ],
)
def test_generate_returns_module_with_fields_names_converted_to_snake_case(
    schema_str, expected_class_def
):
    generator = InputTypesGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    class_def = get_class_def(module)
    assert compare_ast(class_def, expected_class_def)


def test_generate_returns_module_with_valid_field_names():
    schema = """
    input KeywordInput {
        in: String!
        from: String!
        and: String!
        _foo: String!
        _Bar: String!
        ____baz_: String!
        _: String!
        schema: String!
    }
    """

    generator = InputTypesGenerator(schema=build_ast_schema(parse(schema)))

    module = generator.generate()

    parsed = ast.parse(
        ast_to_str(module)
    )  # Round trip because invalid identifiers get picked up in parse
    class_def = get_class_def(parsed)
    field_names = get_assignment_target_names(class_def)
    assert field_names == {
        "in_",
        "from_",
        "and_",
        "foo",
        "bar",
        "baz",
        "underscore_named_field_",
        "schema_",
    }
