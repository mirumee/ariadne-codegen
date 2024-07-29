import ast

import pytest
from graphql import GraphQLEnumType, GraphQLSchema, build_ast_schema, parse

from ariadne_codegen.client_generators.constants import ENUM_CLASS, ENUM_MODULE
from ariadne_codegen.client_generators.enums import EnumsGenerator

from ..utils import compare_ast, filter_class_defs, get_class_def


def test_generate_returns_module_with_correct_imports():
    schema_str = """
    enum CustomEnum {
        VALUE1
        VALUE2
    }
    """
    expected_import = ast.ImportFrom(
        module=ENUM_MODULE, names=[ast.alias(name=ENUM_CLASS)], level=0
    )
    generator = EnumsGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    import_ = module.body[0]
    assert compare_ast(import_, expected_import)


def test_generate_returns_module_with_enum_class_definition():
    schema_str = """
    enum CustomEnum {
        VALUE1
        VALUE2
        from
        import
    }
    """
    expected_class_def = ast.ClassDef(
        name="CustomEnum",
        bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
        keywords=[],
        decorator_list=[],
        body=[
            ast.Assign(
                targets=[ast.Name(id="VALUE1")], value=ast.Constant(value="VALUE1")
            ),
            ast.Assign(
                targets=[ast.Name(id="VALUE2")], value=ast.Constant(value="VALUE2")
            ),
            ast.Assign(
                targets=[ast.Name(id="from_")], value=ast.Constant(value="from")
            ),
            ast.Assign(
                targets=[ast.Name(id="import_")], value=ast.Constant(value="import")
            ),
        ],
        type_params=[],
    )
    generator = EnumsGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    assert generator.get_generated_public_names() == ["CustomEnum"]
    class_def = get_class_def(module)
    assert class_def.name == "CustomEnum"
    assert compare_ast(class_def, expected_class_def)


def test_generate_returns_module_with_enum_class_definition_for_every_enum():
    schema_str = """
    enum TestEnumA {
        VALUE1
        VALUE2
    }

    enum TestEnumB {
        A
        B
        C
    }

    enum TestEnumC {
        A1
        B2
        C3
        D4
        E5
    }
    """
    expected_class_defs = [
        ast.ClassDef(
            name="TestEnumA",
            bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
            keywords=[],
            decorator_list=[],
            body=[
                ast.Assign(
                    targets=[ast.Name(id="VALUE1")], value=ast.Constant(value="VALUE1")
                ),
                ast.Assign(
                    targets=[ast.Name(id="VALUE2")], value=ast.Constant(value="VALUE2")
                ),
            ],
            type_params=[],
        ),
        ast.ClassDef(
            name="TestEnumB",
            bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
            keywords=[],
            decorator_list=[],
            body=[
                ast.Assign(targets=[ast.Name(id="A")], value=ast.Constant(value="A")),
                ast.Assign(targets=[ast.Name(id="B")], value=ast.Constant(value="B")),
                ast.Assign(targets=[ast.Name(id="C")], value=ast.Constant(value="C")),
            ],
            type_params=[],
        ),
        ast.ClassDef(
            name="TestEnumC",
            bases=[ast.Name(id="str"), ast.Name(id=ENUM_CLASS)],
            keywords=[],
            decorator_list=[],
            body=[
                ast.Assign(targets=[ast.Name(id="A1")], value=ast.Constant(value="A1")),
                ast.Assign(targets=[ast.Name(id="B2")], value=ast.Constant(value="B2")),
                ast.Assign(targets=[ast.Name(id="C3")], value=ast.Constant(value="C3")),
                ast.Assign(targets=[ast.Name(id="D4")], value=ast.Constant(value="D4")),
                ast.Assign(targets=[ast.Name(id="E5")], value=ast.Constant(value="E5")),
            ],
            type_params=[],
        ),
    ]
    generator = EnumsGenerator(schema=build_ast_schema(parse(schema_str)))

    module = generator.generate()

    assert generator.get_generated_public_names() == [
        "TestEnumA",
        "TestEnumB",
        "TestEnumC",
    ]
    class_defs = filter_class_defs(module)
    assert compare_ast(class_defs, expected_class_defs)


def test_generate_triggers_generate_enums_module_hook(mocked_plugin_manager):
    generator = EnumsGenerator(
        schema=GraphQLSchema(), plugin_manager=mocked_plugin_manager
    )

    generator.generate()

    assert mocked_plugin_manager.generate_enums_module.called


def test_generate_triggers_generate_enum_hook_for_every_definition(
    mocked_plugin_manager,
):
    schema_str = """
    enum TestEnumAB {
        A
        B
    }
    enum TestEnumCD {
        C
        D
    }
    """
    generator = EnumsGenerator(
        schema=build_ast_schema(parse(schema_str)), plugin_manager=mocked_plugin_manager
    )

    generator.generate()

    assert mocked_plugin_manager.generate_enum.call_count == 2
    _, call0_enum_type = mocked_plugin_manager.generate_enum.mock_calls[0].args
    _, call1_enum_type = mocked_plugin_manager.generate_enum.mock_calls[1].args
    assert isinstance(call0_enum_type, GraphQLEnumType)
    assert call0_enum_type.name == "TestEnumAB"
    assert isinstance(call1_enum_type, GraphQLEnumType)
    assert call1_enum_type.name == "TestEnumCD"


@pytest.mark.parametrize(
    "types_to_include, public_names",
    [
        (None, ["EnumA", "EnumB", "EnumC"]),
        (["EnumA", "EnumC"], ["EnumA", "EnumC"]),
        (["EnumA", "EnumA", "EnumA"], ["EnumA"]),
    ],
)
def test_generate_returns_module_with_filtered_classes(types_to_include, public_names):
    schema_str = """
    enum EnumA {
      A1
      A2
    }

    enum EnumB {
      B1
      B2
    }

    enum EnumC {
      C1
      C2
    }
    """

    generator = EnumsGenerator(schema=build_ast_schema(parse(schema_str)))
    module = generator.generate(types_to_include=types_to_include)

    class_names = [c.name for c in filter_class_defs(module)]
    assert sorted(generator.get_generated_public_names()) == sorted(public_names)
    assert sorted(class_names) == sorted(public_names)
