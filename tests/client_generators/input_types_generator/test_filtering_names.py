import ast

import pytest
from graphql import build_ast_schema, parse

from ariadne_codegen.client_generators.input_types import InputTypesGenerator


@pytest.mark.parametrize(
    "used_types, expected_classes",
    [
        (
            None,
            ["InputA", "InputAA", "InputAAA", "InputAB", "InputX", "InputY", "InputZ"],
        ),
        (["InputA"], ["InputA", "InputAA", "InputAAA", "InputAB"]),
        (["InputAA"], ["InputAA", "InputAAA"]),
        (["InputX"], ["InputX", "InputY", "InputZ"]),
        (
            ["InputA", "InputX"],
            ["InputA", "InputAA", "InputAAA", "InputAB", "InputX", "InputY", "InputZ"],
        ),
        (["InputAB"], ["InputA", "InputAA", "InputAAA", "InputAB"]),
        (["InputAAA", "InputZ"], ["InputAAA", "InputZ"]),
        (
            ["InputA", "InputA", "InputA", "InputAA", "InputAAA"],
            ["InputA", "InputAA", "InputAAA", "InputAB"],
        ),
    ],
)
def test_generator_returns_module_with_filtered_classes(used_types, expected_classes):
    schema_str = """
    input InputA {
        valueAA: InputAA!
        valueAB: InputAB
    }

    input InputAA {
        valueAAA: InputAAA!
    }

    input InputAAA {
        val: String!
    }

    input InputAB {
        val: String!
        valueA: InputA
    }

    input InputX {
        valueY: InputY
    }

    input InputY {
        valueZ: InputZ
    }

    input InputZ {
        val: String
    }
    """

    generator = InputTypesGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate(used_types)

    assert [
        class_def.name
        for class_def in module.body
        if isinstance(class_def, ast.ClassDef)
    ] == expected_classes
